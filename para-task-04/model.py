#!/usr/bin/env python3

# Шаблон для домашнѣго задания
# Рѣализуйте мѣтоды с raise NotImplementedError

import operator


class Scope:

    """Scope - представляет доступ к значениям по именам
    (к функциям и именованным константам).
    Scope может иметь родителя, и если поиск по имени
    в текущем Scope не успешен, то если у Scope есть родитель,
    то поиск делегируется родителю.
    Scope должен поддерживать dict-like интерфейс доступа
    (см. на специальные функции __getitem__ и __setitem__)
    """

    def __init__(self, parent=None):
        self.parent = parent
        self.scope = {}

    def __getitem__(self, key):
        if key in self.scope:
            return self.scope[key]
        return self.parent[key]

    def __setitem__(self, key, item):
        self.scope[key] = item


class Number:

    """Number - представляет число в программе.
    Все числа в нашем языке целые."""

    def __init__(self, value):
        self.value = value

    def evaluate(self, scope):
        return self


class Function:

    """Function - представляет функцию в программе.
    Функция - второй тип поддерживаемый языком.
    Функции можно передавать в другие функции,
    и возвращать из функций.
    Функция состоит из тела и списка имен аргументов.
    Тело функции это список выражений,
    т. е.  у каждого из них есть метод evaluate.
    Во время вычисления функции (метод evaluate),
    все объекты тела функции вычисляются последовательно,
    и результат вычисления последнего из них
    является результатом вычисления функции.
    Список имен аргументов - список имен
    формальных параметров функции."""

    def __init__(self, args, body):
        self.args = args
        self.body = body

    def evaluate(self, scope):
        result = None
        for statement in self.body:
            result = statement.evaluate(scope)
        return result


class FunctionDefinition:

    """FunctionDefinition - представляет определение функции,
    т. е. связывает некоторое имя с объектом Function.
    Результатом вычисления FunctionDefinition является
    обновление текущего Scope - в него
    добавляется новое значение типа Function."""

    def __init__(self, name, function):
        self.name = name
        self.function = function

    def evaluate(self, scope):
        scope[self.name] = self.function
        return self.function


class Conditional:

    """
    Conditional - представляет ветвление в программе, т. е. if.
    """

    def __init__(self, condition, if_true, if_false=None):
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false

    def evaluate(self, scope):
        result = None
        if self.condition.evaluate(scope).value != Number(0).value:
            for statement in self.if_true:
                result = statement.evaluate(scope)
        elif self.if_false:
            for statement in self.if_false:
                result = statement.evaluate(scope)
        return result


class Print:

    """Print - печатает значение выражения на отдельной строке."""

    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        result = self.expr.evaluate(scope).value
        return print(result)


class Read:

    """Read - читает число из стандартного потока ввода
     и обновляет текущий Scope.
     Каждое входное число располагается на отдельной строке
     (никаких пустых строк и лишних символов не будет).
     """

    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        scope[self.name] = Number(int(input()))


class FunctionCall:

    """
    FunctionCall - представляет вызов функции в программе.
    В результате вызова функции должен создаваться новый объект Scope,
    являющий дочерним для текущего Scope
    (т. е. текущий Scope должен стать для него родителем).
    Новый Scope станет текущим Scope-ом при вычислении тела функции.
    """

    def __init__(self, fun_expr, args):
        self.fun_expr = fun_expr
        self.args = args

    def evaluate(self, scope):
        function = self.fun_expr.evaluate(scope)
        call_scope = Scope(scope)
        for param, arg in zip(function.args, self.args):
            call_scope[param] = arg.evaluate(scope)
        return function.evaluate(call_scope)


class Reference:

    """Reference - получение объекта
    (функции или переменной) по его имени."""

    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]


class BinaryOperation:

    """BinaryOperation - представляет бинарную операцию над двумя выражениями.
    Результатом вычисления бинарной операции является объект Number.
    Поддерживаемые операции:
    “+”, “-”, “*”, “/”, “%”, “==”, “!=”,
    “<”, “>”, “<=”, “>=”, “&&”, “||”."""

    sym_to_op = {'+': operator.add,
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
                 '&&': operator.and_,
                 '||': operator.or_,
                 }

    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def evaluate(self, scope):
        lhs_value = self.lhs.evaluate(scope).value
        rhs_value = self.rhs.evaluate(scope).value
        return Number(int(self.sym_to_op[self.op](lhs_value, rhs_value)))


class UnaryOperation:

    """UnaryOperation - представляет унарную операцию над выражением.
    Результатом вычисления унарной операции является объект Number.
    Поддерживаемые операции: “-”, “!”."""

    sym_to_op = {'-': operator.neg,
                 '!': operator.not_,
                 }

    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def evaluate(self, scope):
        expr_value = self.expr.evaluate(scope).value
        return Number(self.sym_to_op[self.op](expr_value))


def example():
    """
    Example test (roughly):

    def foo(hello, world):
        return print(hello + world)

    foo(5, -(3))

    """

    parent = Scope()
    parent["foo"] = Function(('hello', 'world'),
                             [Print(BinaryOperation(Reference('hello'),
                                                    '+',
                                                    Reference('world')))])
    parent["bar"] = Number(10)
    scope = Scope(parent)
    assert scope["bar"].value == 10
    scope["bar"] = Number(20)
    assert scope["bar"].value == 20
    print('It should print 2: ', end='')
    FunctionCall(FunctionDefinition('foo', parent['foo']),
                 [Number(5), UnaryOperation('-', Number(3))]
                 ).evaluate(scope)


def my_tests():
    """
    Test 1

    def foo(a, step):
        b = int(input())
        if a < b:
            print(a)
            print(a + (-step))
            return a + (-step)
        else:
            print(b)
            print(b + (-step))
            return b + (-step)

    p_a = 42
    p_step = 2

    foo(5, 2)
    """
    parent = Scope()

    # Test 1
    parent['p_foo'] = (
    Function(('a', 'step'),
             [Read('b'),
              Conditional(BinaryOperation(Reference('a'), '<', Reference('b')),
                          [Print(Reference('a')),
                           Print(BinaryOperation(Reference('a'),
                                                 '*',
                                                 UnaryOperation('-', Reference('step'))))],
                          [Print(Reference('b')),
                           Print(BinaryOperation(Reference('b'),
                                                 '*',
                                                 UnaryOperation('-', Reference('step'))))]
                          )
              ]
             )
    )

    parent['p_a'] = Number(42)
    parent['p_step'] = Number(2)

    FunctionCall(FunctionDefinition('foo', parent['p_foo']),
                 [Reference('p_a'), Reference('p_step')],
                 ).evaluate(parent)


if __name__ == '__main__':
    example()
    my_tests()
