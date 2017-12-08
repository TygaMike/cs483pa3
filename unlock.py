import sys
import os
import argparse
import random
import binascii
import subprocess
from Crypto import Random
from Crypto.Cipher import AES
import base64

def parse_file(arg_file):
    with open(arg_file) as f:
        content = f.readlines()
        content = "".join(line for line in content)

    return content

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--directory', help='specifies the directory to lock', required=True)
parser.add_argument('-p', '--action_public_key', help='public key to be used to lock/unlock', required=True)
parser.add_argument('-r', '--action_private_key', help='private rsa key used to lock/unlock', required=True)
parser.add_argument('-vk', '--validating_public_key', help='public key used to verify the action public key', required=True)
args = parser.parse_args()

yourpath = args.directory
apubkey = parse_file(args.action_public_key)
aprivkey = parse_file(args.action_private_key)
valpubkey = parse_file(args.validating_public_key)
#validate public key
execname = 'python2.7 rsa-validate.py -k '+args.validating_public_key+' -m '+args.action_public_key+' -s '+args.action_public_key+'-casig'
proc = subprocess.Popen(execname, stdout=subprocess.PIPE, shell=True)
if proc is False:
    print 'Validation Failed: Exiting'
    sys.exit()
#validate AES key
execname = 'python2.7 rsa-validate.py -k '+args.validating_public_key+' -m '+yourpath+'/sym_key_man'+' -s '+yourpath+'/sym_key_man'+'-casig'
proc = subprocess.Popen(execname, stdout=subprocess.PIPE, shell=True)
if proc is False:
    print 'Validation Failed: Exiting'
    sys.exit()
#decrypt AES key
execname = 'python2.7 rsa-dec.py -k '+args.action_public_key+ ' -i '+yourpath+'/sym_key_man'+' -o '+'aeskey'
os.system(execname)

os.system('rm '+yourpath+'/sym_key_man')
os.system('rm '+yourpath+'/sym_key_man-casig')

for root, dirs, files in os.walk(yourpath, topdown=False):
    for name in files: #validate casig of all files in directory before unlocking
        dest = os.path.join(root,name)

        if (str(dest)[-4:] == '-tag'):
            continue
        else:
            execname = 'python2.7 cbcmac-validate.py -k '+'aeskey'+' -m '+dest+' -t '+dest+'-tag'
            proc = subprocess.Popen(execname, stdout=subprocess.PIPE, shell=True)
            if proc is False:
                print 'Validation Failed: Exiting'
                sys.exit()
            os.system('rm '+dest+'-tag')
    for name in dirs:
        print(os.path.join(root, name))

for root, dirs, files in os.walk(yourpath, topdown=False):
    for name in files:
        dest = os.path.join(root,name)
        if (str(dest)[:-4] == '-tag'):
            continue
        else:
            execname = 'python2.7 cbc-dec.py -k '+'aeskey'+ ' -i '+dest+' -o '+dest
            os.system(execname)
    for name in dirs:
        print(os.path.join(root, name))