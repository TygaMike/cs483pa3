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
    iv = int(iv_hex.strip(),32)
else:
    iv = random.randint(1,sys.maxsize)
key_hex = parse_file(args.key_file)
key = key_hex.strip().decode("hex")
ciphertext = list(parse_file(args.input_file))
bs = 32
messages=[ciphertext[i:i+bs] for i in range(0, len(ciphertext), bs)]
message = ''
cipher = AES.AESCipher(key[:32], AES.MODE_ECB)
prior = None

for index, block in enumerate(messages): #go through the blocks backwards to decrypt
    if(prior is not None):
        #if it isn't the IV, actually do stuff
        str_block = ''.join(block)
        enc = binascii.unhexlify(str_block)
        cipherx = cipher.decrypt(enc)  
        #send the cipher block backwards through Fk
        #xor decrypted cipher with the previous block of ciphertext
        xblock = "".join(chr(ord(x)^ord(y)) for x, y in zip(cipherx, prior))

        if(block is messages[-1]):
            #if the block is the last one remove padding
            amount = ord(xblock[-1])
            for i in range(0, amount):
                xblock = xblock[:-1]
        message += xblock
    prior = block
fw = open(args.output_file,'w')
fw.write(message)
fw.close()