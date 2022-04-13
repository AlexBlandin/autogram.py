from random import getrandbits
from itertools import count
import gc

from psutil import Process, virtual_memory
from humanize import naturalsize
from tqdm import tqdm

def autogram(p: str):
  as_word = ("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty", "twenty-one", "twenty-two", "twenty-three", "twenty-four", "twenty-five", "twenty-six", "twenty-seven", "twenty-eight", "twenty-nine", "thirty", "thirty-one", "thirty-two", "thirty-three", "thirty-four", "thirty-five", "thirty-six", "thirty-seven", "thirty-eight", "thirty-nine", "forty", "forty-one", "forty-two", "forty-three", "forty-four", "forty-five", "forty-six", "forty-seven", "forty-eight", "forty-nine", "fifty", "fifty-one", "fifty-two", "fifty-three", "fifty-four", "fifty-five", "fifty-six", "fifty-seven", "fifty-eight", "fifty-nine", "sixty", "sixty-one", "sixty-two", "sixty-three", "sixty-four", "sixty-five", "sixty-six", "sixty-seven", "sixty-eight", "sixty-nine", "seventy", "seventy-one", "seventy-two", "seventy-three", "seventy-four", "seventy-five", "seventy-six", "seventy-seven", "seventy-eight", "seventy-nine", "eighty", "eighty-one", "eighty-two", "eighty-three", "eighty-four", "eighty-five", "eighty-six", "eighty-seven", "eighty-eight", "eighty-nine", "ninety", "ninety-one", "ninety-two", "ninety-three", "ninety-four", "ninety-five", "ninety-six", "ninety-seven", "ninety-eight", "ninety-nine", "a hundred", "a hundred and one", "a hundred and two", "a hundred and three", "a hundred and four", "a hundred and five", "a hundred and six", "a hundred and seven", "a hundred and eight", "a hundred and nine", "a hundred and ten", "a hundred and eleven", "a hundred and twelve", "a hundred and thirteen", "a hundred and fourteen", "a hundred and fifteen", "a hundred and sixteen", "a hundred and seventeen", "a hundred and eighteen", "a hundred and nineteen", "a hundred and twenty", "a hundred and twenty-one", "a hundred and twenty-two", "a hundred and twenty-three", "a hundred and twenty-four", "a hundred and twenty-five", "a hundred and twenty-six", "a hundred and twenty-seven", "a hundred and twenty-eight", "a hundred and twenty-nine", "a hundred and thirty", "a hundred and thirty-one", "a hundred and thirty-two", "a hundred and thirty-three", "a hundred and thirty-four", "a hundred and thirty-five", "a hundred and thirty-six", "a hundred and thirty-seven", "a hundred and thirty-eight", "a hundred and thirty-nine", "a hundred and forty", "a hundred and forty-one", "a hundred and forty-two", "a hundred and forty-three", "a hundred and forty-four", "a hundred and forty-five", "a hundred and forty-six", "a hundred and forty-seven", "a hundred and forty-eight", "a hundred and forty-nine", "a hundred and fifty", "a hundred and fifty-one", "a hundred and fifty-two", "a hundred and fifty-three", "a hundred and fifty-four", "a hundred and fifty-five", "a hundred and fifty-six", "a hundred and fifty-seven", "a hundred and fifty-eight", "a hundred and fifty-nine", "a hundred and sixty", "a hundred and sixty-one", "a hundred and sixty-two", "a hundred and sixty-three", "a hundred and sixty-four", "a hundred and sixty-five", "a hundred and sixty-six", "a hundred and sixty-seven", "a hundred and sixty-eight", "a hundred and sixty-nine", "a hundred and seventy", "a hundred and seventy-one", "a hundred and seventy-two", "a hundred and seventy-three", "a hundred and seventy-four", "a hundred and seventy-five", "a hundred and seventy-six", "a hundred and seventy-seven", "a hundred and seventy-eight", "a hundred and seventy-nine", "a hundred and eighty", "a hundred and eighty-one", "a hundred and eighty-two", "a hundred and eighty-three", "a hundred and eighty-four", "a hundred and eighty-five", "a hundred and eighty-six", "a hundred and eighty-seven", "a hundred and eighty-eight", "a hundred and eighty-nine", "a hundred and ninety", "a hundred and ninety-one", "a hundred and ninety-two", "a hundred and ninety-three", "a hundred and ninety-four", "a hundred and ninety-five", "a hundred and ninety-six", "a hundred and ninety-seven", "a hundred and ninety-eight", "a hundred and ninety-nine", "two hundred", "two hundred and one", "two hundred and two", "two hundred and three", "two hundred and four", "two hundred and five", "two hundred and six", "two hundred and seven", "two hundred and eight", "two hundred and nine", "two hundred and ten", "two hundred and eleven", "two hundred and twelve", "two hundred and thirteen", "two hundred and fourteen", "two hundred and fifteen", "two hundred and sixteen", "two hundred and seventeen", "two hundred and eighteen", "two hundred and nineteen", "two hundred and twenty", "two hundred and twenty-one", "two hundred and twenty-two", "two hundred and twenty-three", "two hundred and twenty-four", "two hundred and twenty-five", "two hundred and twenty-six", "two hundred and twenty-seven", "two hundred and twenty-eight", "two hundred and twenty-nine", "two hundred and thirty", "two hundred and thirty-one", "two hundred and thirty-two", "two hundred and thirty-three", "two hundred and thirty-four", "two hundred and thirty-five", "two hundred and thirty-six", "two hundred and thirty-seven", "two hundred and thirty-eight", "two hundred and thirty-nine", "two hundred and forty", "two hundred and forty-one", "two hundred and forty-two", "two hundred and forty-three", "two hundred and forty-four", "two hundred and forty-five", "two hundred and forty-six", "two hundred and forty-seven", "two hundred and forty-eight", "two hundred and forty-nine", "two hundred and fifty", "two hundred and fifty-one", "two hundred and fifty-two", "two hundred and fifty-three", "two hundred and fifty-four", "two hundred and fifty-five", "two hundred and fifty-six", "two hundred and fifty-seven", "two hundred and fifty-eight", "two hundred and fifty-nine", "two hundred and sixty", "two hundred and sixty-one", "two hundred and sixty-two", "two hundred and sixty-three", "two hundred and sixty-four", "two hundred and sixty-five", "two hundred and sixty-six", "two hundred and sixty-seven", "two hundred and sixty-eight", "two hundred and sixty-nine", "two hundred and seventy", "two hundred and seventy-one", "two hundred and seventy-two", "two hundred and seventy-three", "two hundred and seventy-four", "two hundred and seventy-five", "two hundred and seventy-six", "two hundred and seventy-seven", "two hundred and seventy-eight", "two hundred and seventy-nine", "two hundred and eighty", "two hundred and eighty-one", "two hundred and eighty-two", "two hundred and eighty-three", "two hundred and eighty-four", "two hundred and eighty-five", "two hundred and eighty-six", "two hundred and eighty-seven", "two hundred and eighty-eight", "two hundred and eighty-nine", "two hundred and ninety", "two hundred and ninety-one", "two hundred and ninety-two", "two hundred and ninety-three", "two hundred and ninety-four", "two hundred and ninety-five", "two hundred and ninety-six", "two hundred and ninety-seven", "two hundred and ninety-eight", "two hundred and ninety-nine", "three hundred", "three hundred and one", "three hundred and two", "three hundred and three", "three hundred and four", "three hundred and five", "three hundred and six", "three hundred and seven", "three hundred and eight", "three hundred and nine", "three hundred and ten", "three hundred and eleven", "three hundred and twelve", "three hundred and thirteen", "three hundred and fourteen", "three hundred and fifteen", "three hundred and sixteen", "three hundred and seventeen", "three hundred and eighteen", "three hundred and nineteen", "three hundred and twenty", "three hundred and twenty-one", "three hundred and twenty-two", "three hundred and twenty-three", "three hundred and twenty-four", "three hundred and twenty-five", "three hundred and twenty-six", "three hundred and twenty-seven", "three hundred and twenty-eight", "three hundred and twenty-nine", "three hundred and thirty", "three hundred and thirty-one", "three hundred and thirty-two", "three hundred and thirty-three", "three hundred and thirty-four", "three hundred and thirty-five", "three hundred and thirty-six", "three hundred and thirty-seven", "three hundred and thirty-eight", "three hundred and thirty-nine", "three hundred and forty", "three hundred and forty-one", "three hundred and forty-two", "three hundred and forty-three", "three hundred and forty-four", "three hundred and forty-five", "three hundred and forty-six", "three hundred and forty-seven", "three hundred and forty-eight", "three hundred and forty-nine", "three hundred and fifty", "three hundred and fifty-one", "three hundred and fifty-two", "three hundred and fifty-three", "three hundred and fifty-four", "three hundred and fifty-five", "three hundred and fifty-six", "three hundred and fifty-seven", "three hundred and fifty-eight", "three hundred and fifty-nine", "three hundred and sixty", "three hundred and sixty-one", "three hundred and sixty-two", "three hundred and sixty-three", "three hundred and sixty-four", "three hundred and sixty-five", "three hundred and sixty-six", "three hundred and sixty-seven", "three hundred and sixty-eight", "three hundred and sixty-nine", "three hundred and seventy", "three hundred and seventy-one", "three hundred and seventy-two", "three hundred and seventy-three", "three hundred and seventy-four", "three hundred and seventy-five", "three hundred and seventy-six", "three hundred and seventy-seven", "three hundred and seventy-eight", "three hundred and seventy-nine", "three hundred and eighty", "three hundred and eighty-one", "three hundred and eighty-two", "three hundred and eighty-three", "three hundred and eighty-four", "three hundred and eighty-five", "three hundred and eighty-six", "three hundred and eighty-seven", "three hundred and eighty-eight", "three hundred and eighty-nine", "three hundred and ninety", "three hundred and ninety-one", "three hundred and ninety-two", "three hundred and ninety-three", "three hundred and ninety-four", "three hundred and ninety-five", "three hundred and ninety-six", "three hundred and ninety-seven", "three hundred and ninety-eight", "three hundred and ninety-nine", "four hundred", "four hundred and one", "four hundred and two", "four hundred and three", "four hundred and four", "four hundred and five", "four hundred and six", "four hundred and seven", "four hundred and eight", "four hundred and nine", "four hundred and ten", "four hundred and eleven", "four hundred and twelve", "four hundred and thirteen", "four hundred and fourteen", "four hundred and fifteen", "four hundred and sixteen", "four hundred and seventeen", "four hundred and eighteen", "four hundred and nineteen", "four hundred and twenty", "four hundred and twenty-one", "four hundred and twenty-two", "four hundred and twenty-three", "four hundred and twenty-four", "four hundred and twenty-five", "four hundred and twenty-six", "four hundred and twenty-seven", "four hundred and twenty-eight", "four hundred and twenty-nine", "four hundred and thirty", "four hundred and thirty-one", "four hundred and thirty-two", "four hundred and thirty-three", "four hundred and thirty-four", "four hundred and thirty-five", "four hundred and thirty-six", "four hundred and thirty-seven", "four hundred and thirty-eight", "four hundred and thirty-nine", "four hundred and forty", "four hundred and forty-one", "four hundred and forty-two", "four hundred and forty-three", "four hundred and forty-four", "four hundred and forty-five", "four hundred and forty-six", "four hundred and forty-seven", "four hundred and forty-eight", "four hundred and forty-nine", "four hundred and fifty", "four hundred and fifty-one", "four hundred and fifty-two", "four hundred and fifty-three", "four hundred and fifty-four", "four hundred and fifty-five", "four hundred and fifty-six", "four hundred and fifty-seven", "four hundred and fifty-eight", "four hundred and fifty-nine", "four hundred and sixty", "four hundred and sixty-one", "four hundred and sixty-two", "four hundred and sixty-three", "four hundred and sixty-four", "four hundred and sixty-five", "four hundred and sixty-six", "four hundred and sixty-seven", "four hundred and sixty-eight", "four hundred and sixty-nine", "four hundred and seventy", "four hundred and seventy-one", "four hundred and seventy-two", "four hundred and seventy-three", "four hundred and seventy-four", "four hundred and seventy-five", "four hundred and seventy-six", "four hundred and seventy-seven", "four hundred and seventy-eight", "four hundred and seventy-nine", "four hundred and eighty", "four hundred and eighty-one", "four hundred and eighty-two", "four hundred and eighty-three", "four hundred and eighty-four", "four hundred and eighty-five", "four hundred and eighty-six", "four hundred and eighty-seven", "four hundred and eighty-eight", "four hundred and eighty-nine", "four hundred and ninety", "four hundred and ninety-one", "four hundred and ninety-two", "four hundred and ninety-three", "four hundred and ninety-four", "four hundred and ninety-five", "four hundred and ninety-six", "four hundred and ninety-seven", "four hundred and ninety-eight", "four hundred and ninety-nine", "five hundred", "five hundred and one", "five hundred and two", "five hundred and three", "five hundred and four", "five hundred and five", "five hundred and six", "five hundred and seven", "five hundred and eight", "five hundred and nine", "five hundred and ten", "five hundred and eleven", "five hundred and twelve", "five hundred and thirteen", "five hundred and fourteen", "five hundred and fifteen", "five hundred and sixteen", "five hundred and seventeen", "five hundred and eighteen", "five hundred and nineteen", "five hundred and twenty", "five hundred and twenty-one", "five hundred and twenty-two", "five hundred and twenty-three", "five hundred and twenty-four", "five hundred and twenty-five", "five hundred and twenty-six", "five hundred and twenty-seven", "five hundred and twenty-eight", "five hundred and twenty-nine", "five hundred and thirty", "five hundred and thirty-one", "five hundred and thirty-two", "five hundred and thirty-three", "five hundred and thirty-four", "five hundred and thirty-five", "five hundred and thirty-six", "five hundred and thirty-seven", "five hundred and thirty-eight", "five hundred and thirty-nine", "five hundred and forty", "five hundred and forty-one", "five hundred and forty-two", "five hundred and forty-three", "five hundred and forty-four", "five hundred and forty-five", "five hundred and forty-six", "five hundred and forty-seven", "five hundred and forty-eight", "five hundred and forty-nine", "five hundred and fifty", "five hundred and fifty-one", "five hundred and fifty-two", "five hundred and fifty-three", "five hundred and fifty-four", "five hundred and fifty-five", "five hundred and fifty-six", "five hundred and fifty-seven", "five hundred and fifty-eight", "five hundred and fifty-nine", "five hundred and sixty", "five hundred and sixty-one", "five hundred and sixty-two", "five hundred and sixty-three", "five hundred and sixty-four", "five hundred and sixty-five", "five hundred and sixty-six", "five hundred and sixty-seven", "five hundred and sixty-eight", "five hundred and sixty-nine", "five hundred and seventy", "five hundred and seventy-one", "five hundred and seventy-two", "five hundred and seventy-three", "five hundred and seventy-four", "five hundred and seventy-five", "five hundred and seventy-six", "five hundred and seventy-seven", "five hundred and seventy-eight", "five hundred and seventy-nine", "five hundred and eighty", "five hundred and eighty-one", "five hundred and eighty-two", "five hundred and eighty-three", "five hundred and eighty-four", "five hundred and eighty-five", "five hundred and eighty-six", "five hundred and eighty-seven", "five hundred and eighty-eight", "five hundred and eighty-nine", "five hundred and ninety", "five hundred and ninety-one", "five hundred and ninety-two", "five hundred and ninety-three", "five hundred and ninety-four", "five hundred and ninety-five", "five hundred and ninety-six", "five hundred and ninety-seven", "five hundred and ninety-eight", "five hundred and ninety-nine", "six hundred", "six hundred and one", "six hundred and two", "six hundred and three", "six hundred and four", "six hundred and five", "six hundred and six", "six hundred and seven", "six hundred and eight", "six hundred and nine", "six hundred and ten", "six hundred and eleven", "six hundred and twelve", "six hundred and thirteen", "six hundred and fourteen", "six hundred and fifteen", "six hundred and sixteen", "six hundred and seventeen", "six hundred and eighteen", "six hundred and nineteen", "six hundred and twenty", "six hundred and twenty-one", "six hundred and twenty-two", "six hundred and twenty-three", "six hundred and twenty-four", "six hundred and twenty-five", "six hundred and twenty-six", "six hundred and twenty-seven", "six hundred and twenty-eight", "six hundred and twenty-nine", "six hundred and thirty", "six hundred and thirty-one", "six hundred and thirty-two", "six hundred and thirty-three", "six hundred and thirty-four", "six hundred and thirty-five", "six hundred and thirty-six", "six hundred and thirty-seven", "six hundred and thirty-eight", "six hundred and thirty-nine", "six hundred and forty", "six hundred and forty-one", "six hundred and forty-two", "six hundred and forty-three", "six hundred and forty-four", "six hundred and forty-five", "six hundred and forty-six", "six hundred and forty-seven", "six hundred and forty-eight", "six hundred and forty-nine", "six hundred and fifty", "six hundred and fifty-one", "six hundred and fifty-two", "six hundred and fifty-three", "six hundred and fifty-four", "six hundred and fifty-five", "six hundred and fifty-six", "six hundred and fifty-seven", "six hundred and fifty-eight", "six hundred and fifty-nine", "six hundred and sixty", "six hundred and sixty-one", "six hundred and sixty-two", "six hundred and sixty-three", "six hundred and sixty-four", "six hundred and sixty-five", "six hundred and sixty-six", "six hundred and sixty-seven", "six hundred and sixty-eight", "six hundred and sixty-nine", "six hundred and seventy", "six hundred and seventy-one", "six hundred and seventy-two", "six hundred and seventy-three", "six hundred and seventy-four", "six hundred and seventy-five", "six hundred and seventy-six", "six hundred and seventy-seven", "six hundred and seventy-eight", "six hundred and seventy-nine", "six hundred and eighty", "six hundred and eighty-one", "six hundred and eighty-two", "six hundred and eighty-three", "six hundred and eighty-four", "six hundred and eighty-five", "six hundred and eighty-six", "six hundred and eighty-seven", "six hundred and eighty-eight", "six hundred and eighty-nine", "six hundred and ninety", "six hundred and ninety-one", "six hundred and ninety-two", "six hundred and ninety-three", "six hundred and ninety-four", "six hundred and ninety-five", "six hundred and ninety-six", "six hundred and ninety-seven", "six hundred and ninety-eight", "six hundred and ninety-nine", "seven hundred", "seven hundred and one", "seven hundred and two", "seven hundred and three", "seven hundred and four", "seven hundred and five", "seven hundred and six", "seven hundred and seven", "seven hundred and eight", "seven hundred and nine", "seven hundred and ten", "seven hundred and eleven", "seven hundred and twelve", "seven hundred and thirteen", "seven hundred and fourteen", "seven hundred and fifteen", "seven hundred and sixteen", "seven hundred and seventeen", "seven hundred and eighteen", "seven hundred and nineteen", "seven hundred and twenty", "seven hundred and twenty-one", "seven hundred and twenty-two", "seven hundred and twenty-three", "seven hundred and twenty-four", "seven hundred and twenty-five", "seven hundred and twenty-six", "seven hundred and twenty-seven", "seven hundred and twenty-eight", "seven hundred and twenty-nine", "seven hundred and thirty", "seven hundred and thirty-one", "seven hundred and thirty-two", "seven hundred and thirty-three", "seven hundred and thirty-four", "seven hundred and thirty-five", "seven hundred and thirty-six", "seven hundred and thirty-seven", "seven hundred and thirty-eight", "seven hundred and thirty-nine", "seven hundred and forty", "seven hundred and forty-one", "seven hundred and forty-two", "seven hundred and forty-three", "seven hundred and forty-four", "seven hundred and forty-five", "seven hundred and forty-six", "seven hundred and forty-seven", "seven hundred and forty-eight", "seven hundred and forty-nine", "seven hundred and fifty", "seven hundred and fifty-one", "seven hundred and fifty-two", "seven hundred and fifty-three", "seven hundred and fifty-four", "seven hundred and fifty-five", "seven hundred and fifty-six", "seven hundred and fifty-seven", "seven hundred and fifty-eight", "seven hundred and fifty-nine", "seven hundred and sixty", "seven hundred and sixty-one", "seven hundred and sixty-two", "seven hundred and sixty-three", "seven hundred and sixty-four", "seven hundred and sixty-five", "seven hundred and sixty-six", "seven hundred and sixty-seven", "seven hundred and sixty-eight", "seven hundred and sixty-nine", "seven hundred and seventy", "seven hundred and seventy-one", "seven hundred and seventy-two", "seven hundred and seventy-three", "seven hundred and seventy-four", "seven hundred and seventy-five", "seven hundred and seventy-six", "seven hundred and seventy-seven", "seven hundred and seventy-eight", "seven hundred and seventy-nine", "seven hundred and eighty", "seven hundred and eighty-one", "seven hundred and eighty-two", "seven hundred and eighty-three", "seven hundred and eighty-four", "seven hundred and eighty-five", "seven hundred and eighty-six", "seven hundred and eighty-seven", "seven hundred and eighty-eight", "seven hundred and eighty-nine", "seven hundred and ninety", "seven hundred and ninety-one", "seven hundred and ninety-two", "seven hundred and ninety-three", "seven hundred and ninety-four", "seven hundred and ninety-five", "seven hundred and ninety-six", "seven hundred and ninety-seven", "seven hundred and ninety-eight", "seven hundred and ninety-nine", "eight hundred", "eight hundred and one", "eight hundred and two", "eight hundred and three", "eight hundred and four", "eight hundred and five", "eight hundred and six", "eight hundred and seven", "eight hundred and eight", "eight hundred and nine", "eight hundred and ten", "eight hundred and eleven", "eight hundred and twelve", "eight hundred and thirteen", "eight hundred and fourteen", "eight hundred and fifteen", "eight hundred and sixteen", "eight hundred and seventeen", "eight hundred and eighteen", "eight hundred and nineteen", "eight hundred and twenty", "eight hundred and twenty-one", "eight hundred and twenty-two", "eight hundred and twenty-three", "eight hundred and twenty-four", "eight hundred and twenty-five", "eight hundred and twenty-six", "eight hundred and twenty-seven", "eight hundred and twenty-eight", "eight hundred and twenty-nine", "eight hundred and thirty", "eight hundred and thirty-one", "eight hundred and thirty-two", "eight hundred and thirty-three", "eight hundred and thirty-four", "eight hundred and thirty-five", "eight hundred and thirty-six", "eight hundred and thirty-seven", "eight hundred and thirty-eight", "eight hundred and thirty-nine", "eight hundred and forty", "eight hundred and forty-one", "eight hundred and forty-two", "eight hundred and forty-three", "eight hundred and forty-four", "eight hundred and forty-five", "eight hundred and forty-six", "eight hundred and forty-seven", "eight hundred and forty-eight", "eight hundred and forty-nine", "eight hundred and fifty", "eight hundred and fifty-one", "eight hundred and fifty-two", "eight hundred and fifty-three", "eight hundred and fifty-four", "eight hundred and fifty-five", "eight hundred and fifty-six", "eight hundred and fifty-seven", "eight hundred and fifty-eight", "eight hundred and fifty-nine", "eight hundred and sixty", "eight hundred and sixty-one", "eight hundred and sixty-two", "eight hundred and sixty-three", "eight hundred and sixty-four", "eight hundred and sixty-five", "eight hundred and sixty-six", "eight hundred and sixty-seven", "eight hundred and sixty-eight", "eight hundred and sixty-nine", "eight hundred and seventy", "eight hundred and seventy-one", "eight hundred and seventy-two", "eight hundred and seventy-three", "eight hundred and seventy-four", "eight hundred and seventy-five", "eight hundred and seventy-six", "eight hundred and seventy-seven", "eight hundred and seventy-eight", "eight hundred and seventy-nine", "eight hundred and eighty", "eight hundred and eighty-one", "eight hundred and eighty-two", "eight hundred and eighty-three", "eight hundred and eighty-four", "eight hundred and eighty-five", "eight hundred and eighty-six", "eight hundred and eighty-seven", "eight hundred and eighty-eight", "eight hundred and eighty-nine", "eight hundred and ninety", "eight hundred and ninety-one", "eight hundred and ninety-two", "eight hundred and ninety-three", "eight hundred and ninety-four", "eight hundred and ninety-five", "eight hundred and ninety-six", "eight hundred and ninety-seven", "eight hundred and ninety-eight", "eight hundred and ninety-nine", "nine hundred", "nine hundred and one", "nine hundred and two", "nine hundred and three", "nine hundred and four", "nine hundred and five", "nine hundred and six", "nine hundred and seven", "nine hundred and eight", "nine hundred and nine", "nine hundred and ten", "nine hundred and eleven", "nine hundred and twelve", "nine hundred and thirteen", "nine hundred and fourteen", "nine hundred and fifteen", "nine hundred and sixteen", "nine hundred and seventeen", "nine hundred and eighteen", "nine hundred and nineteen", "nine hundred and twenty", "nine hundred and twenty-one", "nine hundred and twenty-two", "nine hundred and twenty-three", "nine hundred and twenty-four", "nine hundred and twenty-five", "nine hundred and twenty-six", "nine hundred and twenty-seven", "nine hundred and twenty-eight", "nine hundred and twenty-nine", "nine hundred and thirty", "nine hundred and thirty-one", "nine hundred and thirty-two", "nine hundred and thirty-three", "nine hundred and thirty-four", "nine hundred and thirty-five", "nine hundred and thirty-six", "nine hundred and thirty-seven", "nine hundred and thirty-eight", "nine hundred and thirty-nine", "nine hundred and forty", "nine hundred and forty-one", "nine hundred and forty-two", "nine hundred and forty-three", "nine hundred and forty-four", "nine hundred and forty-five", "nine hundred and forty-six", "nine hundred and forty-seven", "nine hundred and forty-eight", "nine hundred and forty-nine", "nine hundred and fifty", "nine hundred and fifty-one", "nine hundred and fifty-two", "nine hundred and fifty-three", "nine hundred and fifty-four", "nine hundred and fifty-five", "nine hundred and fifty-six", "nine hundred and fifty-seven", "nine hundred and fifty-eight", "nine hundred and fifty-nine", "nine hundred and sixty", "nine hundred and sixty-one", "nine hundred and sixty-two", "nine hundred and sixty-three", "nine hundred and sixty-four", "nine hundred and sixty-five", "nine hundred and sixty-six", "nine hundred and sixty-seven", "nine hundred and sixty-eight", "nine hundred and sixty-nine", "nine hundred and seventy", "nine hundred and seventy-one", "nine hundred and seventy-two", "nine hundred and seventy-three", "nine hundred and seventy-four", "nine hundred and seventy-five", "nine hundred and seventy-six", "nine hundred and seventy-seven", "nine hundred and seventy-eight", "nine hundred and seventy-nine", "nine hundred and eighty", "nine hundred and eighty-one", "nine hundred and eighty-two", "nine hundred and eighty-three", "nine hundred and eighty-four", "nine hundred and eighty-five", "nine hundred and eighty-six", "nine hundred and eighty-seven", "nine hundred and eighty-eight", "nine hundred and eighty-nine", "nine hundred and ninety", "nine hundred and ninety-one", "nine hundred and ninety-two", "nine hundred and ninety-three", "nine hundred and ninety-four", "nine hundred and ninety-five", "nine hundred and ninety-six", "nine hundred and ninety-seven", "nine hundred and ninety-eight", "nine hundred and ninety-nine")
  with tqdm(count(), unit=" attempts") as tq:
    T, proc, vm, join, grb, ns = {0}, Process(), virtual_memory, "".join, getrandbits, naturalsize
    pmi, pmp, vmt = proc.memory_info, proc.memory_percent, vm().total
    s = pb = p.replace(" ", "").lower() + "and" # don't repeat adding the "and" for every `t = `
    for i in tq:
      if i%100000 == 0:
        av = vm().available / vmt
        tq.set_description(f"{ns(pmi().rss)} used ({pmp():.2f}% used, {av:.2%} free) ")
        if av < 0.3 and pmp()>10: # if less than 30% free and using more than 10%, cleanup
          print(f"\rOnly {av:.2%} of memory left, clearing cache.", end="")
          T.clear() # would like to retain as much of this as possible, but rn we don't
          gc.collect()
      t = pb + join(f"{as_word[sc]}{c}{'s'*(sc != 1)}" for c,sc in zip("abcdefghijklmnopqrstuvwxyz", map(s.count, "abcdefghijklmnopqrstuvwxyz")))
      if s == t:
        return f"""{p} {", ".join(f'''{"and " * (c == "z")}{as_word[sc]} {c}{"'s" * (sc != 1)}''' for c,sc in zip("abcdefghijklmnopqrstuvwxyz", map(s.count, "abcdefghijklmnopqrstuvwxyz")))}."""
      if hash(t) in T: # pick random variation, collision is fine as s != t, and this makes T ~8x smaller
        t = join(c * max(1, s.count(c) + (grb(3) - 4)*(grb(1) == 0)) for c in "abcdefghijklmnopqrstuvwxyz")
      T.add(hash(t))
      s = t

if __name__ == "__main__":
  print("Self-enumerating pangram (\"autogram\") generator.")
  print("Based on https://codegolf.stackexchange.com/a/165333 but significantly faster and full British English; try pypy!")
  print(f"Total memory: {naturalsize(virtual_memory().total)} (of which {naturalsize(virtual_memory().available)} ({virtual_memory().available / virtual_memory().total:.2%}) is available)")
  print(f"Idle memory use: {naturalsize(Process().memory_info().rss)} ({Process().memory_percent():.2f}%)")
  pg = autogram(input("Figure out the autogram of: "))
  print()
  with open("./autograms.txt", "a", encoding="utf8", newline="\n") as o:
    o.write(f"{pg}\n\n")
  print(pg)
