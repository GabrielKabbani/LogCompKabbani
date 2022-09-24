import symbol
import sys
import re

reserved_words = ["Print"]
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

class UnOp(Node):
    def evaluate(self):
        child = self.children[0].evaluate()

        if self.value == "+":
            return child
        
        elif self.value == "-":
            return -child

class IntVal(Node):
    def evaluate(self):
        return int(self.value)

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

            elif self.source[self.position] == "=":
                self.next = Token("EQUALS", self.source[self.position])

                self.position += 1

                return self.next
            
            elif self.source[self.position] == ";":
                self.next = Token("SEMICOLON", self.source[self.position])

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
                    if self.source[self.position+1].isalpha():
                        raise Exception("variable cannot start with a number")
                    num+=self.source[self.position]
                else:
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
        while token.next.type == "PLUS" or token.next.type == "MINUS":
            value=token.next.value
            token.selectNext()
            result = BinOp(value, [result, Parser.parse_term(token)])

        return result

    @staticmethod
    def parse_term(token):
        result = Parser.parse_factor(token)

        while token.next.type == "DIV" or token.next.type == "MULT":
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

        elif token.next.type == "PLUS" or token.next.type == "MINUS":
            value = token.next.value
            token.selectNext()
            result= UnOp(value, [Parser.parse_factor(token)])

        elif token.next.type == "PAR_OPEN":
            token.selectNext()
            result=Parser.parse_expression(token)
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

                result = Assignment("EQUALS", [result, Parser.parse_expression(token)])
                
                # token.selectNext()

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
                display = Parser.parse_expression(token)

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
                raise Exception("Invalid")

        elif token.next.type == "SEMICOLON":
            token.selectNext()
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
            # print(token.next.type)
        
        token.selectNext()
        return node

                    

                  
    @staticmethod
    def run(math):
        # tokens = Tokenizer(Pre_pro.filter(math.replace("\n","")))
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