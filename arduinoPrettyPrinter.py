from numpy import block


class ArduinoVisitor():
    def __init__(self):
        self.header = ""
        self.defines = ""
        self.declarations = ""
        self.setup = "void setup(){\n"
        self.loop = "void loop(){\n"

        self.analog = {}

        self.print = ""

        self.debug = []

    def pp(self, program):
        self.visitProgram(program)
        self.print = self.header + "\n"+ self.defines + "\n" + self.declarations + "\n" + self.setup + self.loop
        print("\n============ ARDUINO PRETTY PRINTER ============\n")
        print(self.print)
        print("\n========== END ARDUINO PRETTY PRINTER ==========\n")
        print(self.debug)

    def visit(self, node):
        node.accept(self)

    def visitProgram(self, program):
        self.visit(program.setup)
        self.visit(program.main)

    def visitSetup(self, setup):
        for instance in setup.instances:
            self.visit(instance)
        self.setup += "}\n\n"

    def visitMain(self, main):
        for declaration in main.declarations:
            self.visit(declaration)
        for statement in main.statements:
            self.visit(statement)
            print("test")

    def visitStatement(self, statement):
        CMP = statement.type
        self.debug.append(CMP)
        self.loop += "\t"
        if CMP == "read":
            self.visit(statement.body)
            self.analog[self.code] = self.code + "_value"
            self.declarations += "int " + self.analog[self.code] + " = 0;\n"
            self.loop += self.analog[self.code] + " = analogRead(" + self.code + ");\n"
        elif CMP == "serial":
            self.visit(statement.body)
        elif CMP == "set":
            self.visit(statement.body)
        elif CMP == "if":
            self.visit(statement.body)
        elif CMP == "while":
            self.visit(statement.body)

    def visitIf(self, if_):
        self.loop += "if("
        self.visit(if_.cond)
        for statement in if_.block:
            self.loop += "\t"
            self.visit(statement)
        self.loop += "\t}"
        if if_.else_ is not None:
            self.loop += "else{\n"
            for statement in if_.else_:
                self.loop += "\t"
                self.visit(statement)
            self.loop += "\t}\n"

    def visitWhile(self, while_):
        self.loop += "while("
        self.visit(while_.cond)
        for statement in while_.block:
            self.loop += "\t"
            self.visit(statement)
        self.loop += "\t}\n"

    def visitCond(self, cond):
        self.visit(cond.lhs)
        CMP = self.analog.get(self.code)
        if CMP is not None:
            self.loop += CMP
        else:
            self.loop += self.code
        self.visit(cond.op)
        self.loop += self.code
        self.visit(cond.rhs)
        self.loop += self.code + "){\n"

    def visitSetPin(self, pin):
        self.visit(pin.ident)
        self.loop += "digitalWrite("+ self.code + ","
        self.visit(pin.level)
        self.loop += self.code + ");\n"

    def visitPrintSerial(self, serial):
        self.visit(serial.ident)
        self.loop += "Serial.print(" + self.code + ");\n"

    def visitInstance(self, instance):
        CMP = instance.type
        if CMP == "PIN":
            self.visit(instance.body)
        elif CMP == "ADC":
            self.visit(instance.body)
        elif CMP == "SPI":
            self.visit(instance.body)
        elif CMP == "I2C":
            self.visit(instance.body)
        elif CMP == "SERIAL":
            self.visit(instance.body)

    def visitPINType(self, type):
        for declaration in type.declarations:
            self.visit(declaration)

    def visitADCType(self, type):
        for declaration in type.declarations:
            self.visit(declaration)

    def visitSPIType(self, type):
        self.visit(type.declaration)
        for cs in type.cs:
            self.visit(cs)

    def visitI2CType(self, type):
        self.visit(type.declaration)
        for slave in type.slaves:
            self.visit(slave)

    def visitSERIALType(self, type):
        self.visit(type.baud)
        self.setup += "\tSerial.begin(" + self.code + ");\n"

    def visitPINDeclaration(self, declaration):
        self.defines += "#define "
        self.setup += "\tpinMode("
        self.visit(declaration.ident)
        self.defines += self.code + " "
        self.setup += self.code + ","
        self.visit(declaration.pin)
        self.defines += self.code + "\n"
        self.visit(declaration.level)
        self.setup += self.code + ");\n"

    def visitSPIDeclaration(self, declaration):
        self.header += "#include <SPI.h>\n"

    def visitI2CDeclaration(self, declaration):
        self.header += "#include <Wire.h>\n"
        self.setup += "\tWire.begin();\n"

    def visitCSDeclaration(self, cs):
        self.defines += "#define "
        self.visit(cs.ident)
        self.defines += self.code + " "
        self.visit(cs.pin)
        self.defines += self.code + "\n"

    def visitSlaveDeclaration(self, slave):
        self.defines += "#define "
        self.visit(slave.ident)
        self.defines += self.code + " "
        self.visit(slave.addr)
        self.defines += self.code + "\n"

    def visitDeclaration(self, declaration):
        self.declarations += declaration.type + " "
        self.visit(declaration.body)
        self.declarations += ";\n"

    def visitType(self, type):
        self.visit(type.ident)
        self.declarations += self.code + " = "
        self.visit(type.value)
        self.declarations += self.code

    def visitAssignation(self, assignation):
        self.visit(assignation.lhs)
        self.loop += "\t" + self.code + " = "
        self.visit(assignation.exp)
    
    def visitExpression(self, exp):
        self.visit(exp.lhs)
        self.loop += self.code
        if exp.op is not None:
            self.visit(exp.op)
            self.loop += self.code
        if exp.rhs is not None:
            self.visit(exp.rhs)
            self.loop += self.code
        self.loop += ";\n"

    def visitIdent(self, ident):
        self.code = ident.token

    def visitIntLit(self, int):
        self.code = int.token

    def visitFloatLit(self, float):
        self.code = float.token

    def visitCharLit(self, char):
        self.code = char.token

    def visitAnalogLit(self, analog):
        self.code = analog.token

    def visitLevelLit(self, level):
        self.code = level.token

    def visitAdressLit(self, addr):
        self.code = addr.token

    def visitOpLit(self, addr):
        self.code = addr.token
    
