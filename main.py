from lexerClass import Lexer
from parserClass import Parser
from arminiPrettyPrinter import ArminiVisitor
from arduinoPrettyPrinter import ArduinoVisitor

class Compiler:
    def __init__(self):
        self.lexer = Lexer()
        self.parser = Parser()
        self.arminiPP = ArminiVisitor()
        self.arduinoPP = ArduinoVisitor()
        
    def compile(self, file = None):
        tokens = self.lexer.lex(file)
        print("Lexer analysis successful.")
        ast = self.parser.parse(tokens)
        print("Parser analysis successful.")
        #arminiVisitor = self.arminiPP.pp(ast)
        #print("Armini Pretty Printer analysis successful.")
        arduinoVisitor = self.arduinoPP.pp(ast)
        print("Arduino Pretty Printer analysis successful.")

        arduinoFile = open("armini.ino", "w")
        arduinoFile.write(self.arduinoPP.file)

compiler = Compiler()
compiler.compile("armini.txt")