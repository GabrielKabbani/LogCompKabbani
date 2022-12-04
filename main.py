import symbol
import sys
import re

reserved_words = ["Print", "Read", "while", "if", "else", "var", "i32", "String", "fn", "return"]
func_table = {}

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Node:
    def __init__(self, value, children = []):
        self.value = value
        self.children = children

    def evaluate(self, st):
        pass

class Block(Node):

    def evaluate(self, st):
        for statement in self.children:
            statement.evaluate(st)

class BinOp(Node):
    def evaluate(self, st):
        first = self.children[0].evaluate(st)
        second = self.children[1].evaluate(st)

        if first[1] == "i32" and second[1] == "i32":

            if self.value == "+":
                return (first[0] + second[0], "i32")

            elif self.value == "-":
                return (first[0] - second[0], "i32")

            elif self.value == "*":
                return (first[0] * second[0], "i32")

            elif self.value == "/":
                return (int(first[0] // second[0]), "i32")

            elif self.value == "==":
                return (int(first[0] == second[0]), "i32")

            elif self.value == ">":
                return (int(first[0] > second[0]), "i32")

            elif self.value == "<":
                return (int(first[0] < second[0]), "i32")

            elif self.value == "&&":
                return (first[0] and second[0], "i32")

            elif self.value == "||":
                return (first[0] or second[0], "i32")
            
            elif self.value == ".":
                result = str(first[0]) + str(second[0])
                return (str(result), "String")

            else:
                raise Exception("Invalid, operation not defined for BinOp with integers")

        elif first[1] == "String" and second[1] == "String":
            if self.value == ".":
                result = str(first[0]) + str(second[0])
                return (str(result), "String")

            elif self.value == "==":
                result = str(first[0]) == str(second[0])
                return (int(result), "i32")

            elif self.value == ">":
                result = str(first[0]) > str(second[0])
                return (int(result), "i32")

            elif self.value == "<":
                result = str(first[0]) < str(second[0])
                return (int(result), "i32")

            else:
                raise Exception("Invalid, operation not defined for BinOp with strings")

        elif first[1] == "String" or second[1] == "String":
            if self.value == ".":
                result = str(first[0]) + str(second[0])
                return (str(result), "String")

            elif self.value == "==":
                return (int(first[0] == second[0]), "i32")

            else:
                raise Exception("Invalid, operation not defined for BinOp with one string and one integer")


class UnOp(Node):
    def evaluate(self, st):
        child = self.children[0].evaluate(st)

        if child[1] == "i32":    

            if self.value == "+":
                return (child[0], "i32")
            
            elif self.value == "-":
                return (-child[0], "i32")

            elif self.value == "!":
                return (not(child[0]), "i32")

        else:
            raise Exception("Invalid, must be an integer to have UnOp operations")

class IntVal(Node):
    def evaluate(self, st):
        return (int(self.value), "i32")

class StrVal(Node):
    def evaluate(self, st):
        return (str(self.value), "String")

class VarDec(Node):
    def evaluate(self, st):
        val = self.value
        for identifier in self.children:
            print("NAME 3: {}".format(identifier.value))
            st.creator(identifier.value, val)

class While(Node):
    def evaluate(self, st):
        first = self.children[0]
        second = self.children[1]

        while (first.evaluate(st)[0]):
            second.evaluate(st)

class If(Node):
    def evaluate(self, st):
        first = self.children[0]
        second = self.children[1]
        if first.evaluate(st):
            second.evaluate(st)

        elif len(self.children) > 2:
            self.children[2].evaluate(st)


class NoOp(Node):
    def evaluate(self, st):
        pass

class FuncTable:

    @staticmethod
    def creator(type, name, ref):
        if name in func_table:
            raise Exception("Invalid, variable already declared")

        else:
            func_table[name] = [type, ref]

    @staticmethod
    def getter(name):
        if name not in func_table:
            raise Exception("Invalid, variable already declared + {}".format(name))
        
        return func_table[name][1]


class SymbolTable():

    def __init__(self):
        self.symbol_table = {}


    def creator(self, name, type):
        if name in self.symbol_table:
            raise Exception("Invalid, variable already declared + {}".format(name))
        else:
            self.symbol_table[name] = (None, type)
            


    def getter(self,x):
        return self.symbol_table[x]


    def setter(self, x, y):
        if x in self.symbol_table: 
            if y[1] == self.symbol_table[x][1]:
                self.symbol_table[x] = y
            else:
                raise Exception("Invalid, trying to write value on wrongly casted variable")
        else:
            raise Exception("Invalid, variable not declared")

class FuncDec(Node):
    def evaluate(self, st):
        vardec = self.children[0]
        type = self.value

        FuncTable.creator(type, vardec, self)

class FuncCall(Node):
    def evaluate(self, st):
        name = self.value

        funcdec = FuncTable.getter(name)
        st_current = SymbolTable()

        id = funcdec.children[0]
        block = funcdec.children[-1]
        args = funcdec.children[1:len(funcdec.children)-1]
    
        if id == "Main":
            return block.evaluate(st_current)
        else:
            if (len(funcdec.children) - 2) == len(self.children):

                for dec, attribute in zip(args, self.children):
                    print("NAME 1: {}".format(dec.children[0]))
                    st_current.creator(dec.children[0], dec.value)

                    if attribute.value in st.symbol_table:
                        type = st.getter(attribute.value)[1]
                        print("NAME 2: {}".format(attribute.value))
                        st_current.creator(attribute.value, type)
                        st_current.setter(attribute.value, st.getter(attribute.value))
                        st_current.setter(dec.children[0], st.getter(attribute.value))
                    else:
                        st_current.setter(dec.children[0], attribute.evaluate(st_current))
            
                return block.evaluate(st_current)
            else:
                raise Exception("Wrong # of function arguments")

class Return(Node):
    def evaluate(self, st):
        return self.children.evaluate(st)
        
class Identifier(Node):

    def evaluate(self, st):
        var = st.getter(self.value)
        return (var[0], var[1])

class Printer(Node):

    def evaluate(self, st):
        print(self.children[0].evaluate(st)[0])

class Reader(Node):

    def evaluate(self, st):
        return (int(input()), "i32")

class Assignment(Node):

    def evaluate(self, st):
        st.setter(self.children[0], self.children[1].evaluate(st))
    
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

                if self.source[self.position + 1] == ">":
                    self.next = Token("ARROW", self.source[self.position])

                    self.position += 2

                else:

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


class Parser: #deve ter coisa errada na parse_declaration, e acho que a functable ta errada pq n tem a brisa do endereco e falta o bagulho do ->
    
    def __init__(self, token):
        self.token = token

    @staticmethod
    def parse_program(token):
        nodes = []
        while (token.next.type != "EOF"):
            nodes.append(Parser.parse_declaration(token))
        
        return Block("Block", nodes)

    @staticmethod
    def parse_declaration(token):
        if token.next.type == "fn":
            children = []
            token.selectNext()
            if token.next.type == "IDENTIFIER":
                func_id = token.next.value

                children.append(func_id)
                token.selectNext()
                
                if token.next.type == "PAR_OPEN":
                    token.selectNext()

                    while token.next.type != "PAR_CLOSE":
                        if token.next.type == "IDENTIFIER":
                            current_id = [token.next.value]
                            token.selectNext()
                            while token.next.type == "COMMA":
                                token.selectNext()
                                if token.next.type == "IDENTIFIER":
                                    current_id.append(token.next.value)
                                    token.selectNext()

                            if token.next.type == "COLON":
                                token.selectNext()
                                type = token.next.value
                                children.append(VarDec(type, current_id))
                            else:
                                raise Exception("Missing type of argument")

                            if token.next.value != "i32" and token.next.value !="String":
                                raise Exception("unrecognized type: {}".format(token.next.value))

                            token.selectNext()

                        if token.next.type == "COMMA":
                            token.selectNext()

                    token.selectNext()

                    if token.next.type == "ARROW":
                        token.selectNext()
                        if token.next.value != "i32" and token.next.value !="String":
                                raise Exception("unrecognized type: {}".format(token.next.value))
                        type = token.next.value
                        token.selectNext()
                        children.append(Parser.parse_block(token))
                        result = FuncDec(func_id, children)
                        result.value = type
                        return result


                    children.append(Parser.parse_block(token))
                    result = FuncDec(func_id, children)
                    return result




                
                else:
                    raise Exception("Missing opening parenthesis in function")

            else:
                raise Exception("Missing function id")


            

            
        else:
            raise Exception("Missing fn declaration")


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
            
            id = token.next.value
            result = Identifier(id)
            token.selectNext()

            if token.next.type == "PAR_OPEN":

                args =[]
                token.selectNext()
                while token.next.type != "PAR_CLOSE":
                    args.append(Parser.parse_rel_expression(token))
                    if token.next.type == "COMMA":
                        token.selectNext()

                result = FuncCall(id, args)
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
                    raise Exception("Missing ';'" + token.next.value)
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

        elif token.next.type == "return":

            token.selectNext()

            return Return('return', Parser.parse_rel_expression(token))


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
        output = Parser.parse_program(tokens)
        output.children.append(FuncCall("Main", []))


        if output != None and tokens.next.type == "EOF":
            tempo_st = SymbolTable
            output.evaluate(tempo_st)
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