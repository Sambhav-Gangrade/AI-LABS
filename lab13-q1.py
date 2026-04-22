from itertools import product

class Expr:
    def evaluate(self, values):
        pass

class Symbol(Expr):
    def __init__(self, name):
        self.name = name
    def evaluate(self, values):
        return values[self.name]

class Not(Expr):
    def __init__(self, operand):
        self.operand = operand
    def evaluate(self, values):
        return not self.operand.evaluate(values)

class And(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def evaluate(self, values):
        return self.left.evaluate(values) and self.right.evaluate(values)

class Or(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def evaluate(self, values):
        return self.left.evaluate(values) or self.right.evaluate(values)

class Implies(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def evaluate(self, values):
        return (not self.left.evaluate(values)) or self.right.evaluate(values)

class Iff(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def evaluate(self, values):
        return self.left.evaluate(values) == self.right.evaluate(values)

def print_truth_table(expr, variables, title):
    print("\n", title)
    for v in variables:
        print(v.name, end=" ")
    print("| R")
    for values in product([False, True], repeat=len(variables)):
        val_dict = dict(zip([v.name for v in variables], values))
        for v in values:
            print('T' if v else 'F', end=" ")
        print("|", 'T' if expr.evaluate(val_dict) else 'F')

P = Symbol('P')
Q = Symbol('Q')
R = Symbol('R')

expr1 = Implies(Not(P), Q)
expr2 = And(Not(P), Not(Q))
expr3 = Or(Not(P), Not(Q))
expr4 = Implies(Not(P), Not(Q))
expr5 = Iff(Not(P), Not(Q))
expr6 = And(Or(P, Q), Implies(Not(P), Q))
expr7 = Implies(Or(P, Q), Not(R))
expr8 = Iff(Implies(Or(P, Q), Not(R)), Implies(And(Not(P), Not(Q)), Not(R)))
expr9 = Implies(And(Implies(P, Q), Implies(Q, R)), Implies(Q, R))
expr10 = Implies(Implies(P, Or(Q, R)), And(Not(P), And(Not(Q), Not(R))))

print_truth_table(expr1, [P, Q], "~P -> Q")
print_truth_table(expr2, [P, Q], "~P ∧ ~Q")
print_truth_table(expr3, [P, Q], "~P ∨ ~Q")
print_truth_table(expr4, [P, Q], "~P -> ~Q")
print_truth_table(expr5, [P, Q], "~P <-> ~Q")
print_truth_table(expr6, [P, Q], "(P ∨ Q) ∧ (~P -> Q)")
print_truth_table(expr7, [P, Q, R], "(P ∨ Q) -> ~R")
print_truth_table(expr8, [P, Q, R], "((P ∨ Q)->~R) <-> ((~P∧~Q)->~R)")
print_truth_table(expr9, [P, Q, R], "((P->Q)∧(Q->R))->(Q->R)")
print_truth_table(expr10, [P, Q, R], "((P->(Q∨R)) -> (~P∧~Q∧~R))") 