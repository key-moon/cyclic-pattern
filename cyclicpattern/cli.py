import string
from argparse import Namespace
from ast import literal_eval

from cyclicpattern import Pattern

def _parse_num(s: str) -> int:
    s = s.strip()
    res = literal_eval(s)
    if type(res) == int: return res
    raise ValueError("Invalid Value", s)

def main():
    import argparse
    parser = argparse.ArgumentParser()

    alphabet_dic = {
        "lowercase": string.ascii_lowercase,
        "uppercase": string.ascii_uppercase,
        "letters": string.ascii_letters,
        "digits": string.digits,
        "hexdigits": string.hexdigits,
        "octdigits": string.octdigits,
        "punctuation": string.punctuation
    }

    parser.add_argument("--digits", default="digits", help=f"sets of digits, or names of the set ({', '.join(alphabet_dic.keys())})")
    parser.add_argument("--alphabet", default="letters", help=f"sets of alphabet, or names of the set ({', '.join(alphabet_dic.keys())})")
    parser.add_argument("--size", type=int, default=4, help="size of each blocks")

    subparser = parser.add_subparsers()
    
    def cli_info(args: Namespace, pattern: Pattern):
        print("alphabet:", pattern.alphabet)
        print("digits:", pattern.digit)
        print("block size:", pattern.block_size)
        print("max length:", pattern._max_length)

    def cli_generate(args: Namespace, pattern: Pattern):
        print(pattern.generate(_parse_num(args.digit)))

    def cli_search(args: Namespace, pattern: Pattern):
        s = args.pattern
        def test(s):
            try:
                res = pattern.search(s)
                print(res)
                exit(0)
            except Exception as e:
                return e

        l = []
        l.append(test(s))
        # hex
        _s = s[2:] if s.startswith("0x") else s
        if all(c in string.hexdigits for c in _s):
            decoded = bytes.fromhex(_s).decode()
            if not (args.big): decoded = decoded[::-1]
            l.append(test(decoded))
        assert False, ("[!] pattern not found.", l)

    gen_parser = subparser.add_parser("info", aliases=['i'])
    gen_parser.set_defaults(func=cli_info)

    gen_parser = subparser.add_parser("generate", aliases=['g'])
    gen_parser.add_argument("digit")
    gen_parser.set_defaults(func=cli_generate)

    search_parser = subparser.add_parser("search", aliases=['s'])
    search_parser.add_argument("pattern")
    search_parser.add_argument("--big", action="store_true")
    search_parser.set_defaults(func=cli_search)

    args = parser.parse_args()

    def parse_alphabet(val: str):
        return alphabet_dic[val] if val in alphabet_dic else val

    alphabet = parse_alphabet(args.alphabet)
    digits = parse_alphabet(args.digits)

    pattern = Pattern(alphabet, digits, args.size)

    if "func" not in args:
        parser.print_help()
        exit(1)

    args.func(args, pattern)
