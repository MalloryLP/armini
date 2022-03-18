import re

class ASTNode:
    def accept(self, next):
        class_name_camel_case = self.__class__.__name__
        method_name = getattr(next, "visit" + class_name_camel_case)
        method_name(self)

class Program(ASTNode):
    def __init__(self, setup = None, main = None):
        self.setup = setup
        self.main = main

class Setup(ASTNode):
    def __init__(self, instances = []):
        self.instances = instances

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

class AnalogLit(ASTNode):
    def __init__(self, token):
        self.token = token

class AdressLit(ASTNode):
    def __init__(self, token):
        self.token = token

class LevelLit(ASTNode):
    def __init__(self, token):
        self.token = token