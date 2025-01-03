from pathlib import Path 
import time 
from datetime import date, datetime 
from functools import reduce 
from dateutil.relativedelta import relativedelta

CR = "\r"
LF = "\n"
SP = " "
SQ = "'"
DQ = '"'
log = print 
def stay(*s, end="", func=str, **a):
  log(CR, end="") 
  log(*s, end=end, **a)

def join(*s, glue=SP, func=str): return glue.join(func(x) for x in s)
def per   (*s, **a): return join(*s, glue="/", **a)
def under (*s, **a): return join(*s, glue="_", **a)
def hyphen(*s, **a): return join(*s, glue="-", **a)
def num(n): return f"{n:,}"
def ymd(n, format="%Y%m%d"): return f"{n:{format}}"
def ymds_of(*d, format="%Y%m%d"): 
  return hyphen(*list(ymd(x, format=format) for x in d))
def step_of(a, b, **ka): 
  if type(a) is int and type(b) is int: 
    nn = (a, b) 
  else:
    nn = (a + 1, len(b))
  return per(*nn, func=num, **ka)

### test code:
# a, b, c = "a", "b", "c"
# s = (a, b, c)
# d = date.today()
# n = 12345
# dd = (d, d + relativedelta(day=31))
# nn = 1425, 25000
# log(f"join({join(*list(f'{SQ}{x}{SQ}' for x in s), glue=', ')}) → {DQ}{join(*s)}{DQ}")
# log(f"per({join(*list(f'{SQ}{x}{SQ}' for x in s), glue=', ')}) → {DQ}{per(*s)}{DQ}")
# log(f"under({join(*list(f'{SQ}{x}{SQ}' for x in s), glue=', ')}) → {DQ}{under(*s)}{DQ}")
# log(f"hyphen({join(*list(f'{SQ}{x}{SQ}' for x in s), glue=', ')}) → {DQ}{hyphen(*s)}{DQ}")
# log(f"num({join(*list(f'{x}' for x in [n]), glue=', ')}) → {DQ}{num(n)}{DQ}")
# log(f"ymd({join(*list(f'{x}' for x in [d]), glue=', ')}) → {DQ}{ymd(d)}{DQ}")
# log(f"ymds_of({join(*list(f'{x}' for x in dd), glue=', ')}) → {DQ}{ymds_of(*dd)}{DQ}")
# log(f"step_of({join(*list(f'{x}' for x in nn), glue=', ')}) → {DQ}{step_of(*nn)}{DQ}")
# log(f"step_of({join(*list(f'{x}' for x in (0, f'range({n})')), glue=', ')}) → {DQ}{step_of(0, range(n))}{DQ}")

def sand(s, a, b=None): return f"{a}{s}{a if b is None else b}"
def sq(s): return sand(s, SQ)
def dq(s): return sand(s, DQ)
def paren(s): return sand(s, "(", ")")
def braces(s): return sand(s, "(", "}")
def brackets(s): return sand(s, "[", "]")
def comma(*ss, space=True, lf=False): 
  return join(*ss, glue=f",{SP if space else ''}{LF if lf else ''}")
def and_(*ss): return join(*list(paren(x) for x in ss), glue=" and ")
def  or_(*ss): return join(*list(paren(x) for x in ss), glue= " or ")
### test code:
# s, a, b, c = "s", "a", "b", "c"
# ss = list(f"{x}={x}{x}" for x in (a, b, c))
# log(f"sand({comma(*list(sq(x) for x in [s, a, b]))}) → {dq(sand(s, a, b))}")
# log(f"sq({comma(*list(sq(x) for x in [s]))}) → {dq(sq(s))}")
# log(f"dq({comma(*list(sq(x) for x in [s]))}) → {sq(dq(s))}")
# log(f"paren({comma(*list(sq(x) for x in [s]))}) → {dq(paren(s))}")
# log(f"braces({comma(*list(sq(x) for x in [s]))}) → {dq(braces(s))}")
# log(f"brackets({comma(*list(sq(x) for x in [s]))}) → {dq(brackets(s))}")
# log(f"and_({comma(*list(sq(x) for x in ss))}) → {dq(and_(*ss))}")
# log(f" or_({comma(*list(sq(x) for x in ss))}) → {dq( or_(*ss))}")
# f""" 
# select {comma(
#   *list(f"item_{x}" for x in (a, b, c)), 
#   lf=True
# )} from table_one
# """.split(LF)

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
