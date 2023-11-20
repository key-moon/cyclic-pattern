# Cyclic Pattern

CLI Tools / Python library to generate and search pattern strings useful for finding offsets in Binary Exploitation.

## installation
```sh
pip install cyclic-pattern
```

## generate pattern

- generate pattern
```sh
pattern g 10000
# output: aaa0aaa1 ... PPT8PPT9
```

- you can also use the string valid as integer literal (like bin, oct, and hex)
```sh
pattern g 0b1_00_00
# output: aaa0aaa1aaa2aaa3
```

## search pattern

- search pattern in string
```sh
pattern s PPT8PPT9
# output: 9992
```

- search pattern in hex
```sh
pattern s 0x3567676734676767
# output: 256
pattern s --big 0x6767673467676735 # big endian
# output: 256
```

## customize

- generate and search pattern with custom block size
```sh
pattern --size 8 g 36
# output: aaaaaaa0aaaaaaa1aaaaaaa2aaaaaaa3aaaa
pattern --size 8 s uuuuuuw9
# output: 9992
```

- generate and search pattern with custom alphabet and digits
```sh
pattern --alphabet ab --digits 12 g 36
# output: aaa1aaa2bbb1bbb2aab1aab2bba1bba2aba1
pattern --alphabet ab --digits 12 s aba1
# output: 32
```

- alphabet and digits can be specified with preset name (lowercase, uppercase, letters, digits, hexdigits, octdigits, punctuation)
```sh
pattern --alphabet lowercase --digits octdigits g 1000
# output: aaa0aaa1aaa2aaa3 ... eef6eef7ffg0ffg1
pattern --alphabet lowercase --digits octdigits s ffg1
# output: 996
```

- check information of current configuration
```sh
pattern --alphabet abc --digits 012345 --size 6 i
# output:
# alphabet: abc
# digits: 012345
# block size: 6
# max length: 8748
```
