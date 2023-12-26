#!/usr/bin/env python3

import gc
from itertools import count  # tell tqdm to keep going
from random import getrandbits  # the fastest way to get a small random number

from humanize import naturalsize as size
from psutil import Process, virtual_memory
from tqdm import tqdm


def autogram(p: str) -> str | None:
  """
  Self-enumerating pangram ("autogram") generator.

  Based on https://codegolf.stackexchange.com/a/165333 but faster (try PyPy!) and in British English!
  """
  with open("thousand.txt", encoding="utf8") as f:
    as_word = list(map(str.strip, f.readlines()))
  with tqdm(count(), unit=" attempts") as tq:
    hist = set()  # type: set[int] # the almighty cache of hashes we keep around for collisions, our history of hopefuls
    randbits, join = getrandbits, "".join

    def memcheck():  # we like a printout of memory usage, since our cache grows over time (a feature, not a leak!)
      pmp, av = Process().memory_percent(), virtual_memory().available / virtual_memory().total
      tq.set_description(f"{size(Process().memory_info().rss)} used ({pmp:.2f}% used, {av:.2%} free) ")
      if av < 0.3 and pmp > 10:  # if less than 30% memory is free and we're using more than 10% of all memory, cleanup
        hist.clear()  # would like to retain some of this if possible, but we just dump it all for now
        gc.collect()

    def occurences(s):
      "occurences of each letter, 0..25=a..z"
      occ = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      for a in s:
        occ[ord(a) - 97] += 1
      return occ

    word = [occurences(filter(str.isalpha, x)) for x in as_word]  # simplified version of AS_WORD
    word[0][ord("s") - 97] += 1  # add in the extra 's for plurals
    for w in word[2:]:
      w[ord("s") - 97] += 1  # add in the extra 's for plurals

    old = new = prelude = occurences(
      f"{join(filter(str.isalpha, p)).lower()}abcdefghijklmnopqrstuvwxyandz"
    )  # don't repeat adding the "and" and alphabet for every `t = `

    for i in tq:
      if i & 2**18 - 1 == 0:
        memcheck()  # update memory usage printout every so often, do cache cleanup if necessary

      new = prelude
      for a in old:
        for j in range(26):
          new[i] += word[a][j]
      if new == old:  # a match meant it has closure when recounting, which means we've found our autogram!
        return f"{p} {", ".join(f"{"and " * (a == "z")}{as_word[c]} {a}{"'s" * (c != 1)}" for c, a in zip(new, "abcdefghijklmnopqrstuvwxyz", strict=False))}."
      old = new
      hn = hash(tuple(new))
      if hn in hist:  # pick a new random variation, collisions are fine, as we're just trying to escape cycles...
        new = [max(0, c + randbits(1) - randbits(1)) for c in new]  # 50% of ±1 for each letter!
      else:  # count the occurences again
        hist.add(hn)
        new = prelude
        for a in old:
          for j in range(26):
            new[i] = word[a][j]


if __name__ == "__main__":
  print(autogram.__doc__)
  VM, PROC = virtual_memory(), Process()
  print(f"Total memory: {size(VM.total)} (of which {size(VM.available)} ({VM.available / VM.total:.2%}) is available)")
  print(f"Idle memory use: {size(PROC.memory_info().rss)} ({PROC.memory_percent():.2f}%)")

  pangram = autogram(input("Figure out the autogram of: "))
  if pangram:
    print()
    with open("./autograms.txt", "a", encoding="utf8", newline="\n") as o:
      o.write(pangram)
      o.write("\n\n")
    print(pangram)
