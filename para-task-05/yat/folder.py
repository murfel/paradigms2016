#!/usr/bin/env python3

from yat.printer import *


class ConstantFolder:

    def visit(self, tree):
        tree.accept(self)
        return self.result

    def visit_function_definition(self, func_def):
        args = list(map(self.visit, func_def.function.args))
        body = list(map(self.visit, func_def.function.body))
        self.result = FunctionDefinition(func_def.name,
                                         Function(args, body))

    def visit_conditional(self, cond):
        condition = self.visit(cond.condition)
        if_true = list(map(self.visit, cond.if_true))
        if cond.if_false:
            if_false = list(map(self.visit, cond.if_false))
        else:
            if_false = None
        self.result = Conditional(condition, if_true, if_false)

    def visit_print(self, print_stmt):
        self.result = Print(self.visit(print_stmt.expr))

    def visit_read(self, read):
        self.result = Read(read.name)

    def visit_number(self, num):
        self.result = Number(num.value)

    def visit_reference(self, ref):
        self.result = Reference(ref.name)

    def visit_binary_operation(self, binop):
        lhs = self.visit(binop.lhs)
        rhs = self.visit(binop.rhs)

        if isinstance(lhs, Number) and isinstance(rhs, Number):
            self.result = BinaryOperation(lhs, binop.op, rhs).evaluate(Scope())
        elif ((isinstance(lhs, Number) and lhs == Number(0)
               and isinstance(rhs, Reference) and binop.op == '*') or
              (isinstance(rhs, Number) and rhs == Number(0)
               and isinstance(lhs, Reference) and binop.op == '*') or
              (isinstance(lhs, Reference) and isinstance(rhs, Reference)
               and lhs.name == rhs.name and binop.op == '-')):
            self.result = Number(0)
        else:
            self.result = BinaryOperation(lhs, binop.op, rhs)

    def visit_unary_operation(self, unop):
        expr = self.visit(unop.expr)
        if isinstance(expr, Number):
            self.result = unop.evaluate(Scope())
        else:
            self.result = UnaryOperation(unop.op, expr)

    def visit_function_call(self, func_call):
        self.result = FunctionCall(self.visit(func_call.fun_expr),
                                   list(map(self.visit, func_call.args)))

    def prosses_stmt_list(self, stmt_list):
        return list(map(self.visit, stmt_list))


def my_tests():
    PP = PrettyPrinter
    CF = ConstantFolder
    UnOp = UnaryOperation
    BinOp = BinaryOperation

    assert ConstantFolder().visit(UnaryOperation('!', Number(42))) == Number(0)
    assert ConstantFolder().visit(UnaryOperation('!', Number(0))) != Number(0)
    assert ConstantFolder().visit(
        UnaryOperation('-', UnaryOperation('-', Number(42)))) == Number(42)
    assert ConstantFolder().visit(
        UnaryOperation('-', Number(42))) == Number(-42)

    assert (CF().visit(UnOp('-', BinOp(Number(3), '+', Number(8))))
        == Number(-11))

    assert ConstantFolder().visit(BinaryOperation(
        Number(8), '+', Number(13))) == Number(21)
    assert ConstantFolder().visit(BinaryOperation(
        Reference('x'), '-', Reference('x'))) == Number(0)
    assert ConstantFolder().visit(BinaryOperation(
        Number(0), '*', Reference('x'))) == Number(0)
    assert ConstantFolder().visit(BinaryOperation(
        Reference('x'), '*', Number(0))) == Number(0)

    assert ConstantFolder().visit(BinaryOperation(BinaryOperation(
        Number(8), '+', Number(13)), '+', Number(21))) == Number(42)

    PrettyPrinter().visit(ConstantFolder().visit(
        BinaryOperation(Reference('x'), '==', Number(3))))

    PrettyPrinter().visit(ConstantFolder().visit(Conditional(
        UnaryOperation('!', Number(42)), [])))

    fun_call = FunctionCall(Reference('foo'),
                            [BinaryOperation(Number(1), '+', Number(6))])

    fun_call_opti = ConstantFolder().visit(fun_call)
    PrettyPrinter().visit(fun_call_opti)

if __name__ == '__main__':
    my_tests()
