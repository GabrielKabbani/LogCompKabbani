import symbol
import sys
import re

reserved_words = ["Print", "Read", "while", "if", "else", "var", "i32", "String"]
symbol_table = {}

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Node:

    i=0

    def __init__(self, value, children = []):
        self.value = value
        self.children = children

    def evaluate(self):
        pass

    def createId():
        Node.i += 1
        return Node.i


class Block(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)

    def evaluate(self):
        for statement in self.children:
            statement.evaluate()

class BinOp(Node):

    def __init__(self, value, children=[]):
        super().__init__(value, children)
        self.id = Node.createId()

    def evaluate(self):
        first = self.children[0].evaluate()
        Assembler.addOutput("PUSH EBX")
        second = self.children[1].evaluate()
        Assembler.addOutput("POP EAX")

        if first[1] == "i32" and second[1] == "i32":

            if self.value == "+":
                Assembler.addOutput("ADD EAX, EBX")
                Assembler.addOutput("MOV EBX, EAX")
                return (first[0] + second[0], "i32")

            elif self.value == "-":
                Assembler.addOutput("SUB EAX, EBX")
                Assembler.addOutput("MOV EBX, EAX")
                return (first[0] - second[0], "i32")

            elif self.value == "*":
                Assembler.addOutput("IMUL EBX")
                Assembler.addOutput("MOV EBX, EAX")
                return (first[0] * second[0], "i32")

            elif self.value == "/":
                Assembler.addOutput("IDIV EBX")
                Assembler.addOutput("MOV EBX, EAX")
                return (int(first[0] // second[0]), "i32")

            elif self.value == "==":
                Assembler.addOutput("CMP EAX, EBX")
                Assembler.addOutput("CALL binop_je")
                return (int(first[0] == second[0]), "i32")

            elif self.value == ">":
                Assembler.addOutput("CMP EAX, EBX")
                Assembler.addOutput("CALL binop_jg")    
                return (int(first[0] > second[0]), "i32")

            elif self.value == "<":
                Assembler.addOutput("CMP EAX, EBX")
                Assembler.addOutput("CALL binop_jl")   
                return (int(first[0] < second[0]), "i32")

            elif self.value == "&&":
                Assembler.addOutput("AND EBX, EAX")
                return (first[0] and second[0], "i32")

            elif self.value == "||":
                Assembler.addOutput("OR EBX, EAX")
                return (first[0] or second[0], "i32")
            
            elif self.value == ".": #o que fazer aqui
                result = str(first[0]) + str(second[0])
                return (str(result), "String")

            else:
                raise Exception("Invalid, operation not defined for BinOp with integers")

        elif first[1] == "String" and second[1] == "String":
            if self.value == ".":#o que fazer aqui
                result = str(first[0]) + str(second[0])
                return (str(result), "String")

            elif self.value == "==":
                Assembler.addOutput("CMP EAX, EBX")
                Assembler.addOutput("CALL binop_je")
                result = str(first[0]) == str(second[0])
                return (int(result), "i32")

            elif self.value == ">":
                Assembler.addOutput("CMP EAX, EBX")
                Assembler.addOutput("CALL binop_jg") 
                result = str(first[0]) > str(second[0])
                return (int(result), "i32")

            elif self.value == "<":
                Assembler.addOutput("CMP EAX, EBX")
                Assembler.addOutput("CALL binop_jl") 
                result = str(first[0]) < str(second[0])
                return (int(result), "i32")

            else:
                raise Exception("Invalid, operation not defined for BinOp with strings")

        elif first[1] == "String" or second[1] == "String":
            if self.value == ".":#o que fazer aqui
                result = str(first[0]) + str(second[0])
                return (str(result), "String")

            elif self.value == "==":
                Assembler.addOutput("CMP EAX, EBX")
                Assembler.addOutput("CALL binop_je")
                return (int(first[0] == second[0]), "i32")

            else:
                raise Exception("Invalid, operation not defined for BinOp with one string and one integer")


class UnOp(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)
        self.id = Node.createId()

    def evaluate(self):
        child = self.children[0].evaluate()

        if child[1] == "i32":    

            if self.value == "+":
                Assembler.addOutput("ADD EBX, 0")
                return (child[0], "i32")
            
            elif self.value == "-":
                Assembler.addOutput("MOV EAX, {}".format(child[0]))
                Assembler.addOutput("MOV EBX, -1")
                Assembler.addOutput("IMUl EBX")
                Assembler.addOutput("MOV EBX, EAX")
                return (-child[0], "i32")

            elif self.value == "!":
                Assembler.addOutput("NEG EBX")
                return (not(child[0]), "i32")

        else:
            raise Exception("Invalid, must be an integer to have UnOp operations")

class IntVal(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)
        self.id = Node.createId()

    def evaluate(self):
        Assembler.addOutput("MOV EBX, {}".format(self.value))
        return (int(self.value), "i32")

class StrVal(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)

    def evaluate(self):
        return (str(self.value), "String")

class VarDec(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)

    def evaluate(self):
        val = self.value
        for identifier in self.children:
            SymbolTable.creator(identifier.value, val)
            Assembler.addOutput("PUSH DWORD 0")  

class While(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)
        self.id = Node.createId()

    def evaluate(self):
        Assembler.addOutput("LOOP_34:")
        first = self.children[0]
        Assembler.addOutput("CMP EBX, False")
        Assembler.addOutput("JE EXIT_34") 
        second = self.children[1]

        while (first.evaluate()[0]):
            second.evaluate()

        Assembler.addOutput("JMP LOOP_34")
        Assembler.addOutput("EXIT_34:")

class If(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)
        self.id = Node.createId()

    def evaluate(self):
        Assembler.addOutput("if_{}:".format(self.id))
        first = self.children[0]
        Assembler.addOutput("CMP EBX, False")

        if len(self.children) > 2:
            Assembler.addOutput("JE Else_{}".format(self.id))
        else:
            Assembler.addOutput("JE EndIf_{}".format(self.id))


        second = self.children[1]
        Assembler.addOutput("JMP EndIf_{}".format(self.id))

        if first.evaluate():
            second.evaluate()

        elif len(self.children) > 2:
            Assembler.addOutput("Else_{}:".format(self.id))
            self.children[2].evaluate()

        Assembler.addOutput("EndIf_{}:".format(self.id))


class NoOp(Node):
    def __init__(self, value, children=[]):
        pass

    def evaluate(self):
        pass

class SymbolTable():


    stat = 0

    @staticmethod
    def creator(name, type):
        SymbolTable.stat+=4
        if name in symbol_table:
            raise Exception("Invalid, variable already declared")
        else:
            symbol_table[name] = [None, type, SymbolTable.stat]
            

    @staticmethod
    def getter(x):
        return symbol_table[x]

    @staticmethod
    def setter(x, y):
        if x in symbol_table: 
            if y[1] == symbol_table[x][1]:
                symbol_table[x][0]= y[0]
            else:
                raise Exception("Invalid, trying to write value on wrongly casted variable")
        else:
            raise Exception("Invalid, variable not declared")

        
class Identifier(Node):

    def evaluate(self):
        Assembler.addOutput("MOV EBX, [EBP-{}]".format(SymbolTable.getter(self.value)[2]))
        var = SymbolTable.getter(self.value)
        return (var[0], var[1])

class Printer(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)

    def evaluate(self):
        print(self.children[0].evaluate()[0])
        Assembler.addOutput("PUSH EBX")
        Assembler.addOutput("CALL print")
        Assembler.addOutput("POP EBX")  

class Reader(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)

    def evaluate(self):
        return (int(input()), "i32")

class Assignment(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)

    def evaluate(self):
        Assembler.addOutput("MOV [EBP-{}], EBX".format(SymbolTable.getter(self.children[0])[2]))
        SymbolTable.setter(self.children[0], self.children[1].evaluate())

class Assembler:
    string_w = ""

    @staticmethod
    def addOutput(content):
        Assembler.string_w += content + "\n"

    @staticmethod
    def create():
        start = """; constantes
    SYS_EXIT equ 1
    SYS_READ equ 3
    SYS_WRITE equ 4
    STDIN equ 0
    STDOUT equ 1
    True equ 1
    False equ 0

    segment .data

    segment .bss  ; variaveis
    res RESB 1

    section .text
    global _start

    print:  ; subrotina print

    PUSH EBP ; guarda o base pointer
    MOV EBP, ESP ; estabelece um novo base pointer

    MOV EAX, [EBP+8] ; 1 argumento antes do RET e EBP
    XOR ESI, ESI

    print_dec: ; empilha todos os digitos
    MOV EDX, 0
    MOV EBX, 0x000A
    DIV EBX
    ADD EDX, '0'
    PUSH EDX
    INC ESI ; contador de digitos
    CMP EAX, 0
    JZ print_next ; quando acabar pula
    JMP print_dec

    print_next:
    CMP ESI, 0
    JZ print_exit ; quando acabar de imprimir
    DEC ESI

    MOV EAX, SYS_WRITE
    MOV EBX, STDOUT

    POP ECX
    MOV [res], ECX
    MOV ECX, res

    MOV EDX, 1
    INT 0x80
    JMP print_next

    print_exit:
    POP EBP
    RET

    ; subrotinas if/while
    binop_je:
    JE binop_true
    JMP binop_false

    binop_jg:
    JG binop_true
    JMP binop_false

    binop_jl:
    JL binop_true
    JMP binop_false

    binop_false:
    MOV EBX, False
    JMP binop_exit
    binop_true:
    MOV EBX, True
    binop_exit:
    RET

    _start:

    PUSH EBP ; guarda o base pointer
    MOV EBP, ESP ; estabelece um novo base pointer

    ; codigo gerado pelo compilador

    """
        finish = """; interrupcao de saida
    POP EBP
    MOV EAX, 1
    INT 0x80
    """
        with open("program.asm", "w") as file:
                file.write(start + Assembler.string_w + finish)  
    
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


            elif self.source[self.position] == ".":
                self.next = Token("DOT", self.source[self.position])

                self.position += 1

                return self.next

            elif self.source[self.position] == ",":
                self.next = Token("COMMA", self.source[self.position])

                self.position += 1

                return self.next

            elif self.source[self.position] == ":":
                self.next = Token("COLON", self.source[self.position])

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

                return self.next

            elif self.source[self.position] == "&" and self.source[self.position+1] == "&":
                self.next = Token("AND", "&&")
                self.position += 2

                return self.next

            elif self.source[self.position] == "=":
                if self.source[self.position+1] == "=":
                    self.next = Token("COMPARE_EQUALS", "==")
                    self.position += 2
                else:
                    self.next = Token("EQUALS", self.source[self.position])

                    self.position += 1

                return self.next

            if self.source[self.position] == "\"":
                var = ""
                self.position+=1
                while self.source[self.position]!= "\"":
                    var += self.source[self.position]
                    self.position+=1

                self.position+=1
                self.next = Token("String", var)
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
                    if id == "String":
                        self.next = Token("type", "String")
                    elif id == "i32":
                        self.next = Token("type", "i32")
                    else:
                        self.next = Token(id, id)
                else:
                    self.next = Token("IDENTIFIER", id)



            else: #futuramente implementar enum pra verificar se é numero mesmo
                if self.source[self.position].isdigit():
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
        while token.next.type == "PLUS" or token.next.type == "MINUS" or token.next.type == "OR":
            value=token.next.value
            token.selectNext()
            result = BinOp(value, [result, Parser.parse_term(token)])

        return result
    
    @staticmethod
    def parse_rel_expression(token):
        result = Parser.parse_expression(token)
        while token.next.type == "BIGGER" or token.next.type == "SMALLER" or token.next.type == "COMPARE_EQUALS" or token.next.type == "DOT":
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

        elif token.next.type == "String":
            value = token.next.value
            result = StrVal(value)
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
            print("ERROR TYPE VARIABLE: {}".format(token.next.type))
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

        elif token.next.type == "var":
            token.selectNext()

            if token.next.type == "IDENTIFIER":
                names = [Identifier(token.next.value)]
                token.selectNext()
                while token.next.type == "COMMA":
                    token.selectNext()
                    if token.next.type == "IDENTIFIER":
                        names.append(Identifier(token.next.value))
                    else:
                        raise Exception("Invalid variable after comma")
                    token.selectNext()
                if token.next.type == "COLON":
                    token.selectNext()
                else:
                    raise Exception("Missing colon after variable names")
                if token.next.type == "type":
                    var_type = token.next.value

                token.selectNext()

                if token.next.type == "SEMICOLON":
                    token.selectNext()
                    return VarDec(var_type, names)
                    
                else:
                    raise Exception("Missing ';'")


            else:
                raise Exception("Invalid variable")


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
    Assembler.create()


main()