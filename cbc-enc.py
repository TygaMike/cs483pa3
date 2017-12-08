import argparse
import random
import sys
import binascii

from Crypto.Cipher import AES

def parse_file(arg_file):
    with open(arg_file) as f:
        content = f.readlines()
        content = "".join(line for line in content)

    return content

parser = argparse.ArgumentParser()
parser.add_argument('-k', '--key_file', help='specifies a file that contains the key', required=True)
parser.add_argument('-i', '--input_file', help='specifies a file that contains the input', required=True)
parser.add_argument('-o', '--output_file', help='specifies a file that contains the output', required=True)
parser.add_argument('-v', '--iv_file', help='specifies a file that contains the key')
args = parser.parse_args()

if(args.iv_file):
    iv_hex = parse_file(args.iv_file)
    iv = int(iv_hex.strip(),16)
else:
    iv_hex = random.getrandbits(128)
    iv_hex = str(iv_hex)
    iv_hex = iv_hex[:32]
key_hex = parse_file(args.key_file)
key = key_hex.strip()
key = key.decode("hex")
message = list(parse_file(args.input_file))
bs = 16 #bytes, 128 bit
messages=[message[i:i+bs] for i in range(0, len(message), bs)]
ciphertext = ''
ciphertext += str(iv_hex)
cipher = AES.AESCipher(key[:16], AES.MODE_ECB)
for index, block in enumerate(messages):
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
    ciphertext += ciphert
    iv_hex = ciphert #store this block of ciphertext to use as the iv was in this block
fw = open(args.output_file,'w')
fw.write(ciphertext)
fw.close()