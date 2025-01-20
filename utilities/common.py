from pathlib import Path 
from datetime import date, datetime 
from dateutil.relativedelta import relativedelta 
from functools import reduce 
import time, csv
import pandas as pd 

CR, LF, SP, PER, BAR, UNDER = "\r\n /-_"
COMMA, PERIOD, LT, GT = ",.<>"
SQ, DQ, EXCLAMATION, AT, SHARP = "'\"!@#" 
DOLLAR, PERCENT, CARET, AMP, ASTA, = "$%^&*"
AR_LEFT, AR_DOWN, AR_TOP, AR_RIGHT = "←↓↑→"
EQ, PLUS = "=+"
PAREN, BRACES, BRACKETS = "(),{},[]".split(COMMA)
COMMA_S = f"{COMMA}{SP}"
CRR, LFF = "\\r,\\n".split(COMMA)

log = print 
def stay(*s, end="", mask=60, **a): 
  log(CR, end="") 
  log(*s, SP*mask, end=end, **a)
def join(*s, glue=SP, func=str): return glue.join(func(x) for x in s) 
def sand(s, a, b=None): return join(a, s, a if b is None else b, glue="")
def sq(s, **a): return sand(s, SQ)
def dq(s, **a): return sand(s, DQ)
def paren(s, **a): return sand(s, *PAREN)
def braces(s, **a): return sand(s, *BRACES)
def brackets(s, **a): return sand(s, *BRACKETS)
def comma(*s, **a): return join(*s, glue=COMMA, **a)
def comma_s(*s, **a): return join(*s, glue=COMMA_S, **a)
def per(*s, **a): return join(*s, glue=PER, **a)
def bar(*s, **a): return join(*s, glue=BAR, **a)
def under(*s, **a): return join(*s, glue=UNDER, **a)
def ymd(d, spec="%Y%m%d"): return format(d, spec)
def num(n, spec=","): return format(n, spec)
def ymds_of(*d, spec="%Y%m%d", glue=BAR, **a): return join(*d, glue=glue, func=lambda x:ymd(x, spec), **a) 
def step_of(a, b, spec=",", glue=PER, **aa):
  if type(a) is int and type(b) is int: 
    nn = (a, b) 
  else: 
    nn = (a + 1, len(b)) 
  return join(*nn, glue=glue, func=lambda x:num(x, spec=spec), **aa)

if False: 
  s, a, b, c = "sabc"
  d = date.today() 
  n = 12345
  dd = list(d + relativedelta(day=x) for x in (1, 31))
  log(sq(s), dq(s), paren(s), braces(s), brackets(s))
  log(ymds_of(*dd))
  log(step_of(n//100, n))
  log(step_of(n//100, range(n)))

if False: # test code: 
  todo = range(100)
  done = 0 
  for i, _ in enumerate(todo):
    end = "" if i < len(arr) - 1 else LF 
    stay(step_of(i, todo), "doing...", end=end)
    done += 1
    time.sleep(2 / len(todo))
  log(step_of(done, len(todo)), "done!")

def fullpath(*path) -> Path: 
  root = Path(".") 
  fn = reduce(lambda a, b: Path(a) / Path(b), path, root)
  return fn.resolve().absolute()
def ensure_dir(*path, parents=True, exist_ok=True, **a) -> Path: 
  dn = fullpath(*path) 
  dn.mkdir(parents=parents, exist_ok=exist_ok, **a) 
  return dn
def ensure_file(*path, **a) -> Path: 
  fn = fullpath(*path) 
  ensure_dir(fn.parent)
  if not fn.exists(): 
    fn.touch()  
  return fn 

if False: # test code: 
  root = fullpath(".")
  fn = fullpath("test", "check", "check.txt")
  log(ensure_file(fn))
  with fn.open(mode="w") as f:
    f.write("check!!")

def fiscal_year_of(day=date.today) -> date: 
  years = 0 if day > day + relativedelta(month=4) else -1
  st =  day + relativedelta(month=4, years=years)
  return (st, st + relativedelta(years=1, days=-1))
def months_of(st: date, ed: date) -> list[date, date]: 
  st = st + relativedelta(day=1)
  ed = ed + relativedelta(day=31)
  diff = relativedelta(ed, st).months + 1 
  first_days = list(st + relativedelta(months=x) for x in range(diff)) 
  return list((x, x + relativedelta(months=1, days=-1)) for x in first_days)

if False: # test code: 
  d = date.today() 
  st = d + relativedelta(day=1)
  ed = st + relativedelta(years=1, days=-1)
  months = months_of(st, ed)
  for st, _ in months:
    log(st, AR_RIGHT, fiscal_year_of(st))

SJIS = "cp931"
UTF8 = "utf-8" 
UTF8SIG = "utf-8_sig"
def load_csv(*path, encoding=UTF8SIG, **a): 
  fn = fullpath(*path) 
  df = pd.read_csv(fn, encoding=encoding, **a) 
  return df 
def save_csv(df, *path, encoding=UTF8SIG, quoting=csv.QUOTE_ALL, index=False, **a) -> Path: 
  fn = fullpath(*path)
  df.to_csv(fn, encoding=encoding, quoting=quoting, index=index, **a) 
  return fn 

if False: # test code: 
  from random import randint 
  df = pd.DataFrame(dict(
    id=x, 
    value=randint(500, 1000), 
  ) for x in range(100))
  fn = ensure_file("test", "save_csv_check", "check.csv")
  log(dq(save_csv(df, fn)))
  log(load_csv(fn))

class dotdict(dict):
  def __setattr__(self, name, value):
    self[name] = value 
  def __getattr__(self, name): 
    return self.get(name)

if False: # test code; 
  dd = dotdict(dict(a="aa", b="bb"))
  dd.b = "bbb" 
  dd.c = "cccc" 
  dd 

