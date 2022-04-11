from time import sleep


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
        print(self.include + "\n" + self.define + "\n" + self.declarations + self.setup + "}\n" + self.main + "\n}")
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
        for stm in main.body:
            self.visit(stm)
            self.main += "\n"

    def visitIf(self, if_):
        self.main += "\tif("
        self.visit(if_.cond)
        self.main += self.print
        self.main += "){\n"
        for stm in if_.body:
            self.main += "\t"
            self.visit(stm)
        self.main += "\t}"
        if if_.else_:
            self.main += "else{\n"
            for stm in if_.else_:
                self.main += "\t"
                self.visit(stm)
            self.main += "\t}"
        else:
            self.main += "\n"

    def visitWhile(self, while_):
        self.main += "\twhile("
        self.visit(while_.cond)
        self.main += "){\n"
        for stm in while_.body:
            self.main += "\t"
            self.visit(stm)
        self.main += "\t}\n"

    def visitRead(self, read):
        self.visit(read.data)
        self.declarations += "int " + self.print + "_value = 0;\n"
        self.main += "\t" + self.print + "_value = analogRead(" + self.print + ");\n"

    def visitSet(self, set_):
        self.visit(set_.pin)
        self.main += "\tdigitalWrite(" + str(self.print) + "," + set_.level + ");\n"

    def visitSendSerial(self, serial):
        self.visit(serial.data)
        self.main += "\tSerial.print(" + self.print + "_value);\n"

    def visitSendI2c(self, i2c):
        self.visit(i2c.data)
        data = self.print
        self.visit(i2c.slave)
        self.main += "\tWire.beginTransmission(" + self.print +");\n"
        self.main += "\tWire.write(" + data +");\n"
        self.main += "\tWire.endTransmission(" + self.print +");\n"

    def visitSendSpi(self, spi):
        self.visit(spi.slave)
        self.main += "\tdigitalWrite(" + self.print + ",LOW);\n"
        slave = self.print
        self.visit(spi.data)
        self.main += "\tSPI.transfert(" + self.print +");\n"
        self.main += "\tdigitalWrite(" + slave + ",HIGH);\n"


    def visitAssign(self, assign):
        self.visit(assign.lhs)
        self.main += "\t" + self.print
        self.visit(assign.op)
        self.main += self.print
        self.visit(assign.rhs)
        self.main += self.print
        self.main += ";\n"

    def visitBinary(self, binary):
        self.visit(binary.lhs)
        self.main += self.print
        if binary.op:
            self.visit(binary.op)
            self.main += self.print
            self.visit(binary.rhs)
            

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
            self.setup += "\tdigitalWrite(" + self.print + ",HIGH);\n"

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
        name = self.print
        self.define += "#define " + self.print + " "
        self.setup += "\tpinMode(" + self.print + ", OUTPUT);\n"
        self.visit(componant.nb)
        self.define += self.print + "\n"
        self.print = name

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

    def visitOpLit(self, int):
        self.print = int.token