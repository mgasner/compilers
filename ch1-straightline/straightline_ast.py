class Stm(object): pass

class CompoundStm(Stm):
  def __init__(self, stm1, stm2):
    self.stm1 = stm1
    self.stm2 = stm2

class AssignStm(Stm):
  def __init__(self, id, exp):
    self.id = id
    self.exp = exp

class PrintStm(Stm):
  def __init__(self, exps):
    self.exps = exps

class Exp(object):
  pass

class IdExp(Exp):
  def __init__(self, id):
    self.id = id

class NumExp(Exp):
  def __init__(self, num):
    self.num = num
    
class OpExp(Exp):
  def __init__(self, left, oper, right):
    self.left = left
    self.oper = oper
    self.right = right
  Plus = 1
  Minus = 2
  Times = 3
  Div = 4
    
class EseqExp(Exp):
  def __init__(self, stm, exp):
    self.stm = stm
    self.exp = exp

class ExpList(object):
  pass

class PairExpList(ExpList):
  def __init__(self, head, tail):
    self.head = head
    self.tail = tail

class LastExpList(ExpList):
  def __init__(self, head):
    self.head = head
