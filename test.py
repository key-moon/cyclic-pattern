from tqdm import tqdm
import pattern as pattern

TEST_LEN = 1000000
pat = pattern.generate(TEST_LEN)

for i in tqdm(range(len(pat) - 4)):
  s = pattern.search(pat[i:i+pattern.DEFAULT_BLOCK_SIZE])
