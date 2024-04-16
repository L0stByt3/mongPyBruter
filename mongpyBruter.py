import argparse
import os
from bruter import BRUTERLSTB

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        #return open(arg, 'r')  # return an open file handle
        return arg
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A simple dictionary attack tool for MongoDB servers. By L0stByt3')
    parser.add_argument("--hosts",
                        help="Path to target(s) host file. File must be content one or more ip address",
                        default="hosts.txt",
                        type=lambda x: is_valid_file(parser, x)
                        )
    parser.add_argument("--target",
                        "-t",
                        help="Single domain or ip address. Ex. 127.0.0.1"
                        )
    parser.add_argument("--user",
                        "-u",
                        help="A single username"
                        )
    parser.add_argument("--password",
                        "-p",
                        help="A single password"
                        )
    parser.add_argument("--nullcredentials",
                        "-n",
                        help="Test conection without credentials",
                        default=False
                        )
    parser.add_argument("--users",
                        help="Path to user list dictionary file. By default is ./users.txt",
                        default="users.txt",
                        type=lambda x: is_valid_file(parser, x)
                        )
    parser.add_argument("--passwords",
                        help="Path to password list dictionary file. By default is ./passwords.txt",
                        default="passwords.txt",
                        type=lambda x: is_valid_file(parser, x)
                        )
    parser.add_argument("-m","--mode",
                        help="Mode can be [unique | list] by default is: list",
                        default="list")
    args = parser.parse_args()

    if args.mode == "list":
        b = BRUTERLSTB(hosts=args.hosts,users=args.users,passwords=args.passwords,mode="list")
        b.do()
    elif args.mode == "unique":
        if args.nullcredentials and args.target is not None:
            b = BRUTERLSTB(single=(args.target,"",""),mode="unique")
        elif args.target != "" and args.user is None and args.password is None and not args.nullcredentials:
            parser.error("--target -t requires -u and -p.")




