from pprint import pp
from lexerClass import Lexer
from parserClass import Parser
from visitorClass import Visitor

class Compiler:
    def __init__(self):
        self.lexer = Lexer()
        self.parser = Parser()
        self.visitor = Visitor()
        
    def compile(self, file = None):
        tokens = self.lexer.lex(file)
        print("Lexer analysis successful.")
        ast = self.parser.parse(tokens)
        print("Parser analysis successful.")
        visitor = self.visitor.pp(ast)
        print("Visitor with Pretty Printer analysis successful.")
        

compiler = Compiler()
compiler.compile("armini.txt")