from pathlib import Path
from datetime import date, datetime 
from functools import reduce 
from dateutil.relativedelta import relativedelta 
import pandas as pd 
import time 
import csv

log = print 
CR, LF, SP, SQ, DQ, PER, BAR, UNDER, COMMA, DOT = "\r\n '\"/-_,."
if False: # test
  nn = "CR", "LF", "SP", "SQ", "DQ", "PER", "BAR", "UNDER", "COMMA", "DOT"
  vv = [CR, LF, SP, SQ, DQ, PER, BAR, UNDER, COMMA, DOT]
  for n, v in zip(nn, vv): 
    log(f"{n}: {DQ}{v}{DQ}")


def join(*s, glue=SP, func=str): return glue.join(func(x) for x in s)
def sand(s, a, b=None): return join(*(a, s, a if b is None else b), glue="")
def sq(s): return sand(s, SQ)
def dq(s): return sand(s, DQ)
def per(*s): return join(*s, glue=PER)
def bar(*s): return join(*s, glue=BAR)
def under(*s): return join(*s, glue=UNDER)
def comma(*s): return join(*s, glue=COMMA)
def dot(*s): return join(*s, glue=DOT)
def paren(s): return sand(s, *"()")
def braces(s): return sand(s, *"{}")
def brackets(s): return sand(s, *"[]")
def format(s, format=""): return f"{s:{format}}"
def num(n, format=","): return f"{n:{format}}"
def ymd(d, format="%Y%m%d"): return f"{d:{format}}"
def ymds_of(*d, format="%Y%m%d"): return bar(*(ymd(x, format) for x in d))
def step_of(a, b):
  if type(a) is int and type(b) is int: 
    nn = (a, b) 
  else: 
    nn = (a + 1, len(b))
  return per(*(num(x) for x in nn))
def and_(*s): return join(*s, glue=" and ", func=paren)
def  or_(*s): return join(*s, glue= " or ", func=paren)
if False: # test 

  s, a, b, c = "sabc"
  d = date.today() 
  st = d + relativedelta(day=1)
  ed = d + relativedelta(day=31)
  dd = (st, ed)
  n = 12345
  log(f"sq{paren(comma(*[s]))} → {dq(sq(s))}")
  log(f"dq{paren(comma(*[s]))} → {sq(dq(s))}")
  log(f"per{paren(comma(a, b, c))} → {dq(per(a, b, c))}")
  log(f"bar{paren(comma(a, b, c))} → {dq(bar(a, b, c))}")
  log(f"under{paren(comma(a, b, c))} → {dq(under(a, b, c))}")
  log(f"comma{paren(comma(a, b, c))} → {dq(comma(a, b, c))}")
  log(f"dot{paren(comma(a, b, c))} → {dq(dot(a, b, c))}")
  log(f"paren{paren(comma(*[s]))} → {dq(paren(s))}")
  log(f"braces{paren(comma(*[s]))} → {dq(braces(s))}")
  log(f"brackets{paren(comma(*[s]))} → {dq(brackets(s))}")
  log(f"format{paren(comma(*[s], f'format={SQ}{SQ}'))} → {dq(format(s))}")
  log(f"num{paren(comma(*[n]))} → {dq(num(n))}")
  log(f"num{paren(comma(*[n], f'format={SQ},.02f{SQ}'))} → {dq(num(n, format=',.02f'))}")
  log(f"ymd{paren(comma(*[d]))} → {dq(ymd(d))}")
  log(f"ymd{paren(comma(*[d], f'format={SQ}%y%m%d{SQ}'))} → {dq(ymd(d, format='%y%m%d'))}")
  log(f"ymds_of{paren(comma(*dd))} → {dq(ymds_of(*dd))}")
  log(f"step_of{paren(comma(n//2, n))} → {dq(step_of(n//2, n))}")
  log(f"step_of{paren(comma(0, f'range({n})'))} → {dq(step_of(0, range(n)))}")
  log(f"and_{paren(comma(a, b, c))} → {dq(and_(a, b, c))}")
  log(f" or_{paren(comma(a, b, c))} → {dq( or_(a, b, c))}")

def stay(*s, end="", mask=60, **a):
  log(CR, end="") 
  log(*s, SP*mask, end=end, **a)
if False: # test
  n = 10
  s = 0.1
  ls = range(n) 
  for i in ls:
    end = "" if i < len(ls) - 1 else LF 
    stay(step_of(i, ls), "processing..., end=end", end=end)
    time.sleep(s)
  log(num(len(ls)), "done!")


def fullpath(*path) -> Path:
  root = Path(".")
  full = reduce(lambda a, b: Path(a) / Path(b), path, root)
  return full.resolve().absolute()
def ensure_dir(*path, parents=True, exist_ok=True, **a) -> Path: 
  dirname = fullpath(*path)
  dirname.mkdir(parents=parents, exist_ok=exist_ok, **a)
  return dirname
def resetfile(filename: Path, content="", mode="w", **a):
  filename = fullpath(filename)
  with filename.open(mode=mode, **a) as f: 
    f.write(content)
  return filename

if False: # test 
  fn = ensure_dir("test.", "check") / "reset.txt"
  log(resetfile(fn, content="check!"))

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

if False: # test
  days = (date(2024, 1, 1), date(2024, 12, 31))
  day = days[0]
  log(f"quoter_period_of({day}) → {quoter_period_of(day)}")
  log(f"month_period_of({day}) → {month_period_of(day)}")
  log(f"""month_periods_of({days}) → {LF}{join(
    *list(ymds_of(*x) for x in month_periods_of(days)), 
    glue=LF,  
  )}""")

UTF8SIG = "utf-8_sig"
def load_csv(filename, encoding=UTF8SIG, **a):
  filename = fullpath(filename) 
  df = pd.read_csv(filename, encoding=encoding, **a) 
  return df 
def save_csv(df, filename, encoding=UTF8SIG, quoting=csv.QUOTE_ALL, index=False, **a): 
  filename = fullpath(filename) 
  df.to_csv(filename, encoding=encoding, quoting=quoting, index=index, **a)
  return filename 

if False: ## test code: 
  from random import randint 
  df = pd.DataFrame(dict(
    id=x, 
    name=f"name of {x:03}", 
    subname=f"subname of {x:03}",
    price=randint(500, 4500) 
  ) for x in range(1, 101))
  fn = fullpath("test") / "test.csv"
  save_csv(df, fn)
  load_csv(fn)

class dotdict(dict):
  def __setattr__(self, name, value):
    self[name] = value 
  def __getattr__(self, name):
    return self.get(name)
