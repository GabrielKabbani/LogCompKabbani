import sys

x=sys.argv[1]


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
    def parseExpression(token):

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
            while token.next.type == "PLUS" or token.next.type == "MINUS" or token.next.type == "SPACE":
                if token.next.type == "PLUS":
                    token.selectNext()
                    if token.next.type == "SPACE":
                        result+=0
                    elif token.next.type == "INT":
                        result += int(token.next.value)
                    else:
                        raise Exception("Invalid")

                elif token.next.type == "MINUS":
                    token.selectNext()
                    if token.next.type == "SPACE":
                        result-=0
                    elif token.next.type == "INT":
                        result -= int(token.next.value)
                    else:
                        raise Exception("Invalid")

                token.selectNext()
            
            if token.next.type == "EOF":
                return result

        else:
            raise Exception("Invalid")
                    
    @staticmethod
    def run(math):
        tokens = Tokenizer(math)
        output = Parser.parseExpression(tokens)

        if output != None:
            print(output)       

def main():
	Parser.run(sys.argv[1])

main()
