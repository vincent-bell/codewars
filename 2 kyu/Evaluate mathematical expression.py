### Token Types ###
TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'


class Token:
    def __init__(self, _type, value):
        self.type = _type
        self.value = value

    def __repr__(self):
        return f'{self.type}:{self.value}'


### Lexer ###
class Lexer:
    def __init__(self):
        self.current_char = None
        self.index = -1

    def make_tokens(self, expression):
        self.expression = expression
        self.tokens = []
        self.advance()

        while self.current_char is not None:

            if self.current_char.isspace():
                self.advance()
            elif self.current_char.isdigit():
                self.make_number()
            elif self.current_char == '+':
                self.tokens.append(Token(TT_PLUS, '+'))
                self.advance()
            elif self.current_char == '-':
                self.tokens.append(Token(TT_MINUS, '-'))
                self.advance()
            elif self.current_char == '*':
                self.tokens.append(Token(TT_MUL, '*'))
                self.advance()
            elif self.current_char == '/':
                self.tokens.append(Token(TT_DIV, '/'))
                self.advance()
            elif self.current_char == '(':
                self.tokens.append(Token(TT_LPAREN, '('))
                self.advance()
            elif self.current_char == ')':
                self.tokens.append(Token(TT_RPAREN, ')'))
                self.advance()

        return self.tokens

    def make_number(self):
        num_str = ''
        dot_count = 0

        while self.current_char and self.current_char.isdigit() or self.current_char == '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            self.tokens.append(Token(TT_INT, int(num_str)))
        else:
            self.tokens.append(Token(TT_FLOAT, float(num_str)))

    def advance(self):
        self.index += 1
        self.current_char = self.expression[self.index] if self.index < len(self.expression) else None


### Nodes ###
class NumberNode:
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f'{self.token}'


class BinaryOperationNode:
    def __init__(self, left_node, operator_token, right_node):
        self.left_node = left_node
        self.operator_token = operator_token
        self.right_node = right_node

    def __repr__(self):
        return f'({self.left_node}, {self.operator_token}, {self.right_node})'


class UnaryOperationNode:
    def __init__(self, operator_token, node):
        self.operator_token = operator_token
        self.node = node

    def __repr__(self):
        return f'({self.operator_token}, {self.node})'


### Parser ###
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = -1
        self.advance()

        self.parse = self.expression

    def factor(self):
        token = self.token

        if token.type in (TT_PLUS, TT_MINUS):
            self.advance()
            factor = self.factor()
            return UnaryOperationNode(token, factor) # ?

        elif token.type in [TT_INT, TT_FLOAT]:
            self.advance()
            return NumberNode(token)

        elif token.type == TT_LPAREN:
            self.advance()
            expression = self.expression()
            if self.token.type == TT_RPAREN:
                self.advance()
                return expression
 
    def term(self):
        return self.binary_operation(self.factor, (TT_MUL, TT_DIV))

    def expression(self):
        return self.binary_operation(self.term, (TT_PLUS, TT_MINUS))

    def binary_operation(self, func, operations):
        left = func()

        while self.token.type in operations:
            operator_token = self.token
            self.advance()
            right = func()
            left = BinaryOperationNode(left, operator_token, right)

        return left

    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.token = self.tokens[self.token_index]
        return self.token


### Number ###
class Number:
    def __init__(self, value):
        self.value = value

    def added_to(self, other):
        return Number(self.value + other.value)

    def subtracted_by(self, other):
        return Number(self.value - other.value)

    def multiplied_by(self, other):
        return Number(self.value * other.value)

    def divided_by(self, other):
        return Number(self.value / other.value)


### Interpreter ###
class Interpreter:
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        methods = {
            'visit_NumberNode': self.visit_NumberNode,
            'visit_BinaryOperationNode': self.visit_BinaryOperationNode,
            'visit_UnaryOperationNode': self.visit_UnaryOperationNode
        }
        return methods[method_name](node)

    def visit_NumberNode(self, node):
        return Number(node.token.value)

    def visit_BinaryOperationNode(self, node):
        left = self.visit(node.left_node)
        right = self.visit(node.right_node)

        if node.operator_token.type == TT_PLUS:
            return left.added_to(right)
        elif node.operator_token.type == TT_MINUS:
            return left.subtracted_by(right)
        elif node.operator_token.type == TT_MUL:
            return left.multiplied_by(right)
        elif node.operator_token.type == TT_DIV:
            return left.divided_by(right)

    def visit_UnaryOperationNode(self, node):
        number = self.visit(node.node)

        if node.operator_token.type == TT_MINUS:
            return number.multiplied_by(Number(-1))


def calc(expression):
    lexer = Lexer()
    tokens = lexer.make_tokens(expression)

    parser = Parser(tokens)
    abstract_syntax_tree = parser.parse()

    return Interpreter().visit(abstract_syntax_tree).value
