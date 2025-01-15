from pathlib import Path
from datetime import date, datetime 
from functools import reduce 
from dateutil.relativedelta import relativedelta 
import pandas as pd 
import time 
import csv
CR, LF, SP, PER, BAR, UNDER = "\r\n /-_"
COLON, SEMICOLON, COMMA, DOT, SQ, DQ = ":;,.'\""
EQ, PLUS, MINUS, ASTA, SLASH = "=+-*/"
AR_LEFT, AR_BOTTOM, AR_TOP, AR_RIGHT = "←↓↑→"
TILDE, EXCLAMATION, ATMARD, SHARP, DOLLAR, PERCENT, CARET, AMPERSAND, PIPE = "~!@#$%^&|"
PAREN, BRACES, BRACKETS = "(),{},[]".split(COMMA)
log = print 
def join(*s, glue=SP, func=str): return glue.join(func(x) for x in s)
def sand(s, a, b=None): return join(*(a, s, a if b is None else b), glue="")
def comma(*s, **a): return join(*s, glue=COMMA, **a)
def comma_s(*s, **a): return join(*s, glue=f"{COMMA}{SP}", **a)
def sq(s, **a): return sand(s, SQ, **a)
def dq(s, **a): return sand(s, DQ, **a)
def paren(s, **a): return sand(s, *PAREN, **a)
def braces(s, **a): return sand(s, *BRACES, **a)
def brackets(s, **a): return sand(s, *BRACKETS, **a)
def per(*s, **a): return join(*s, glue=PER, **a)
def bar(*s, **a): return join(*s, glue=BAR, **a)
def under(*s, **a): return join(*s, glue=UNDER, **a)
def and_(*s, func=paren, **a): return join(*s, glue=" and ", func=func, **a) 
def  or_(*s, func=paren, **a): return join(*s, glue= " or ", func=func, **a) 
def ymd(d, format_spec="%Y%m%d"): return format(d, format_spec)
def num(n, format_spec=","): return format(n, format_spec)
def ymds_of(*d, format_spec="%Y%m%d"): return bar(*d, func=lambda d: ymd(d, format_spec))
def step_of(a, b, format_spec=","): 
  if type(a) is int and type(b) is int:
    nn = (a, b) 
  else: 
    nn = (a + 1, len(b))
  return per(*nn, func=lambda n: num(n, format_spec))

def stay(*s, end="", mask=60, **a):
  log(CR, end="")
  log(*s, SP*mask, end=end, **a)

if False: # test code:
  s, a, b, c = "sabc" 
  d = date.today() 
  st = d + relativedelta(day=1)
  ed = d + relativedelta(day=31)
  dd = (st, ed)
  n = 12345
  def disp(func=lambda x:x): 
    specials = {
      "\r": "\\r", 
      "\n": "\\n", 
    }
    return lambda s: func(specials.get(s, s))
  log(comma_s(*"CR, LF, SP, PER, BAR, UNDER".split(", ")), EQ, comma_s(CR, LF, SP, PER, BAR, UNDER, func=disp(dq)))
  log(comma_s(*"COLON, SEMICOLON, COMMA, DOT, SQ, DQ".split(", ")), EQ, comma_s(COLON, SEMICOLON, COMMA, DOT, SQ, DQ, func=disp(dq)))
  log(comma_s(*"EQ, PLUS, MINUS, ASTA, SLASH".split(", ")), EQ, comma_s(EQ, PLUS, MINUS, ASTA, SLASH, func=disp(dq)))
  log(comma_s(*"AR_LEFT, AR_BOTTOM, AR_TOP, AR_RIGHT".split(", ")), EQ, comma_s(AR_LEFT, AR_BOTTOM, AR_TOP, AR_RIGHT, func=disp(dq)))
  log(comma_s(*"TILDE, EXCLAMATION, ATMARD, SHARP, DOLLAR, PERCENT, CARET, AMPERSAND, PIPE".split(", ")), EQ, comma_s(TILDE, EXCLAMATION, ATMARD, SHARP, DOLLAR, PERCENT, CARET, AMPERSAND, PIPE, func=disp(dq)))
  log(comma_s(*"PAREN,BRACES,BRACKETS".split(COMMA)), EQ, comma_s(PAREN, BRACES, BRACKETS, func=disp(dq)))
  log(f"join{paren(comma_s(a, b, c, func=sq))}", EQ, dq(join(a, b, c)))
  log(f"comma{paren(comma_s(a, b, c, func=sq))}", EQ, dq(comma(a, b, c)))
  log(f"comma_s{paren(comma_s(a, b, c, func=sq))}", EQ, dq(comma_s(a, b, c)))
  log(f"par{paren(comma_s(a, b, c, func=sq))}", EQ, dq(per(a, b, c)))
  log(f"bar{paren(comma_s(a, b, c, func=sq))}", EQ, dq(bar(a, b, c)))
  log(f"under{paren(comma_s(a, b, c, func=sq))}", EQ, dq(under(a, b, c)))
  log(f"and_{paren(comma_s(a, b, c, func=sq))}", EQ, dq(and_(a, b, c)))
  log(f" or_{paren(comma_s(a, b, c, func=sq))}", EQ, dq( or_(a, b, c)))
  log(f"num{paren(comma_s(n))}", EQ, dq(num(n)))
  log(f"ymd{paren(comma_s(d))}", EQ, dq(ymd(d)))
  log(f"ymds_of{paren(comma_s(*dd))}", EQ, dq(ymds_of(*dd)))
  log(f"step_of{paren(comma_s(n // 10, n))}", EQ, dq(step_of(n // 10 , n)))
  log(f"step_of{paren(comma_s(0, f'range({n})'))}", EQ, dq(step_of(0, range(n))))

  n = 100
  sleep = 2 / n 
  for i in range(n):
    end = "" if i < n - 1 else LF 
    stay(num(i), "doing...", end=end)
    time.sleep(sleep)
  log(num(n), "done!")



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
