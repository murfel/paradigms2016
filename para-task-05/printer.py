#!/usr/bin/env python3

from yat.model import *


class Arithm:

    def visit(self, tree):
        tree.accept(self)
        return self.result

    def visit_number(self, num):
        self.result = str(num.value)

    def visit_reference(self, ref):
        self.result = ref.name

    def visit_binary_operation(self, binop):
        self.result = '({} {} {})'.format(
            self.visit(binop.lhs), binop.op, self.visit(binop.rhs))

    def visit_unary_operation(self, unop):
        self.result = '({}{})'.format(unop.op, self.visit(unop.expr))

    def visit_function_call(self, func_call):
        self.result = '{}({})'.format(self.visit(
            func_call.fun_expr), ', '.join(map(self.visit, func_call.args)))

    def visit_function_definition(self, fun_def):
        self.result = fun_def.name


class PrettyPrinter:

    def __init__(self, indent=4 * ' '):
        self.indent = indent

    def visit(self, tree):
        self.visit_silently(tree)
        print('\n'.join(self.result))

    def visit_silently(self, tree):
        self.result = []
        tree.accept(self)
        return self.result

    def visit_function_definition(self, func_def):
        self.result.append('def {}({}) {{'.format(func_def.name, ', '.join(
            func_def.function.args)))
        self.add_stmt_block(func_def.function.body)
        self.result.append('};')

    def visit_conditional(self, cond):
        self.result.append('if ({}) {{'.format(Arithm().visit(cond.condition)))
        self.add_stmt_block(cond.if_true)
        if cond.if_false:
            self.result.append('} else {')
            self.add_stmt_block(cond.if_false)
        self.result.append('};')

    def visit_print(self, print_stmt):
        self.result.append('print {};'.format(Arithm().visit(print_stmt.expr)))

    def visit_read(self, read):
        self.result.append('read {};'.format(read.name))

    def visit_arithm_as_sentence(self, expr):
        self.result.append(Arithm().visit(expr) + ';')

    def add_stmt_block(self, stmt_block):
        for stmt in stmt_block:
            for line in PrettyPrinter(self.indent).visit_silently(stmt):
                self.result.append('{}{}'.format(self.indent, line))

    visit_number = visit_arithm_as_sentence
    visit_reference = visit_arithm_as_sentence
    visit_binary_operation = visit_arithm_as_sentence
    visit_unary_operation = visit_arithm_as_sentence
    visit_function_call = visit_arithm_as_sentence


def my_tests():
    number = Number(42)
    conditional = Conditional(number, [Number(1), Number(2), Number(3)],
                              [Number(4), Number(5), Number(6)])
    printer = PrettyPrinter()
    printer.visit(conditional)

    conditional2 = Conditional(number, [conditional])

    function = Function(['x', 'y'],
                        [conditional2, Number(5)])
    definition = FunctionDefinition('foo', function)
    printer = PrettyPrinter()
    printer.visit(definition)

    number = Number(42)
    print = Print(number)
    printer = PrettyPrinter()
    printer.visit(print)

    read = Read('x')
    printer = PrettyPrinter()
    printer.visit(read)

    ten = Number(10)
    printer = PrettyPrinter()
    printer.visit(ten)

    reference = Reference('x')
    printer = PrettyPrinter()
    printer.visit(reference)

    n0, n1, n2 = Number(1), Number(2), Number(3)
    add = BinaryOperation(n1, '+', n2)
    mul = BinaryOperation(n0, '*', add)
    printer = PrettyPrinter()
    printer.visit(mul)

    reference = Reference('foo')
    call = FunctionCall(reference, [mul, FunctionCall(reference, [Number(
        9), Reference('x'), UnaryOperation('-', Number(42)), Number(3)])])
    printer = PrettyPrinter()
    printer.visit(call)

    call = FunctionCall(FunctionDefinition('bar', Function([], [])), [])
    printer = PrettyPrinter()
    printer.visit(call)

    number = Number(42)
    print = Print(number)
    printer = PrettyPrinter()
    printer.visit(print)

    number = Number(42)
    unary = UnaryOperation('-', number)
    printer = PrettyPrinter()
    printer.visit(unary)


if __name__ == '__main__':
    my_tests()
