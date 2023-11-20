#!/usr/bin/python

import string
from ast import literal_eval

DEFAULT_ALPHABET = string.ascii_lowercase + string.ascii_uppercase
DEFAULT_NUMBER = string.digits
DEFAULT_BLOCK_SIZE = 4

class Pattern:
    def __init__(self, alphabet: str, number: str, block_size: int) -> None:
        self.alphabet = alphabet
        self.number = number
        self.block_size = block_size

        self._pattern_cache = ""
        # alphabet: abc ... xyz
        #   number: 012 ... 789
        #    chunk: aaa0aaa1 ... aaa9bbb0 ... zzz8zzz9
        self._chunk_size = len(self.alphabet) * len(self.number) * self.block_size
        self._max_chunk_count = pow(len(self.alphabet), self.block_size - 2)
        self._max_length = self._chunk_size * self._max_chunk_count

    def _generate_chunk(self, chunk_id):
        if self._max_chunk_count <= chunk_id:
            raise ValueError(f"No more chunks can be generated (chunk {chunk_id} requested)")
        offsets = [0] * (self.block_size - 1)

        offset = chunk_id
        for i in range(1, self.block_size - 1)[::-1]:
            offsets[i] = offset % len(self.alphabet)
            offset //= len(self.alphabet)
        
        res = ""
        for i in range(len(self.alphabet)):
            block_prefix = "".join([self.alphabet[(i + offset) % len(self.alphabet)] for offset in offsets])
            res += "".join([block_prefix + c for c in self.number])
        assert len(res) == self._chunk_size
        return res

    def generate(self, n: int):
        if self._max_length <= n:
            raise ValueError(f"Pattern length limit exceeded (requested: {n}, length limit: {self._max_length})")
        while len(self._pattern_cache) < n:
            next_chunk_ind = len(self._pattern_cache) // self._chunk_size
            self._pattern_cache += self._generate_chunk(next_chunk_ind)
        return self._pattern_cache[:n]

    def _parse_alphabet_part(self, alphabet_part: str, base_alphabet: str):
        base_index = self.alphabet.index(base_alphabet)
        hoge = [(self.alphabet.index(c) - base_index) % len(self.alphabet) for c in alphabet_part]
        res = 0
        base = 1
        while 1 <= len(hoge):
            res += base * hoge.pop()
            base *= len(self.alphabet)
        return res

    def _search(self, needle: str):
        number_ind = -1
        for ind, c in enumerate(needle):
            if c in self.number:
                number_ind = ind
                break
        if number_ind == -1:
            raise ValueError(f"Invalid format (number not found)", needle)
        
        num = self.number.index(needle[number_ind])
        prefix, suffix = needle[:number_ind], needle[(number_ind + 1):]

        def _calc_index(alphabet_part: int, alphabet_ind: int, number: int, offset: int):
            return (((alphabet_part * len(self.alphabet)) + alphabet_ind) * len(self.number) + number) * self.block_size + offset

        # not across block (aaa0)
        if len(suffix) == 0:
            return _calc_index(self._parse_alphabet_part(prefix, prefix[0]), self.alphabet.index(prefix[0]), num, 0)

        # not across different alphabet block (aa0a)
        if num != len(self.number) - 1:
            return _calc_index(self._parse_alphabet_part(suffix + prefix, suffix[0]), self.alphabet.index(suffix[0]), num, len(suffix))

        def _rot_alphabet(s, rot):
            return "".join([self.alphabet[(self.alphabet.index(c) + rot) % len(self.alphabet)] for c in s])

        # not across chunk (aa9b)
        if suffix[0] != self.alphabet[0]:
            suffix = _rot_alphabet(suffix, -1)
            return _calc_index(self._parse_alphabet_part(suffix + prefix, suffix[0]), self.alphabet.index(suffix[0]), num, len(suffix))

        # across chunk (zz9a)
        suffix = _rot_alphabet(suffix, -1)
        suffix_base = pow(len(self.alphabet), len(prefix))
        alphabet_index = self._parse_alphabet_part(suffix + prefix, suffix[0])
        if self._parse_alphabet_part(prefix, suffix[0]) == suffix_base - 1: alphabet_index -= suffix_base
        return _calc_index(alphabet_index, self.alphabet.index(suffix[0]), num, len(suffix))

    def search(self, needle: str):
        if len(needle) < self.block_size:
            raise ValueError(f"Not enough information", needle)
        res = self._search(needle[:self.block_size])
        # TODO: speedup
        generated = self.generate(res + len(needle))[res:]
        if generated != needle:
            raise ValueError(f"Unexpected data ({generated=}) ({needle=})")
        return res

pattern = Pattern(DEFAULT_ALPHABET, DEFAULT_NUMBER, DEFAULT_BLOCK_SIZE)
generate = pattern.generate
search = pattern.search

def _parse_num(s: str) -> int:
    s = s.strip()
    res = literal_eval(s)
    if type(res) == int: return res
    raise ValueError("Invalid Value", s)

def main():
    import argparse
    parser = argparse.ArgumentParser()


    # TODO:
    # parser.add_argument("--alphabet", default=None)
    # parser.add_argument("--size", default="4")

    subparser = parser.add_subparsers()
    
    def cli_generate(args):
        print(pattern.generate(_parse_num(args.number)))

    def cli_search(args):
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

    gen_parser = subparser.add_parser("generate", aliases=['g'])
    gen_parser.add_argument("number")
    gen_parser.set_defaults(func=cli_generate)

    search_parser = subparser.add_parser("search", aliases=['s'])
    search_parser.add_argument("pattern")
    search_parser.add_argument("--big", action="store_true")
    search_parser.set_defaults(func=cli_search)

    args = parser.parse_args()
    args.func(args)
