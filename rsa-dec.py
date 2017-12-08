import argparse
import random

def parse_file(arg_file):
    with open(arg_file) as f:
        content = f.readlines()

    return content

class RSA(object):

    def __init__(self, N, e_or_d, output_file):
        self.N = N
        self.n = n
        self.e_or_d = e_or_d
        self.output_file = output_file

    def decrypt(self, number_to_decrypt):
        decrypted_number = pow(number_to_decrypt, self.e_or_d, self.N)
        self.write_to_file(decrypted_number)
    
    def unpad(self,padded):
        r = random.getrandbits(n/2)
        ln = len(str(r))
        return padded[ln+2:]

    def write_to_file(self, result):
        with open(self.output_file, 'w') as f:
            f.write(str(result) + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    required_group = parser.add_argument_group('required arguments')

    required_group.add_argument("-k", 
        "--key_file", 
        help="specifies a file storing a valid RSA key in the example format",
        required=True)

    required_group.add_argument("-i",
        "--input",
        help="specifies the path of the file containing an integer in Zn in String form (base 10)",
        required=True)

    required_group.add_argument("-o",
        "--output",
        help="specifies the path of the file where the resulting output is stored in String form (base 10)",
        required=True)

    args = parser.parse_args()
    key_file_contents = parse_file(args.key_file)
    number = parse_file(args.input)[0]
    n = int(key_file_contents[0])
    N = key_file_contents[1]
    e_or_d = key_file_contents[2]
    number = int(number,16)
    rsa = RSA(int(N), int(e_or_d), args.output)
    pd = rsa.unpad(number)
    rsa.decrypt(int(pd))