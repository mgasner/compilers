from straightline_ast import *

# find the maximum number of args passed to a print statement in the program tree, keeping in mind that print statements can be nested. quick and dirty; not trying to be tidy in recursing down the tree.
def maxargs(prog):
  if isinstance(prog, PrintStm):
    num = 1
    if isinstance(prog.exps, ExpList):
      exp = prog.exps
      while isinstance(exp, PairExpList):
        exp = exp.tail
        num = num + 1
    return max(num, maxargs(prog.exps))      
  elif isinstance(prog, CompoundStm):
    return max(maxargs(prog.stm1), maxargs(prog.stm2))
  elif isinstance(prog, OpExp):
    return max(maxargs(prog.left), maxargs(prog.right))
  elif isinstance(prog, EseqExp):
    return max(maxargs(prog.stm), maxargs(prog.exp))
  elif isinstance(prog, PairExpList):
    return max(maxargs(prog.head), maxargs(prog.tail))
  elif isinstance(prog, AssignStm):
    return maxargs(prog.exp)
  elif isinstance(prog, LastExpList):
    return maxargs(prog.head)
  else:
    return 0

# interp calls the mutually recursive interpStm and interpExp with a new environment
def interp(prog):
  if isinstance(prog, Stm):
    interpStm(prog, Table())
  elif isinstance(prog, Exp):
    interpExp(prog, Table())
  else:
    raise Exception("INTERP -- expected a Stm or Exp", prog)

# returns an updated environment
def interpStm(prog, table):
  if isinstance(prog, CompoundStm):
    table = interpStm(prog.stm1, table)
    return interpStm(prog.stm2, table)
  elif isinstance(prog, AssignStm):
    res, newtable = interpExp(prog.exp, table)
    return newtable.update(prog.id, res)
  elif isinstance(prog, PrintStm):
    if isinstance(prog.exps, ExpList):
      exp = prog.exps
      res, table = interpExp(exp.head, table)
      acc = str(res)
      if isinstance(exp, LastExpList):
        print(acc)
        return table
      exp = exp.tail
      while isinstance(exp, PairExpList):
        res, table = (interpExp(exp.head, table))
        acc = " ".join([acc, str(res)])
        exp = exp.tail
      res, table = interpExp(exp.head, table)
      acc = " ".join([acc, str(res)])
      print(acc)
      return table
    else:
      res, table = interpExp(prog.exps, table)
      print(res)
      return table
  else:
    raise Exception("INTERPSTM -- expected a CompoundStm, AssignStm, or PrintStm", prog)

def interpExp(prog, table):
  if isinstance(prog, IdExp):
    return (table.lookup(prog.id), table)
  elif isinstance(prog, NumExp):
    return (prog.num, table)
  elif isinstance(prog, OpExp):
    lres, table = interpExp(prog.left, table)
    rres, table = interpExp(prog.right, table)
    if prog.oper == OpExp.Plus:
      return (lres + rres, table)
    elif prog.oper == OpExp.Minus:
      return (lres - rres, table)
    elif prog.oper == OpExp.Times:
      return (lres * rres, table)
    elif prog.oper == OpExp.Div:
      return (lres / rres, table)
    else:
      raise Exception("INTERPEXP -- Didn't recognize binop", prog.oper)
  elif isinstance(prog, EseqExp):
    table = interpStm(prog.stm, table)
    return interpExp(prog.exp, table)
  elif isinstance(prog, PairExpList):
    table = interpExp(prog.head, table)
    return interpExp(prog.tail, table)
  elif isinstance(prog, LastExpList):
    return interpExp(prog.head, table)
  else:
    raise Exception("INTERPEXP -- expected a IdExp, NumExp, OpExp, EseqExp, PairExpList, or LastExpList", prog)

## a, b = tuple(a)
    

class Table:
  def __init__(self, id = None, value = None, tail = None):
    if id and value:
      self.id = id
      self.value = value
    if isinstance(tail, Table):
      self.tail = tail    
  def lookup(self, key):
    if self.id == key:
      return self.value
    elif instanceof(self.tail, Table):
      return self.tail.lookup(key)
    else:
      raise Exception("TABLE.LOOKUP -- key not found", key)
  def update(self, key, value):
    return Table(key, value, self)
