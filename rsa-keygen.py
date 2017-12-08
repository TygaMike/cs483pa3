import argparse
import os
from random import randrange
from random import getrandbits
from fractions import gcd

class RSAKeygen(object):

    def __init__(self, pub_file, priv_file):
        self.pub_file = pub_file
        self.priv_file = priv_file

    def generate_keypair(self, size):
        low = 1 << (size // 2 - 1)
        high = 1 << (size // 2 + 1)
        min_num = 1 << (size - 1)
        max_num = (1 << size) - 1

        first_prime = self.generate_prime_number_in_range(low, high)
        second_prime = self.generate_prime_number_in_range(low, high)

        while not min_num <= first_prime * second_prime <= max_num:
            second_prime = self.generate_prime_number_in_range(low, high)
            first_prime = self.generate_prime_number_in_range(low, high)
 
        phi = (first_prime - 1) * (second_prime - 1)
        e = randrange(1, phi)

        # Guess and check for e, cannot iterate through phi when dealing with extremely large bit sizes
        while not self.is_relatively_prime(e, phi):
            e = randrange(1, phi)

        d = self.get_multiplicative_inverse(e, phi)

        N = first_prime * second_prime

        self.export_to_files(size, N, e, d)

    def is_prime(self, number, check_count=5):
        if (number < 2):
            return False

        count = 0
        s = number - 1

        while s % 2 == 0:
            s = s // 2
            count += 1

        for check in range(check_count):
            a_random = randrange(2, number - 1)
            v = pow(a_random, s, number)

            if v == 1:
			    return True
		    
            for i in xrange(count - 1):
                if v == number - 1:
                    return True

                v = pow(v, 2, number)

            return v == number - 1

    def is_relatively_prime(self, first, second):
        if gcd(first, second) == 1:
            return True

        return False

    def get_multiplicative_inverse(self, e, phi):
        d = 0
        x1 = 0
        x2 = 1
        y1 = 1
        phi_copy = phi
        
        while e > 0:
            phi_over_e = phi_copy / e
            result = phi_copy - phi_over_e * e
            phi_copy = e
            e = result
            x = x2 - phi_over_e * x1
            y = d - phi_over_e * y1
            x2 = x1
            x1 = x
            d = y1
            y1 = y
        
        if phi_copy == 1:
            return d + phi

    def generate_prime_number_in_range(self, low, high):
        while True:
            number = randrange(low, high)
            if self.is_prime(number):
                return number

    def export_to_files(self, n, N, e, d):
        with open(self.pub_file, 'w') as f:
            f.write(str(n) + '\n')
            f.write(str(N) + '\n')
            f.write(str(e) + '\n')

        with open(self.priv_file, 'w') as f:
            f.write(str(n) + '\n')
            f.write(str(N) + '\n')
            f.write(str(d) + '\n')

        if cabool:
            execname = 'python2.7 rsa-sign.py -k '+args.ca_file+' -m '+self.pub_file+' -s '+self.pub_file+'-casig'
            os.system(execname)
        else:
            execname = 'python2.7 rsa-sign.py -k '+self.priv_file+' -m '+self.pub_file+' -s '+self.pub_file+'-casig'
            os.system(execname)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    required_group = parser.add_argument_group('required arguments')

    required_group.add_argument("-p", 
        "--public_key_file", 
        help="specifies the file to store the public key",
        required=True)

    required_group.add_argument("-s",
        "--private_key_file",
        help="specifies the file to store the private key",
        required=True)

    required_group.add_argument("-n",
        "--number_of_bits",
        help="specifies the number of bits in your N",
        required=True)

    required_group.add_argument("-c",
        "--ca_file",
        help="key to generate signature with")

    args = parser.parse_args()

    if(args.ca_file):
        cabool = True
    else:
        cabool = False

    keygen = RSAKeygen(args.public_key_file, args.private_key_file)
    keygen.generate_keypair(int(args.number_of_bits))
