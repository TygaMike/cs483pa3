import argparse
import random
import sys
import binascii
from Crypto.Cipher import AES

def parse_file(arg_file):
    with open(arg_file) as f:
        content = f.readline()

    return content

parser = argparse.ArgumentParser()
parser.add_argument('-k', '--key_file', help='specifies a file that contains the key', required=True)
parser.add_argument('-m', '--input_file', help='specifies the path of the message file is being store', required=True)
parser.add_argument('-t', '--output_file', help=' the path of the tag file, either as output forcbcmac-tagor as an input forcbcmac-validate', required=True)
args = parser.parse_args()

key_hex = parse_file(args.key_file)
key = key_hex.strip().decode("hex")
message = parse_file(args.input_file)
message = str(len(message)) + message
message = list(message)
tag = parse_file(args.output_file)
bs = 16 #bytes, 128 bit
messages=[message[i:i+bs] for i in range(0, len(message), bs)]
cipher = AES.AESCipher(key[:16], AES.MODE_ECB)
for index, block in enumerate(messages):
    if block == messages[0]:
        iv_hex = block
        continue
    str_block = ''.join(block)
    #now xor message with iv
    if (len(str_block) != 16):
        diff = 16 - (len(str_block)%16)
        for j in range (0, diff):
            str_block += chr(diff)
    xblock = "".join(chr(ord(x)^ord(y)) for x, y in zip(str_block, str(iv_hex)))
    #convert xor'd message back to a string and append to the ciphertext
    cipherx = cipher.encrypt(xblock)
    ciphert=binascii.hexlify(bytearray(cipherx)).decode('utf-8')
    iv_hex = ciphert #store this block of ciphertext to use as the iv was in this block
if ciphert == tag:
    print 'True'
else:
    print 'False'