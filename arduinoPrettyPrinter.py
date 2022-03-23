class ArduinoVisitor():
    def __init__(self):
        self.header = ""
        self.defines = ""
        self.declarations = ""
        self.setup = "void setup(){\n"
        self.loop = "void loop(){\n"

        self.print = ""

    def pp(self, program):
        self.visitProgram(program)
        self.print = self.header + "\n"+ self.defines + "\n" + self.declarations + "\n" + self.setup + self.loop
        print("\n============ ARDUINO PRETTY PRINTER ============\n")
        print(self.print)
        print("\n========== END ARDUINO PRETTY PRINTER ==========\n")

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

    def visitIntType(self, type):
        self.visit(type.ident)
        self.declarations += self.code + " = "
        self.visit(type.value)
        self.declarations += self.code

    def visitFloatType(self, type):
        self.visit(type.ident)
        self.declarations += self.code + " = "
        self.visit(type.value)
        self.declarations += self.code

    def visitCharType(self, type):
        self.visit(type.ident)
        self.declarations += self.code + " = "
        self.visit(type.value)
        self.declarations += self.code

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