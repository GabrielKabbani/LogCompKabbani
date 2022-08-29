import sys
import re
x=sys.argv[1]

#tirar token space

class Token:
    def __init__(self, type,value):
        self.type = type
        self.value = value
    
class Tokenizer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None
        
    def selectNext(self):
        token_incomplete=True
        int=""

        if self.position < len(self.source): #esse é o EOF     
            if "+" not in self.source and "-" not in self.source and "*" not in self.source and "/" not in self.source:
                self.next = Token("ERROR", self.source[self.position])
                return self.next

            if self.source[self.position] == "+":
                self.next = Token("PLUS", self.source[self.position])

                while self.source[self.position+1]==" ":
                    self.position+=1

                self.position += 1

                return self.next

            elif self.source[self.position] == "-":
                self.next = Token("MINUS", self.source[self.position])

                while self.source[self.position+1]==" ":
                    self.position+=1

                self.position += 1

                return self.next

            elif self.source[self.position] == "*":
                self.next = Token("MULT", self.source[self.position])

                while self.source[self.position+1]==" ":
                    self.position+=1

                self.position += 1

                return self.next
            
            elif self.source[self.position] == "/":
                self.next = Token("DIV", self.source[self.position])

                while self.source[self.position+1]==" ":
                    self.position+=1

                self.position += 1

                return self.next

            elif self.source[self.position] == " ":
                self.next = Token("SPACE", self.source[self.position])
                self.position+=1

                return self.next

            else: #futuramente implementar enum pra verificar se é numero mesmo
                if self.source[self.position].isdigit():
                    int+=self.source[self.position]
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
                                    int+=self.source[i+1]
                                else:
                                    token_incomplete = False
                            else:
                                token_incomplete = False


            if token_incomplete == False:
                self.next = Token("INT", int)
                self.position += len(int)
                token_incomplete = True
                int = ""
                return self.next

        else:
            self.next = Token("EOF", "")
            return self.next


class Parser:
    
    def __init__(self, token):
        self.token = token

    @staticmethod
    def parse_term(token):

        token.selectNext()
        result=0

        if token.next.type == "SPACE":
            while(token.next.type == "SPACE"):
                token.selectNext()

        if token.next.type == "ERROR":
            raise Exception("Invalid")
            
        if token.next.type == "INT":
            result = int(token.next.value)
            token.selectNext()
            while token.next.type == "MULT" or token.next.type == "DIV" or token.next.type == "SPACE":
                if token.next.type == "MULT":
                    token.selectNext()
                    if token.next.type == "INT":
                        result *= int(token.next.value)
                    else:
                        raise Exception("Invalid")

                elif token.next.type == "DIV":
                    token.selectNext()
                    if token.next.type == "INT":
                        result //= int(token.next.value)
                    else:
                        raise Exception("Invalid")

                token.selectNext()
            
            
            return result

        else:
            raise Exception("Invalid")

    @staticmethod
    def parse_expression(token):
        result = Parser.parse_term(token)

        while token.next.type == "PLUS" or token.next.type == "MINUS":
            if token.next.type == "PLUS":
                result += Parser.parse_term(token)
                token.selectNext()

            elif token.next.type == "MINUS":
                result -= Parser.parse_term(token)
                token.selectNext()

        if token.next.type == "EOF":
                return result

        
                    
    @staticmethod
    def run(math):
        tokens = Tokenizer(math)
        output = Parser.parse_expression(tokens)

        if output != None:
            print(output)      


class Pre_pro:

    @staticmethod
    def filter(txt):
        return re.sub(r'//*.*\n?', '', txt)


def main():
    # limpar comentarios antes com um metodo filter. usar newline pra saber quando acabou
	Parser.run(Pre_pro.filter(sys.argv[1]))

main()
