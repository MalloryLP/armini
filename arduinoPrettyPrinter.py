class ArduinoVisitor():
    def __init__(self):
        self.print = ""
        self.include = ""
        self.define = ""
        self.declarations = ""

        self.setup = "\nvoid setup(){\n"
        self.main = "\nvoid loop(){\n"

    def pp(self, program):
        self.visitProgram(program)
        print("\n============ ARDUINO PRETTY PRINTER ============\n")
        print(self.include + "\n" + self.define + "\n" + self.declarations + self.setup + "}\n" + self.main + "}")
        print("\n========== END ARDUINO PRETTY PRINTER ==========\n")

    def visit(self, node):
        node.accept(self)

    def visitProgram(self, program):
        self.visit(program.setup)
        self.visit(program.main)

    def visitSetup(self, setup):
        for instance in setup.instances:
            self.visit(instance)

    def visitMain(self, main):
        for dcl in main.dcls:
            self.visit(dcl)

    def visitDeclaration(self, dcl):
        self.visit(dcl.type)
        self.declarations += self.print + " "
        self.visit(dcl.name)
        self.declarations += self.print + " "
        self.visit(dcl.value)
        self.declarations += self.print + ";\n"

    def visitPinInstance(self, instance):
        for dcl in instance.dcls:
            self.visit(dcl)

    def visitAdcInstance(self, instance):
        for dcl in instance.dcls:
            self.visit(dcl)

    def visitSpiInstance(self, instance):
        self.include += "#include <SPI.h>\n"
        self.setup += "\n\tSPI.begin();\n"
        self.visit(instance.name)
        self.visit(instance.SCK)
        self.visit(instance.MOSI)
        self.visit(instance.MISO)
        for dcl in instance.dcls:
            self.visit(dcl)

    def visitI2cInstance(self, instance):
        self.include += "#include <Wire.h>\n"
        self.setup += "\n\tWire.begin();\n"
        self.visit(instance.name)
        self.visit(instance.SCK)
        self.visit(instance.SCL)
        for dcl in instance.dcls:
            self.visit(dcl)

    def visitPin(self, pin):
        self.visit(pin.name)
        self.define += "#define " + self.print + " "
        self.setup += "\tpinMode(" + self.print + ","
        self.visit(pin.nb)
        self.define += self.print + "\n"
        self.visit(pin.level)
        self.setup += self.print + ");\n"

    def visitAdc(self, pin):
        self.visit(pin.name)
        self.define += "#define " + self.print + " "
        self.setup += "\tpinMode(" + self.print + ","
        self.visit(pin.nb)
        self.define += self.print + "\n"
        self.visit(pin.level)
        self.setup += self.print + ");\n"

    def visitComponant(self, componant):
        self.visit(componant.name)
        self.define += "#define " + self.print + " "
        self.setup += "\tpinMode(" + self.print + ", OUTPUT);\n"
        self.visit(componant.nb)
        self.define += self.print + "\n"

    def visitSerial(self, serial):
        self.visit(serial.bauds)
        self.setup += "\n\tSerial.begin(" + self.print + ");\n"
        
    def visitIdent(self, ident):
        self.print = ident.token

    def visitIntLit(self, int):
        self.print = int.token

    def visitCharLit(self, int):
        self.print = int.token

    def visitFloatLit(self, int):
        self.print = int.token

    def visitAnalogLit(self, int):
        self.print = int.token

    def visitAdressLit(self, int):
        self.print = int.token
