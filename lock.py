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
        content = "".join(line.strip() for line in content)

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

execname = 'python2.7 rsa-validate.py -k '+args.validating_public_key+' -m '+args.action_public_key+' -s '+args.action_public_key+'-casig'
proc = subprocess.Popen(execname, stdout=subprocess.PIPE, shell=True)
if proc is False:
    print 'Validation Failed: Exiting'
    sys.exit()

k = binascii.b2a_hex(os.urandom(16))
with open('aeskey',"w+") as f:
    f.write(k)
f.close()
execname = 'python2.7 rsa-enc.py -k '+args.action_private_key+ ' -i '+'aeskey'+' -o '+'sym_key_man'
os.system(execname)
execname = 'python2.7 rsa-sign.py -k '+args.action_private_key+' -m '+'sym_key_man'+' -s sym_key_man-casig'
os.system(execname)

for root, dirs, files in os.walk(yourpath, topdown=False):
    for name in files:
        dest = os.path.join(root,name)
        execname = 'python2.7 cbc-enc.py -k '+'aeskey'+ ' -i '+dest+' -o '+dest
        os.system(execname)
        execname = 'python2.7 cbcmac-tag.py -k '+'aeskey'+ ' -m '+dest+' -t '+dest+'-tag'
        os.system(execname)
    for name in dirs:
        print(os.path.join(root, name))

os.system('cp sym_key_man '+yourpath)
os.system('cp sym_key_man-casig '+yourpath)