import symbol
import sys
import re

reserved_words = ["Print", "Read", "while", "if", "else"]
symbol_table = {}

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Node:
    def __init__(self, value, children = []):
        self.value = value
        self.children = children

    def evaluate(self):
        pass

class Block(Node):

    def evaluate(self):
        for statement in self.children:
            statement.evaluate()

class BinOp(Node):
    def evaluate(self):
        first = self.children[0].evaluate()
        second = self.children[1].evaluate()

        if self.value == "+":
            return first + second

        elif self.value == "-":
            return first - second

        elif self.value == "*":
            return first * second

        elif self.value == "/":
            return int(first // second)

        elif self.value == "==":
            return first == second

        elif self.value == ">":
            return first > second

        elif self.value == "<":
            return first < second

        elif self.value == "&&":
            return first and second

        elif self.value == "||":
            return first or second

class UnOp(Node):
    def evaluate(self):
        child = self.children[0].evaluate()

        if self.value == "+":
            return child
        
        elif self.value == "-":
            return -child

        elif self.value == "!":
            return not(child)

class IntVal(Node):
    def evaluate(self):
        return int(self.value)

class While(Node):
    def evaluate(self):
        first = self.children[0]
        second = self.children[1]

        while (first.evaluate()):
            second.evaluate()

class If(Node):
    def evaluate(self):
        first = self.children[0]
        second = self.children[1]
        if first.evaluate():
            second.evaluate()

        elif len(self.children) > 2:
            self.children[2].evaluate()


class NoOp(Node):
    def evaluate(self):
        pass

class SymbolTable():

    @staticmethod
    def getter(x):
        return symbol_table[x]

    @staticmethod
    def setter(x, y):
        symbol_table[x] = y
        
class Identifier(Node):

    def evaluate(self):
        return SymbolTable.getter(self.value)

class Printer(Node):

    def evaluate(self):
        print(self.children[0].evaluate())

class Reader(Node):

    def evaluate(self):
        return int(input())

class Assignment(Node):

    def evaluate(self):
        SymbolTable.setter(self.children[0], self.children[1].evaluate())
    
class Tokenizer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None
        
    def selectNext(self):
        token_incomplete=True
        num=""
        while self.position < len(self.source) and self.source[self.position] == " ":
            self.position+=1

        if self.position < len(self.source): #esse é o EOF 
            
            if self.source[self.position] == "+":
                self.next = Token("PLUS", self.source[self.position])

                self.position += 1

                return self.next

            elif self.source[self.position] == "-":
                self.next = Token("MINUS", self.source[self.position])

                self.position += 1

                return self.next

            elif self.source[self.position] == "*":
                self.next = Token("MULT", self.source[self.position])

                self.position += 1

                return self.next
            
            elif self.source[self.position] == "/":
                self.next = Token("DIV", self.source[self.position])

                self.position += 1

                return self.next

            elif self.source[self.position] == "(":
                self.next = Token("PAR_OPEN", self.source[self.position])

                self.position += 1

                return self.next

            elif self.source[self.position] == ")":
                self.next = Token("PAR_CLOSE", self.source[self.position])

                self.position += 1

                return self.next

            elif self.source[self.position] == "{":
                self.next = Token("KEY_OPEN", self.source[self.position])

                self.position += 1

                return self.next

            elif self.source[self.position] == "}":
                self.next = Token("KEY_CLOSE", self.source[self.position])

                self.position += 1

                return self.next

            elif self.source[self.position] == "|" and self.source[self.position+1] == "|":
                self.next = Token("OR", "||")
                self.position += 2

            elif self.source[self.position] == "&" and self.source[self.position+1] == "&":
                self.next = Token("AND", "&&")
                self.position += 2

            elif self.source[self.position] == "=":
                if self.source[self.position+1] == "=":
                    self.next = Token("COMPARE_EQUALS", "==")
                    self.position += 2
                else:
                    self.next = Token("EQUALS", self.source[self.position])

                    self.position += 1

                return self.next
            
            elif self.source[self.position] == ";":
                self.next = Token("SEMICOLON", self.source[self.position])

                self.position += 1

                return self.next
                

            elif self.source[self.position] == ">":
                self.next = Token("BIGGER", self.source[self.position])

                self.position += 1

                return self.next

            elif self.source[self.position] == "<":
                self.next = Token("SMALLER", self.source[self.position])

                self.position += 1

                return self.next

            elif self.source[self.position] == "!":
                self.next = Token("NOT", self.source[self.position])

                self.position += 1

                return self.next

            elif self.source[self.position].isalpha():

                id = self.source[self.position]
                self.position += 1

                while self.source[self.position].isalpha() or self.source[self.position].isdigit() or self.source[self.position] == "_" and self.position < len(self.source)-1:
                    id += self.source[self.position]
                    self.position +=1

                if id in reserved_words:
                    self.next = Token(id, id)
                else:
                    self.next = Token("IDENTIFIER", id)



            else: #futuramente implementar enum pra verificar se é numero mesmo
                if self.source[self.position].isdigit():
                    num+=self.source[self.position]
                else:
                    print(self.source[self.position])
                    raise Exception("Invalid, cannot begin with this value")
                
                if self.position == len(self.source)-1:
                    token_incomplete = False
                else:
                    for i in range(self.position,len(self.source)):
                        if token_incomplete:
                            if i != len(self.source) - 1:
                                if self.source[i+1].isdigit():
                                    num+=self.source[i+1]
                                else:
                                    token_incomplete = False
                            else:
                                token_incomplete = False
                    
            if token_incomplete == False:
                self.next = Token("INT", int(num))
                self.position += len(num)
                token_incomplete = True
                num = ""
                return self.next

        else:
            self.next = Token("EOF", "")
            return self.next


class Parser:
    
    def __init__(self, token):
        self.token = token

    @staticmethod
    def parse_expression(token):
        result = Parser.parse_term(token)
        while token.next.type == "PLUS" or token.next.type == "MINUS" or token.next.type == "OR":
            value=token.next.value
            token.selectNext()
            result = BinOp(value, [result, Parser.parse_term(token)])

        return result
    
    @staticmethod
    def parse_rel_expression(token):
        result = Parser.parse_expression(token)
        while token.next.type == "BIGGER" or token.next.type == "SMALLER" or token.next.type == "COMPARE_EQUALS":
            value=token.next.value
            token.selectNext()
            result = BinOp(value, [result, Parser.parse_expression(token)])

        return result

    @staticmethod
    def parse_term(token):
        result = Parser.parse_factor(token)

        while token.next.type == "DIV" or token.next.type == "MULT" or token.next.type == "AND":
                value = token.next.value
                token.selectNext()
                result = BinOp(value, [result, Parser.parse_factor(token)])

        return result

    @staticmethod
    def parse_factor(token):
        result = 0

        if token.next.type == "INT":
            value = token.next.value
            result = IntVal(value)
            token.selectNext()

        elif token.next.type == "IDENTIFIER":
            result = Identifier(token.next.value)
            token.selectNext()

        elif token.next.type == "PLUS" or token.next.type == "MINUS" or token.next.type == "NOT":
            value = token.next.value
            token.selectNext()
            result= UnOp(value, [Parser.parse_factor(token)])

        elif token.next.type == "Read":
            token.selectNext()
            if token.next.type == "PAR_OPEN":
                token.selectNext()
                if token.next.type != "PAR_CLOSE":
                    raise Exception("Invalid, missing closing parenthesis")
                token.selectNext()
                result = Reader("")
            else:
                raise Exception("Invalid, missing opening parenthesis")

        elif token.next.type == "PAR_OPEN":
            token.selectNext()
            result=Parser.parse_rel_expression(token)
            if token.next.type != "PAR_CLOSE":
                raise Exception("Invalid, missing closing parenthesis")
            token.selectNext()

        elif token.next.type == "PAR_CLOSE":
            raise Exception("Invalid, missing opening parenthesis")

        else:
            raise Exception("Invalid")
        
        return result

    
    @staticmethod
    def parse_statement(token):

        result = NoOp(None)
        if token.next.type == "IDENTIFIER":
            result = token.next.value
            token.selectNext()

            if token.next.type == "EQUALS":
                token.selectNext()

                result = Assignment("EQUALS", [result, Parser.parse_rel_expression(token)])

                if token.next.type == "SEMICOLON":
                    token.selectNext()
                    return result
                else:
                    raise Exception("Missing ';'")
            else:
                raise Exception("Invalid")

        elif token.next.type == "Print":
            token.selectNext()

            if token.next.type == "PAR_OPEN":

                token.selectNext()
                display = Parser.parse_rel_expression(token)

                if token.next.type == "PAR_CLOSE":

                    result = Printer("Print", [display])
                    token.selectNext()

                    if token.next.type == "SEMICOLON":
                        token.selectNext()
                        return result
                    else:
                        raise Exception("Missing ';'")
                else:
                    raise Exception("Missing closing parenthesis")
            else:
                raise Exception("Missing opening parenthesis")

        elif token.next.type == "SEMICOLON":
            token.selectNext()
            return result

        elif token.next.type == "INT":
            raise Exception("var cannot start with number")

        elif token.next.type == "while":
            token.selectNext()
            if token.next.type == "PAR_OPEN":
                token.selectNext()
                val = Parser.parse_rel_expression(token)

                if token.next.type == "PAR_CLOSE":
                    token.selectNext()
                    val2 = Parser.parse_statement(token)
                    result = While("", [val, val2])
                    return result

                else: 
                    raise Exception("Missing closing parenthesis")
            else:
                raise Exception("Missing opening parenthesis")

        elif token.next.type == "if":
            token.selectNext()
            if token.next.type == "PAR_OPEN":
                token.selectNext()
                val = Parser.parse_rel_expression(token)

                if token.next.type == "PAR_CLOSE":
                    token.selectNext()
                    val2 = Parser.parse_statement(token)
                    #outro selectnext?

                    if token.next.type == "else":
                        token.selectNext()
                        val3 = Parser.parse_statement(token)
                        result = If("", [val, val2, val3])
                    
                    else:
                        result = If("", [val, val2])

                    return result

                else: 
                    raise Exception("Missing closing parenthesis")
            else:
                raise Exception("Missing opening parenthesis")

    

        else:
            result = Parser.parse_block(token)
            return result

    @staticmethod
    def parse_block(token):
        if token.next.type == "KEY_OPEN":
            token.selectNext()
        else:
            raise Exception("Missing opening keys")

        node = Block("", [])

        while token.next.type != "KEY_CLOSE":
            child = Parser.parse_statement(token)
            node.children.append(child)
            if token.next.type == "EOF":
                raise Exception("Missing closing keys")
        
        token.selectNext()
        return node

                    

                  
    @staticmethod
    def run(math):
        tokens = Tokenizer(Pre_pro.filter(math))
        tokens.selectNext()
        output = Parser.parse_block(tokens)
        if output != None and tokens.next.type == "EOF":
            output.evaluate()
        else:
            raise Exception("Invalid")


class Pre_pro:

    @staticmethod
    def filter(source: str):
        source = re.sub(re.compile("//.*?\n"), "", source)
        source = re.sub("\s+", " ", source)
        return source.replace("\n", "")


def main():
    with open(sys.argv[1], "r") as file:
        Parser.run(file.read())


main()