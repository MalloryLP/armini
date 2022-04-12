import argparse
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
        
    def compile(self, inputFile = None, outputFile = None):
        tokens = self.lexer.lex(inputFile)
        print("Lexer analysis successful.")
        ast = self.parser.parse(tokens)
        print("Parser analysis successful.")
        #arminiVisitor = self.arminiPP.pp(ast)
        #print("Armini Pretty Printer analysis successful.")
        arduinoVisitor = self.arduinoPP.pp(ast)
        print("Arduino Pretty Printer analysis successful.")

        open(outputFile, "w").close()
        arduinoFile = open(outputFile, "w")
        arduinoFile.write(self.arduinoPP.file)
        arduinoFile.close()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This program compiles a program in Armini language into Arduino to simplify your work.", epilog="Program realized in the compilation course",formatter_class=argparse.RawTextHelpFormatter)
    
    parser.add_argument("-i", "--input_file", help=".txt armini code input file", required=True)
    parser.add_argument("-o", "--output_file", help=".ino arduino code output file", required=True)

    args = parser.parse_args()

    compiler = Compiler()
    compiler.compile(args.input_file, args.output_file)