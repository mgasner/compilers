import straightline_ast.py

# a := 5 + 3;
# b := (print(a, a - 1), 10 * a);
# print(b);

prog = CompoundStm(AssignStm("a", OpExp(NumExp(5), OpExp.Plus, NumExp(3))), CompoundStm(AssignStm("b", EseqExp(PrintStm(PairExpList(IdExp("a"), LastExpList(OpExp(IdExp("a"), OpExp.Minus, NumExp(1))))), OpExp(NumExp(10), OpExp.Times, IdExp("a")))), PrintStm(LastExpList("b"))))

maxargs(prog)
interp(prog)
