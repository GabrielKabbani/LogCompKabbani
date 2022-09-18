import sys
import re
x=sys.argv[1]


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


            else: #futuramente implementar enum pra verificar se é numero mesmo
                if self.source[self.position].isdigit():
                    num+=self.source[self.position]
                else:
                    self.next = Token("ERROR", self.source[self.position])
                    self.position+=1
                    return self.next
                
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
    def run(math):
        tokens = Tokenizer(math)
        tokens.selectNext()
        output = Parser.parse_expression(tokens)
        if output != None and tokens.next.type == "EOF":
            print(output.evaluate())    
        else:
            raise Exception("Invalid")


class Pre_pro:

    @staticmethod
    def filter(txt):
        for i in range(len(txt)):
            if txt[i] == "/" and txt[i+1] == "/":
                return txt[:i]
        return txt


def main():
	Parser.run(Pre_pro.filter(sys.argv[1]))

main()