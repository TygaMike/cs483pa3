import hashlib
import argparse

def parse_file(arg_file):
    with open(arg_file) as f:
        content = f.readlines()

    return content

def hash_message(message):
    hash_object = hashlib.sha256(message)

    return hash_object.hexdigest()

def sign(hashed_message, N, d):
    number = int(hashed_message, 16)

    return pow(number, int(d), int(N))

def write_to_file(result, file_name):
    with open(file_name, 'w+') as f:
        f.write(str(result))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    required_group = parser.add_argument_group('required arguments')

    required_group.add_argument("-k", 
        "--key_file", 
        help="specifies the file of either the public or private key",
        required=True)

    required_group.add_argument("-m",
        "--message_file",
        help="specifies the file that contains the message to be signed",
        required=True)

    required_group.add_argument("-s",
        "--signature_file",
        help="specifies the output file",
        required=True)

    args = parser.parse_args()
    output_file = args.signature_file
    message = parse_file(args.message_file)
    message = " ".join(line.strip() for line in message)

    key_file_contents = parse_file(args.key_file)
    N = key_file_contents[1]
    d = key_file_contents[2]

    hashed_message = hash_message(message)
    signed_message = sign(hashed_message, N, d)

    write_to_file(signed_message, output_file)