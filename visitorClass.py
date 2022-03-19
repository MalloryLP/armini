class Visitor:
    def __init__(self):
        self.code = [] #variable d'instance qui récupère tous les mots clés (useless)
        self.print = "" #variable d'instance pour le pretty printer

    def visit(self, node):
        node.accept(self)

    def pp(self, program):
        self.visitProgram(program)
        print("\n============ PRETTY PRINTER ============\n")
        print(self.print)
        print("\n========== END PRETTY PRINTER ==========\n")

    def visitProgram(self, program):
        self.code.append("SETUP")
        self.print += "SETUP{"
        self.visit(program.setup)
        #self.visit(program.main)
        
    def visitSetup(self, setup):
        for instance in setup.instances:
            self.visit(instance)
            self.print += "\n\t}"

    def visitInstance(self, instance):
        self.code.append(instance.type)
        self.print += "\n\t" + instance.type + "{"
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
        self.print += "\n\t\t"
        self.visit(type.baud)

    def visitPINDeclaration(self, declaration):
        self.code.append(declaration.new)
        self.print += "\n\t\t" + declaration.new + " "
        self.visit(declaration.ident)
        self.visit(declaration.pin)
        self.visit(declaration.level)

    def visitADCDeclaration(self, declaration):
        self.code.append(declaration.new)
        self.print += "\n\t\t" + declaration.new + " "
        self.visit(declaration.ident)
        self.visit(declaration.pin)
        self.visit(declaration.level)

    def visitSPIDeclaration(self, declaration):
        self.print += "\n\t\t"
        self.visit(declaration.ident)
        self.visit(declaration.SCK)
        self.visit(declaration.MOSI)
        self.visit(declaration.MISO)

    def visitI2CDeclaration(self, declaration):
        self.print += "\n\t\t"
        self.visit(declaration.ident)
        self.visit(declaration.SCL)
        self.visit(declaration.SDA)

    def visitCSDeclaration(self, cs):
        self.print += "\n\t\t"
        self.code.append(cs.new)
        self.visit(cs.ident)
        self.visit(cs.pin)

    def visitSlaveDeclaration(self, slave):
        self.print += "\n\t\t"
        self.code.append(slave.new)
        self.visit(slave.ident)
        self.visit(slave.addr)

    def visitIdent(self, ident):
        self.code.append(ident.token)
        self.print += ident.token + " "

    def visitIntLit(self, int):
        self.code.append(int.token)
        self.print += int.token + " "

    def visitAnalogLit(self, analog):
        self.code.append(analog.token)
        self.print += analog.token + " "

    def visitAdressLit(self, addr):
        self.code.append(addr.token)
        self.print += addr.token + " "

    def visitLevelLit(self, level):
        self.code.append(level.token)
        self.print += level.token + " "
    