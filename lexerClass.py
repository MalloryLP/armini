import re
import sys

regexExpressions = [
    (r'[ \n\t]+', None),
    (r'#[^\n]*', None),
    (r'SETUP\b', 'SETUP'),
    (r'PROGRAM\b', 'PROGRAM'),
    (r'LOOP\b', 'LOOP'),
    (r'new\b', 'new'),
    (r'PIN\b', 'PIN'),
    (r'ADC\b', 'ADC'),
    (r'SPI\b', 'SPI'),
    (r'I2C\b', 'I2C'),
    (r'SERIAL\b', 'SERIAL'),
    (r'INPUT\b', 'INPUT'),
    (r'OUTPUT\b', 'OUTPUT'),
    (r'HIGH\b', 'HIGH'),
    (r'LOW\b', 'LOW'),
    (r'to\b', 'TO'),
    (r'true\b', 'TRUE_LIT'),
    (r'false\b', 'FALSE_LIT'),
    (r'if\b', 'IF'),
    (r'else\b', 'ELSE'),
    (r'while\b', 'WHILE'),
    (r'int\b', 'INT'),
    (r'char\b', 'CHAR'),
    (r'bool\b', 'BOOL'),
    (r'float\b', 'FLOAT'),
    (r'\(', 'LPAREN'),
    (r'\)', 'RPAREN'),
    (r'\{', 'LBRACE'),
    (r'\}', 'RBRACE'),
    (r'\[', 'LBRACK'),
    (r'\]', 'RBRACK'),
    (r'\;', 'SEMICOLON'),
    (r'\:', 'COLON'),
    (r'\,', 'COMMA'),
    (r'\/\*', 'LCOMMENT'),
    (r'\*\/', 'RCOMMENT'),
    (r'\/\/(.*)', 'COMMENT'),
    (r'\.', 'DOT'),
    (r'\=', 'ASSIGN'),
    (r'\+', 'ADD'),
    (r'\-', 'SUB'),
    (r'\*', 'MUL'),
    (r'\/', 'DIV'),
    (r'\<', 'LT'),
    (r'\<\=', 'LTE'),
    (r'\>', 'GT'),
    (r'\>\=', 'GTE'),
    (r'\&\&', 'DAMPER'),
    (r'\|\|', 'DBAR'),
    (r'\=\=', 'DEQ'),
    (r'\!\=', 'NEQ'),
    (r'\=', 'ASSIGN'),
    (r'[A]\d+', 'ANALOG_LIT'),
    (r'0x\d+', 'ADRESS_LIT'),
    (r'[a-zA-Z][a-zA-Z0-9]*', 'IDENTIFIER'),
    (r'\d+\.\d+', 'FLOAT_LIT'),
    (r'\d+', 'INTEGER_LIT'),
    (r'\"[^\"]*\"', 'CHAR_LIT')
    
]

class Token:
	def __init__(self, kind, value, position):
		self.kind = kind
		self.value = value
		self.position = position

class Lexer:
    def __init__(self):
        self.tokens = []
        self.file = None

    def lex(self, file):
        self.file = open(file).readlines()
        lineNumber = 0
        for line in self.file:
            lineNumber += 1
            position = 0
            while position < len(line):
                match = None
                for tokenRegex in regexExpressions:
                    pattern, tag = tokenRegex
                    regex = re.compile(pattern)
                    match = regex.match(line, position)
                    if match:
                        data = match.group(0)
                        if tag:
                            token = Token(tag, data, [lineNumber, position])
                            self.tokens.append(token)
                        break
                if not match:
                    print(self.file[position])
                    print("no match")
                    sys.exit(1)
                else:
                    position = match.end(0)
        return self.tokens
