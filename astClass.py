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

class Main(ASTNode):
    def __init__(self, dcls = [], body = []):
        self.dcls = dcls
        self.body = body

class Declaration(ASTNode):
    def __init__(self, type = None, name = None, value = None):
        self.type = type
        self.name = name
        self.value = value

class PinInstance(ASTNode):
    def __init__(self, dcls = []):
        self.dcls = dcls

class AdcInstance(ASTNode):
    def __init__(self, dcls = []):
        self.dcls = dcls

class SpiInstance(ASTNode):
    def __init__(self, name = None, SCK = None, MOSI = None, MISO = None, dcls = []):
        self.name = name
        self.SCK = SCK
        self.MOSI = MOSI
        self.MISO = MISO
        self.dcls = dcls

class I2cInstance(ASTNode):
    def __init__(self, name = None, SCK = None, SCL = None, dcls = []):
        self.name = name
        self.SCK = SCK
        self.SCL = SCL
        self.dcls = dcls

class Pin(ASTNode):
    def __init__(self, name = None, nb = None, level = None):
        self.name = name
        self.nb = nb
        self.level = level

class Adc(ASTNode):
    def __init__(self, name = None, nb = None, level = None):
        self.name = name
        self.nb = nb
        self.level = level

class Componant(ASTNode):
    def __init__(self, name = None, nb = None):
        self.name = name
        self.nb = nb

class Serial(ASTNode):
    def __init__(self, bauds = None):
        self.bauds = bauds

class Ident(ASTNode):
    def __init__(self, token):
        self.token = token

class Assign(ASTNode):
    def __init__(self, lhs = None, op = None, rhs = None):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

class Binary(ASTNode):
    def __init__(self, lhs = None, op = None, rhs = None):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

class If(ASTNode):
    def __init__(self, cond = None, body = None, else_ = None):
        self.cond = cond 
        self.body = body
        self.else_ = else_

class While(ASTNode):
    def __init__(self, cond = None, body = None):
        self.cond = cond 
        self.body = body

class Set(ASTNode):
    def __init__(self, pin = None, level = None):
        self.pin = pin
        self.level = level
    
class Read(ASTNode):
    def __init__(self, data = None):
        self.data = data

class SendSerial(ASTNode):
    def __init__(self, data = None):
        self.data = data

class SendI2c(ASTNode):
    def __init__(self, data = None, slave = None):
        self.data = data
        self.slave = slave

class SendSpi(ASTNode):
    def __init__(self, data = None, slave = None):
        self.data = data
        self.slave = slave

class IntLit(ASTNode):
    def __init__(self, token):
        self.token = token

class CharLit(ASTNode):
    def __init__(self, token):
        self.token = token

class FloatLit(ASTNode):
    def __init__(self, token):
        self.token = token

class AnalogLit(ASTNode):
    def __init__(self, token):
        self.token = token

class AdressLit(ASTNode):
    def __init__(self, token):
        self.token = token

class OpLit(ASTNode):
    def __init__(self, token):
        self.token = token