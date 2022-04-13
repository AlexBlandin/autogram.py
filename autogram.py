from itertools import count, chain
from random import getrandbits
from time import sleep
import gc
try:
  from functools import cache
except:
  from functools import lru_cache as cache

from psutil import Process, virtual_memory
from humanize import naturalsize
from tqdm import tqdm

def autogram(p: str):
  @cache
  def as_word(n: int):
    word = [b"zero", b"one", b"two", b"three", b"four", b"five", b"six", b"seven", b"eight", b"nine"]
    n, m = divmod(n, 100)
    e, d = divmod(m, 10)
    return b" ".join([word[n], b"hundred"]*(n > 0) + ([[b"ten", b"eleven", b"twelve", b"thir", b"four", b"fif", b"six", b"seven", b"eigh", b"nine"][d] + b"teen" * (d > 2)] if 9 < m < 20 else [[b"twen", b"thir", b"for", b"fif", b"six", b"seven", b"eigh", b"nine"][e - 2] + b"ty"]*(e > 0) + [word[d]]*(d > 0)))
  with tqdm(count(), unit=" attempts") as tq:
    T, s, proc = {hash(b"")}, b"", Process()
    pmi, pmp = proc.memory_info, proc.memory_percent
    join, ch, grb, ns = b"".join, chain, getrandbits, naturalsize # locals avoids global lookup
    pb = bytes(p.replace(" ",""), encoding="utf8").lower() + b'and' # convert to bytes to reduce memory
    for i in tq:
      if i%50000 == 0:
        tq.set_description(f"{ns(pmi().rss)} ({pmp():.2f}%) used ")
        if pmp() > 5: # switch to "less than X% free memory remaining?"
          print(f"\rUsing {pmp():.2f}% of total memory ({ns(pmi().rss)}), give me a moment...",end="")
          T.clear()
          as_word.cache_clear() # would like to retain much of this, but rn we don't
          gc.collect(); sleep(1); gc.collect(); sleep(1); gc.collect(); sleep(1); gc.collect()
          print(f"\rUsing {ns(pmi().rss)} ({pmp():.2f}%) with {as_word.cache_info()}.",end=""); sleep(5)
      t = join(ch([pb],(as_word(sc) + bytes(chr(c), encoding="utf8") + b"s"*(sc != 1) for c,sc in zip(b"abcdefghijklmnopqrstuvwxyz", map(s.count, b"abcdefghijklmnopqrstuvwxyz")))))
      if s == t:
        return f"""{p} {", ".join(f'''{"and " * (chr(c) == "z")}{as_word(sc).decode()} {chr(c)}{"'s" * (sc != 1)}''' for c,sc in zip(b"abcdefghijklmnopqrstuvwxyz", map(s.count, b"abcdefghijklmnopqrstuvwxyz")))}."""
      if hash(t) in T: # pick random variation, collision is fine as s != t, and this makes T ~8x smaller
        t = join(bytes(chr(c), encoding="utf8") * max(1, s.count(c) + (grb(3) - 4)*(grb(1) == 0)) for c in b"abcdefghijklmnopqrstuvwxyz")
      T.add(hash(t))
      s = t

if __name__ == "__main__":
  print("Self-enumerating pangram (\"autogram\") generator.")
  print("Based on https://codegolf.stackexchange.com/a/165333 but significantly faster; try pypy!")
  print(f"Total memory: {naturalsize(virtual_memory().total)} (of which {naturalsize(virtual_memory().available)} is available)")
  print(f"Idle memory use: {naturalsize(Process().memory_info().rss)} ({Process().memory_percent():.2f}%)")
  pg = autogram(input("Figure out the autogram of: "))
  print()
  with open("./autograms.txt", "a", encoding="utf8", newline="\n") as o:
    o.write(f"{pg}\n\n")
  print(pg)
