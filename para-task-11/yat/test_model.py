#!/usr/bin/env python3

import io
import pytest
import sys
import os.path
import operator

from unittest.mock import patch

try:
    from yat.model import *
except:
    from model import *


@patch('sys.stdout', new_callable=io.StringIO)
def get_value(n, mock_stdout):
    Print(n).evaluate(Scope())
    return int(mock_stdout.getvalue())


class TestPrint():

    def test_simple(self):
        Print(Number(42)).evaluate(Scope())


class TestNumber():

    def test_simple(self):
        assert get_value(Number(42)) == 42

    def test_evaluate(self):
        assert isinstance(Number(42).evaluate(Scope()), Number)


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

    def test_not_positive(self):
        assert get_value(UnaryOperation('!', Number(1)).evaluate(Scope())) == 0

    def test_not_negative(self):
        assert get_value(UnaryOperation('!', Number(0)).evaluate(Scope())) != 0

    def test_minus_positive(self):
        assert get_value(
            UnaryOperation('-', Number(42)).evaluate(Scope())) == -42

    def test_expand_operand(self):
        assert get_value(
            UnaryOperation(
                '-',
                UnaryOperation('!', Number(0))
            ).evaluate(Scope())
        ) < 0


class TestBinaryOperation:

    @pytest.mark.parametrize("op, left, right, ans",
                             [('+', 100, 25, 125),
                              ('-', 100, 25, 75),
                              ('*', 100, 25, 2500),
                              ('/', 9, 2, 4),
                              ('%', 10, 3, 1)])
    def test_arithmetic_ops(self, op, left, right, ans):
        assert (get_value(
                BinaryOperation(Number(left),
                                op,
                                Number(right)).evaluate(Scope())) == ans)

    @pytest.mark.parametrize("op, left, right, ans",
                             [('==', 3, 3, True),
                              ('!=', 1, 3, True),
                              ('<', 3, 5, True),
                              ('>', 3, 5, False),
                              ('<=', 5, 3, False),
                              ('>=', 3, 3, True),
                              ('&&', 1, 0, False),
                              ('||', 1, 0, True)])
    def test_logical_ops(self, op, left, right, ans):
        val = get_value(BinaryOperation(Number(left),
                                        op,
                                        Number(right)).evaluate(Scope()))
        if ans:
            assert (val != 0)
        else:
            assert (val == 0)


class TestConditional():

    def test_true_empty_none(self):
        Conditional(Number(1), [])

    def test_true_empty_empty(self):
        Conditional(Number(1), [], [])

    def test_false_empty_none(self):
        Conditional(Number(0), [])

    def test_false_empty_empty(self):
        Conditional(Number(0), [], [])

    def test_true_none_none(self):
        Conditional(Number(1), None)

    def test_false_none_none(self):
        Conditional(Number(0), None)

    def test_simple(self):
        assert get_value(Conditional(
            Number(1), [Number(42), Number(13)]).evaluate(Scope())) == 13

    def test_check_condition(self):
        assert get_value(Conditional(Number(0), [Number(42), Number(13)], [
                         Number(8)]).evaluate(Scope())) == 8


class TestFunction():

    def test_empty(self):
        Function((), []).evaluate(Scope())

    def test_empty_body(self):
        Function(('foo', 'bar'), []).evaluate(Scope())

    def test_no_args(self):
        assert get_value(Function((), [Number(42)]).evaluate(Scope())) == 42

    def test_simple(self):
        assert get_value(
            Function(('foo', 'bar'), [Number(42), Number(13)]
                     ).evaluate(Scope())) == 13


class TestFunctionCall():

    def test_simple(self):
        fun = Function(('foo', 'bar'),
                       [Number(42), Reference('foo'), Reference('bar')])
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

    @patch('sys.stdin', new=io.StringIO('777'))
    def test_update_scope(self):
        scope = Scope()
        Read('num').evaluate(scope)
        assert get_value(scope['num']) == 777

    @patch('sys.stdin', new=io.StringIO('777'))
    def test_return_value(self):
        scope = Scope()
        assert get_value(Read('num').evaluate(scope)) == 777


if __name__ == '__main__':
    pytest.main()
