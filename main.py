from lexerClass import Lexer
from parserClass import Parser
from visitorClass import Visitor
from arduinoPrettyPrinter import ArduinoVisitor

class Compiler:
    def __init__(self):
        self.lexer = Lexer()
        self.parser = Parser()
        self.arminiPP = Visitor()
        self.arduinoPP = ArduinoVisitor()
        
    def compile(self, file = None):
        tokens = self.lexer.lex(file)
        print("Lexer analysis successful.")
        ast = self.parser.parse(tokens)
        print("Parser analysis successful.")
        #visitor = self.arminiPP.pp(ast)
        #print("Visitor with Pretty Printer analysis successful.")
        #print(self.arminiPP.code)
        visitor = self.arduinoPP.pp(ast)
        print("Visitor with Pretty Printer analysis successful.")
        

compiler = Compiler()
compiler.compile("armini.txt")