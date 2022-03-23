class ArduinoVisitor():
    def __init__(self):
        self.print = ""

    def pp(self, program):
        self.visitProgram(program)
        print("\n============ ARDUINO PRETTY PRINTER ============\n")
        print(self.print)
        print("\n========== END ARDUINO PRETTY PRINTER ==========\n")

    def visit(self, node):
        node.accept(self)

    def visitProgram(self, program):
        self.visit(program.setup)

    def visitSetup(self, setup):
        for instance in setup.instances:
            self.visit(instance)

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

    def visitPINDeclaration(self, declaration):
        self.print += "#define "
        self.visit(declaration.ident)
        self.print += " "
        self.visit(declaration.pin)
        self.print += "\n"

    def visitSPIDeclaration(self, declaration):
        self.print = "#include <SPI.h>\n" + self.print

    def visitI2CDeclaration(self, declaration):
        self.print = "#include <Wire.h>\n" + self.print

    def visitCSDeclaration(self, cs):
        self.print += "#define "
        self.visit(cs.ident)
        self.print += " "
        self.visit(cs.pin)
        self.print += "\n"

    def visitIdent(self, ident):
        self.print += ident.token

    def visitIntLit(self, int):
        self.print += int.token

    def visitAnalogLit(self, analog):
        self.print += analog.token