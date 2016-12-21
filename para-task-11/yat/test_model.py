#!/usr/bin/env python3

import io
import pytest
import sys
import os.path

try:
    from yat.model import *
except:
    from model import *


def get_value(n):
    Print(n).evaluate(Scope())
    return int(sys.stdout.getvalue())


class TestPrint():

    def test_simple(self, monkeypatch):
        Print(Number(42)).evaluate(Scope())


class TestNumber():

    def test_simple(self, monkeypatch):
        monkeypatch.setattr(sys, 'stdout', io.StringIO())
        assert get_value(Number(42)) == 42


class TestScope():

    def test_simple(self):
        parent = Scope()
        foo = Number(42)
        parent['foo'] = foo
        assert parent['foo'] == foo

    def test_inherit_parent(self):
        parent = Scope()
        foo = Number(42)
        parent['foo'] = foo
        scope = Scope(parent)
        assert scope['foo'] == foo

    def test_inheritance_leaves_parent_ok(self):
        parent = Scope()
        foo = Number(42)
        parent['foo'] = foo
        scope = Scope(parent)
        bar = Number(13)
        scope['foo'] = bar
        assert parent['foo'] == foo


class TestReference():

    def test_simple(self):
        parent = Scope()
        foo = Number(42)
        parent['foo'] = foo
        assert Reference('foo').evaluate(parent) == foo


class TestUnaryOperation():

    def test_not_positive(self, monkeypatch):
        monkeypatch.setattr(sys, 'stdout', io.StringIO())
        assert get_value(UnaryOperation('!', Number(1)).evaluate(Scope())) == 0

    def test_not_negative(self, monkeypatch):
        monkeypatch.setattr(sys, 'stdout', io.StringIO())
        assert get_value(UnaryOperation('!', Number(0)).evaluate(Scope())) == 1

    def test_minus_positive(self, monkeypatch):
        monkeypatch.setattr(sys, 'stdout', io.StringIO())
        assert get_value(
            UnaryOperation('-', Number(42)).evaluate(Scope())) == -42

    def test_expand_operand(self, monkeypatch):
        monkeypatch.setattr(sys, 'stdout', io.StringIO())
        assert get_value(
            UnaryOperation(
                '-',
                UnaryOperation('!', Number(0))
            ).evaluate(Scope())
        ) == -1


class TestBinaryOperation():
    sym_to_op = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.floordiv,
        '%': operator.mod,
        '==': operator.eq,
        '!=': operator.ne,
        '<': operator.lt,
        '>': operator.gt,
        '<=': operator.le,
        '>=': operator.ge,
        '&&': lambda a, b: a and b,
        '||': lambda a, b: a or b,
    }

    def test_simple(self, monkeypatch):
        for op, func in self.sym_to_op.items():
            for i in range(10):
                for j in range(1, 10):
                    monkeypatch.setattr(sys, 'stdout', io.StringIO())
                    assert (get_value(
                        BinaryOperation(
                            Number(i),
                            op,
                            Number(j)
                        ).evaluate(Scope())) == int(func(i, j)))


class TestConditional():

    def test_true_empty_none(self):
        Conditional(Number(1), [])

    def test_true_empty_empty(self):
        Conditional(Number(1), [], [])

    def test_false_empty_none(self):
        Conditional(Number(0), [])

    def test_false_empty_empty(self):
        Conditional(Number(0), [], [])

    def test_simple(self, monkeypatch):
        monkeypatch.setattr(sys, 'stdout', io.StringIO())
        assert get_value(Conditional(
            Number(1), [Number(42), Number(13)]).evaluate(Scope())) == 13

    def test_check_condition(self, monkeypatch):
        monkeypatch.setattr(sys, 'stdout', io.StringIO())
        assert get_value(Conditional(Number(0), [Number(42), Number(13)], [
                         Number(8)]).evaluate(Scope())) == 8


class TestFunction():

    def test_empty(self):
        Function((), [])

    def test_empty_body(self):
        Function(('foo', 'bar'), [])

    def test_no_args(self, monkeypatch):
        monkeypatch.setattr(sys, 'stdout', io.StringIO())
        assert get_value(Function((), [Number(42)]).evaluate(Scope())) == 42

    def test_simple(self, monkeypatch):
        monkeypatch.setattr(sys, 'stdout', io.StringIO())
        assert get_value(
            Function(('foo', 'bar'), [Number(42), Number(13)]
                     ).evaluate(Scope())) == 13


class TestFunctionCall():

    def test_simple(self, monkeypatch):
        monkeypatch.setattr(sys, 'stdout', io.StringIO())
        fun = Function(('foo', 'bar'), [Number(
            42), Reference('foo'), Reference('bar')])
        fun_call = FunctionCall(FunctionDefinition(
            'fun', fun), (Number(1), Number(2)))
        assert get_value(fun_call.evaluate(Scope())) == 2

    def test_empty(self):
        FunctionCall(FunctionDefinition(
            'fun', Function((), [])), ()).evaluate(Scope())


class TestFunctionDefinition():

    def test_simple(self):
        parent = Scope()
        fun = Function((), [])
        FunctionDefinition('foo', fun).evaluate(parent)
        assert parent['foo'] == fun


class TestRead():

    def test_update_scope(self, monkeypatch):
        monkeypatch.setattr(sys, 'stdout', io.StringIO())
        monkeypatch.setattr(sys, 'stdin', io.StringIO('777'))
        scope = Scope()
        Read('num').evaluate(scope)
        assert get_value(scope['num']) == 777

    def test_return_value(self, monkeypatch):
        monkeypatch.setattr(sys, 'stdout', io.StringIO())
        monkeypatch.setattr(sys, 'stdin', io.StringIO('777'))
        scope = Scope()
        assert get_value(Read('num').evaluate(scope)) == 777


if __name__ == '__main__':
    pytest.main()
