# %%
from pathlib import Path 
import time 
from datetime import date, datetime 
from functools import reduce 
from dateutil.relativedelta import relativedelta
import pandas as pd 
import csv 

log = print 
CR = "\r"
LF = "\n"
SP = " "
SQ = "'"
DQ = '"'
PER = "/"
BAR = "-"
UNDER = "_"
COMMA = ","
DOT = "."
def join(*s, glue=SP, func=str): return glue.join(list(func(x) for x in s))
def per(*s, glue=PER, **a): return join(*s, glue=glue, **a)
def bar(*s, glue=BAR, **a): return join(*s, glue=glue, **a)
def under(*s, glue=UNDER, **a): return join(*s, glue=glue, **a)
def comma(*s, glue=COMMA, **a): return join(*s, glue=glue, **a)
def sand(s, a, b=None): return join(*(a, s, a if b is None else b), glue="")
def sq(s): return sand(s, SQ)
def dq(s): return sand(s, DQ)
def paren(s): return sand(s, *"()")
def braces(s): return sand(s, *"{}")
def brackets(s): return sand(s, *"[]")
def and_(*s): return join(*s, glue=" and ", func=paren)
def  or_(*s): return join(*s, glue= " or ", func=paren)
def ymd(d, format="%Y%m%d"): return f"{d:{format}}"
def num(n, format=","): return f"{n:{format}}"
def ymds_of(*d, format="%Y%m%d"): return bar(*(ymd(x, format) for x in d))
def step_of(a, b): 
  if type(a) is int and type(b) is int: 
    nn = (a, b) 
  else:
    nn = (a + 1, len(b))
  return per(*nn, func=num)
## test code:
# ss = "sabc"
# s, a, b, c = ss
# n = 1000
# dd = date(2025, 1, 1), date(2025, 1, 31)
# d, _ = dd 
# nn = 1200, 5000
# log(f"join({comma(*ss)}) → {dq(join(*ss))}")
# log(f"per({comma(*ss)}) → {dq(per(*ss))}")
# log(f"bar({comma(*ss)}) → {dq(bar(*ss))}")
# log(f"under({comma(*ss)}) → {dq(under(*ss))}")
# log(f"comma({comma(*ss)}) → {dq(comma(*ss))}")
# log(f"sq({comma(s)}) → {dq(sq(s))}")
# log(f"dq({comma(s)}) → {sq(dq(s))}")
# log(f"paren({comma(s)}) → {dq(paren(s))}")
# log(f"braces({comma(s)}) → {dq(braces(s))}")
# log(f"brackets({comma(s)}) → {dq(brackets(s))}")
# log(f"and_({comma(*ss)}) → {dq(and_(*ss))}")
# log(f" or_({comma(*ss)}) → {dq( or_(*ss))}")
# log(f"ymd({comma(d)}) → {dq(ymd(d))}")
# log(f"ymd({comma(d)},format='%y%m%d') → {dq(ymd(d, format='%y%m%d'))}")
# log(f"num({comma(n)}) → {dq(num(n))}")
# log(f"num({comma(n)},format=',.2f') → {dq(num(n, format=',.2f'))}")
# log(f"ymds_of({comma(*dd)}) → {dq(ymds_of(*dd))}")
# log(f"ymds_of({comma(*dd)},format='%y%m%d') → {dq(ymds_of(*dd, format='%y%m%d'))}")
# log(f"step_of(1000,15000) → {dq(step_of(1000, 15000))}")
# log(f"step_of(0,range(2500)) → {dq(step_of(0, range(2500)))}")


def stay(*s, end="", mask=60, **a): 
  log(CR, end="")
  log(*s, SP*mask, end=end, **a)
## test code: 
# n = 10
# ls = range(n)
# for i in ls:
#   end = "" if i < len(ls) - 1 else LF 
#   stay(step_of(i, ls), "processing...", end=end)
#   time.sleep(.5)
# log(num(n), "done!")

def fullpath(*path): 
  root = Path(".")
  full = reduce(lambda a, b:Path(a) / Path(b), path, root)
  return full.resolve().absolute() 
def ensure_dir(*path, **a): 
  dirname = fullpath(*path) 
  dirname.mkdir(parents=True, exist_ok=True, **a)
  return dirname 

def resetfile(filename: Path, content="", mode="w", **a):
  filename = fullpath(filename)
  with filename.open(mode=mode, **a) as f: 
    f.write(content)
  return filename

def quoter_start_of(day=date.today()):
  st = day + relativedelta(month=4, day=1)
  if st > day: 
    st += relativedelta(years=-1)
  return st 
def quoter_end_of(day=date.today()):
  st = quoter_start_of(day)
  return st + relativedelta(years=1, days=-1)
def quoter_period_of(day=date.today()):
  return (quoter_start_of(day), quoter_end_of(day))

def month_start_of(day=date.today()): 
  return day + relativedelta(day=1)
def month_end_of(day=date.today()): 
  return day + relativedelta(day=31)
def month_period_of(day=date.today()):
  return (month_start_of(day), month_end_of(day))
def month_periods_of(days):
  st, ed = days 
  st = month_start_of(st)
  ed = month_end_of(ed)
  months = relativedelta(ed, st).months + 1 
  starts = list(st + relativedelta(months=x) for x in range(months))
  return list(month_period_of(x) for x in starts)

### test code:
# days = (date(2024, 1, 1), date(2024, 12, 31))
# day = days[0]
# log(f"quoter_period_of({day}) → {quoter_period_of(day)}")
# log(f"month_period_of({day}) → {month_period_of(day)}")
# log(f"""month_periods_of({days}) → {LF}{join(
#   *list(hyphen(*list(ymd(d) for d in x)) for x in month_periods_of(days)), 
#   glue=LF,  
# )}""")

UTF8SIG = "utf-8_sig"
def load_csv(filename, encoding=UTF8SIG, **a):
  filename = fullpath(filename) 
  df = pd.read_csv(filename, encoding=encoding, **a) 
  return df 
def save_csv(df, filename, encoding=UTF8SIG, quoting=csv.QUOTE_ALL, index=False, **a): 
  filename = fullpath(filename) 
  df.to_csv(filename, encoding=encoding, quoting=quoting, index=index, **a)
  return filename 

### test code: 
# from random import randint 
# df = pd.DataFrame(dict(
#   id=x, 
#   name=f"name of {x:03}", 
#   subname=f"subname of {x:03}",
#   price=randint(500, 4500) 
# ) for x in range(1, 101))
# fn = fullpath("test") / "test.csv"
# save_csv(df, fn)
# load_csv(fn)

class dotdict(dict):
  def __setattr__(self, name, value):
    self[name] = value 
  def __getattr__(self, name):
    return self.get(name)
