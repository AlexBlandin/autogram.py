#!/usr/bin/env python3

import gc
from itertools import count
from pathlib import Path
from random import getrandbits

from humanize import naturalsize as size
from psutil import Process, virtual_memory
from tqdm import tqdm


def autogram(p: str) -> str:
  """
  Self-enumerating pangram ("autogram") generator.

  Based on https://codegolf.stackexchange.com/a/165333 but faster (try PyPy!) and in British English!
  """
  as_word = list(Path("thousand.txt").read_text().splitlines())
  with tqdm(count(), unit=" attempts") as tq:
    hist = set()  # type: set[int] # the almighty cache of hashes we keep around for collisions, our history of hopefuls
    randbits, join = getrandbits, "".join

    def memcheck():  # we like a printout of memory usage, since our cache grows over time (a feature, not a leak!)
      pmp, av = Process().memory_percent(), virtual_memory().available / virtual_memory().total
      tq.set_description(f"{size(Process().memory_info().rss)} used ({pmp:.2f}% used, {av:.2%} free) ")
      if av < 0.3 and pmp > 10:  # if less than 30% memory is free and we're using more than 10% of all memory, cleanup
        hist.clear()  # would like to retain some of this if possible, but we just dump it all for now
        gc.collect()

    word = [join(filter(str.isalpha, w)) + "s" * (w != "one") for w in as_word]  # simplified version of AS_WORD, w/ 's
    old = prelude = f"{join(filter(str.isalpha, p)).lower()}abcdefghijklmnopqrstuvwxyandz"  # don't repeat adding the "and" and alphabet for every `t = `
    counts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for a in old:
      counts[ord(a) - 97] += 1

    for i in tq:
      if i & 2**18 - 1 == 0:
        memcheck()  # update memory usage printout every so often, do cache cleanup if necessary

      new = prelude + join(map(word.__getitem__, counts))
      if new == old:  # a match meant it has closure when recounting, which means we've found our autogram!
        return (
          f"{p} {", ".join(f"{"and " * (a == "z")}{as_word[c]} {a}{"'s" * (c != 1)}" for c, a in zip(counts, "abcdefghijklmnopqrstuvwxyz", strict=False))}."
        )
      old = new
      hn = hash(new)
      if hn in hist:  # pick a new random variation, collisions are fine, as we're just trying to escape cycles...
        counts = [max(0, c + randbits(1) - randbits(1)) for c in counts]  # 50% of ±1 for each letter!
      else:  # count the occurences again
        hist.add(hn)
        counts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for a in new:
          counts[ord(a) - 97] += 1
  return ""  # NOTE unreachable


if __name__ == "__main__":
  print(autogram.__doc__)
  VM, PROC = virtual_memory(), Process()
  print(f"Total memory: {size(VM.total)} (of which {size(VM.available)} ({VM.available / VM.total:.2%}) is available)")
  print(f"Idle memory use: {size(PROC.memory_info().rss)} ({PROC.memory_percent():.2f}%)")

  pangram = autogram(input("Figure out the autogram of: "))

  print()
  with open("./autograms.txt", "a", encoding="utf8", newline="\n") as o:
    o.write(pangram)
    o.write("\n\n")
  print(pangram)
