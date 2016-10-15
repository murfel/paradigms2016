#!/usr/bin/env python3

from yat.model import *


class PrettyPrinter:

    ident = 4 * ' '

    def visit(self, tree):
        self.result = ''
        self.ident_level = 0
        self.sentence = True

        tree.accept(self)
        print(self.result)

    def visit_number(self, num):
        sentence = self.sentence
        self.sentence = False
        self.result += str(num.value)
        self.complete_if_sentence(sentence)

    def visit_function_definition(self, func_def):
        sentence = self.sentence
        self.sentence = False
        self.result += self.ident_level * self.ident + 'def ' + func_def.name
        self.add_arg_block(func_def.function.args)
        self.ident_level += 1
        self.add_stmt_block(func_def.function.body)
        self.ident_level -= 1
        self.complete_if_sentence(sentence)

    def visit_conditional(self, cond):
        self.result += 'if ('
        self.sentence = False
        cond.condition.accept(self)
        self.result += ')'

        self.sentence = True
        self.ident_level += 1
        self.add_stmt_block(cond.if_true)

        self.sentence = True
        if cond.if_false:
            self.result += ' else '
            self.add_stmt_block(cond.if_false)

        self.complete_if_sentence(True)
        self.ident_level -= 1

    def visit_print(self, print):
        self.result += 'print '
        self.sentence = False
        print.expr.accept(self)
        self.complete_if_sentence(True)

    def visit_read(self, read):
        self.result += 'read ' + read.name
        self.complete_if_sentence(True)

    def visit_function_call(self, func_call):
        sentence = self.sentence
        self.sentence = False
        func_call.fun_expr.accept(self)
        self.add_arg_block(func_call.args)
        self.complete_if_sentence(sentence)

    def visit_reference(self, ref):
        self.result += ref.name
        self.complete_if_sentence(self.sentence)

    def visit_binary_operation(self, binop):
        self.result += '(('
        sentence = self.sentence
        self.sentence = False
        binop.lhs.accept(self)
        self.result += ') ' + binop.op + ' ('
        binop.rhs.accept(self)
        self.result += '))'
        self.complete_if_sentence(sentence)

    def visit_unary_operation(self, unop):
        self.result += '(' + unop.op + '('
        sentence = self.sentence
        self.sentence = False
        unop.expr.accept(self)
        self.result += '))'
        self.complete_if_sentence(sentence)

    def add_stmt_block(self, stmt_block):
        self.result += ' {'
        for stmt in stmt_block:
            self.sentence = True
            self.result += '\n' + self.ident_level * self.ident
            stmt.accept(self)
        self.result += '\n' + (self.ident_level - 1) * self.ident + '}'

    def add_arg_block(self, expr_block):
        self.result += '('
        for arg in expr_block:
            arg.accept(self)
            self.result += ', '
        if expr_block:
            self.result = self.result[:-2]
        self.result += ')'

    def complete_if_sentence(self, sentence):
        if sentence:
            self.result += ';'


def my_tests():
    number = Number(42)
    conditional = Conditional(number, [], [])
    printer = PrettyPrinter()
    printer.visit(conditional)

    function = Function([], [conditional, Number(5)])
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

    reference = Reference('foo')
    call = FunctionCall(reference, [Number(1), Number(2), Number(3)])
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

    n0, n1, n2 = Number(1), Number(2), Number(3)
    add = BinaryOperation(n1, '+', n2)
    mul = BinaryOperation(n0, '*', add)
    printer = PrettyPrinter()
    printer.visit(mul)


if __name__ == '__main__':
    my_tests()
