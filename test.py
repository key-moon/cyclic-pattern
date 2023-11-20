from tqdm import tqdm
import cyclicpattern as cyclicpattern

TEST_LEN = 1000000
pat = cyclicpattern.generate(TEST_LEN)

for i in tqdm(range(len(pat) - 4)):
  s = cyclicpattern.search(pat[i:i+cyclicpattern.DEFAULT_BLOCK_SIZE])
