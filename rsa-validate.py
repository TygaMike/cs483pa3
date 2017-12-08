import hashlib
import argparse

def parse_file(arg_file):
    with open(arg_file) as f:
        content = f.readlines()

    return content

def hash_message(message):
    hash_object = hashlib.sha256(message)

    return hash_object.hexdigest()

def validate(signature, e, N, hashed_message):
    recevied_message = pow(int(signature), int(e), int(N))

    if recevied_message == int(hashed_message, 16):
        return True

    return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    required_group = parser.add_argument_group('required arguments')

    required_group.add_argument("-k", 
        "--key_file", 
        help="specifies the file of either the public or private key",
        required=True)

    required_group.add_argument("-m",
        "--message_file",
        help="specifies the file that contains the message",
        required=True)

    required_group.add_argument("-s",
        "--signature_file",
        help="specifies the signature file",
        required=True)

    args = parser.parse_args()
    signature = parse_file(args.signature_file)[0]

    message = parse_file(args.message_file)
    message = " ".join(line.strip() for line in message)
    hashed_message = hash_message(message)

    key_file_contents = parse_file(args.key_file)
    N = key_file_contents[1]
    e = key_file_contents[2]

    print validate(signature, e, N, hashed_message)
