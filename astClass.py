from ast import AST
import re

class ASTNode:
    def accept(self, next):
        class_name_camel_case = self.__class__.__name__
        method_name = getattr(next, "visit" + class_name_camel_case)
        print(class_name_camel_case)
        method_name(self)

class Program(ASTNode):
    def __init__(self, setup = None, main = None):
        self.setup = setup
        self.main = main

class Setup(ASTNode):
    def __init__(self, instances = []):
        self.instances = instances

class Main(ASTNode):
    def __init__(self, declarations = [], statements = []):
        self.declarations = declarations
        self.statements = statements

class Statement(ASTNode):
    def __init__(self, type = None, body = None):
        self.type = type
        self.body = body

class Declaration(ASTNode):
    def __init__(self, type = None, body = None):
        self.type = type
        self.body = body

class Instance(ASTNode):
    def __init__(self, type = None, body = None):
        self.type = type
        self.body = body

class InstanceType(ASTNode):
    def __init__(self, type):
        self.type = type

class SetupBody(ASTNode):
    def __init__(self, types = []):
        self.types = types

class PINType(ASTNode):
    def __init__(self, declarations = []):
        self.declarations = declarations

class ADCType(ASTNode):
    def __init__(self, declarations = []):
        self.declarations = declarations

class SPIType(ASTNode):
    def __init__(self, declaration, cs = []):
        self.declaration = declaration
        self.cs = cs

class I2CType(ASTNode):
    def __init__(self, declaration, slaves = []):
        self.declaration = declaration
        self.slaves = slaves

class SERIALType(ASTNode):
    def __init__(self, baud = None):
        self.baud = baud

class PINDeclaration(ASTNode):
    def __init__(self, new = None, ident = None, pin = None, level = None):
        self.new = new
        self.ident = ident
        self.pin = pin
        self.level = level

class ADCDeclaration(ASTNode):
    def __init__(self, new = None, ident = None, pin = None, level = None):
        self.new = new
        self.ident = ident
        self.pin = pin
        self.level = level

class SPIDeclaration(ASTNode):
    def __init__(self, ident = None, SCK = None, MOSI = None, MISO = None):
        self.ident = ident
        self.SCK = SCK
        self.MOSI = MOSI
        self.MISO = MISO

class CSDeclaration(ASTNode):
    def __init__(self, new = None, ident = None, pin = None):
        self.new = new
        self.ident = ident
        self.pin = pin

class I2CDeclaration(ASTNode):
    def __init__(self, ident = None, SCL = None, SDA = None):
        self.ident = ident
        self.SCL = SCL
        self.SDA = SDA

class SlaveDeclaration(ASTNode):
    def __init__(self, new = None, ident = None, addr = None):
        self.new = new
        self.ident = ident
        self.addr = addr

class Ident(ASTNode):
    def __init__(self, token):
        self.token = token

class IntLit(ASTNode):
    def __init__(self, token):
        self.token = token

class FloatLit(ASTNode):
    def __init__(self, token):
        self.token = token

class TrueLit(ASTNode):
    def __init__(self, token):
        self.token = token

class FalseLit(ASTNode):
    def __init__(self, token):
        self.token = token

class CharLit(ASTNode):
    def __init__(self, token):
        self.token = token

class AnalogLit(ASTNode):
    def __init__(self, token):
        self.token = token

class AdressLit(ASTNode):
    def __init__(self, token):
        self.token = token

class LevelLit(ASTNode):
    def __init__(self, token):
        self.token = token

class IntType(ASTNode):
    def __init__(self, ident = None, value = None):
        self.ident = ident
        self.value = value

class FloatType(ASTNode):
    def __init__(self, ident = None, value = None):
        self.ident = ident
        self.value = value

class CharType(ASTNode):
    def __init__(self, ident = None, value = None):
        self.ident = ident
        self.value = value

class BoolType(ASTNode):
    def __init__(self, ident = None, value = None):
        self.ident = ident
        self.value = value

class If(ASTNode):
    def __init__(self, cond = None, block = None, else_ = None):
        self.cond = cond 
        self.block = block
        self.else_ = else_

class Binary(ASTNode):
    def __init__(self, lhs = None, op = None, rhs = None):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

class Unary(ASTNode):
    def __init__(self, op = None, e = None):
        self.op = op
        self.e = e

class Parenth(ASTNode):
    def __init__(self, e):
        self.e = e

class Block(ASTNode):
    def __init__(self, statements = []):
        self.statements = statements