from traceback import print_tb


class Visitor:
    def __init__(self):
        self.code = [] #variable d'instance qui récupère tous les mots clés (useless)
        self.print = "" #variable d'instance pour le pretty printer

    def visit(self, node):
        node.accept(self)

    def pp(self, program):
        self.visitProgram(program)
        print(self.code)
        print("\n============ PRETTY PRINTER ============\n")
        print(self.print)
        print("\n========== END PRETTY PRINTER ==========\n")

    def visitProgram(self, program):
        self.code.append("SETUP")
        self.print += "SETUP{"
        self.visit(program.setup)
        self.print += "\n}"
        self.code.append("PROGRAM")
        self.print += "\nPROGRAM{\n"
        self.visit(program.main)
        self.print += "\n}"
        
    def visitSetup(self, setup):
        for instance in setup.instances:
            self.visit(instance)
            self.print += "\n\t}"

    def visitMain(self, main):
        for declaration in main.declarations:
            self.visit(declaration)
        self.code.append("LOOP")
        self.print += "\n\tLOOP{\n"
        for statement in main.statements:
            self.visit(statement)
        self.print += "\n\t}\n"

    def visitStatement(self, statement):
        self.code.append(statement.type)
        if statement.type is not None:
            self.print += "\t\t" + statement.type
        else:
            self.print += "\t\t"
        self.visit(statement.body)

    def visitIf(self, if_):
        self.visit(if_.cond)
        for block in if_.block:
            self.print += "\n\t\t\t"
            self.visit(block)
        self.print += "}"
        if if_.else_ is not None:
            self.print += "else{\n"
            for block in if_.else_:
                self.visit(block)
            self.print += "\t\t}\n"
    
    def visitWhile(self, while_):
        self.visit(while_.cond)
        for block in while_.block:
            self.print += "\n\t\t"
            self.visit(block)
        self.print += "\n\t\t}"
        

    def visitSetPin(self, declaration):
        self.code.append(declaration.set)
        self.print += " "
        self.visit(declaration.ident)
        self.print += "to"
        self.print += " "
        self.visit(declaration.level)

    def visitPrintSerial(self, serial):
        self.code.append(serial.serial)
        self.print += "("
        self.visit(serial.ident)
        self.print += ")"
        self.print += "\n"
  

   
    def visitCond(self, cond):
        self.print += "( "
        self.visit(cond.lhs)
        self.visit(cond.op)
        self.visit(cond.rhs)
        self.print += "){\n"

    def visitAssignation(self, assign):
        self.visit(assign.lhs)
        self.visit(assign.op)
        self.visit(assign.rhs)
        self.print += "\n"

    def visitExpression(self, exp):
        self.visit(exp.lhs)
        if exp.op is not None:
            self.visit(exp.op)
        if exp.rhs is not None:
            self.visit(exp.rhs)
        self.print += "\n"

    def visitDeclaration(self, declaration):
        self.code.append(declaration.type)
        self.print += "\t" + declaration.type + " "
        self.visit(declaration.body)

    def visitType(self, type):
        self.visit(type.ident)
        if type.array is not None:
            self.print += "["
            self.visit(type.array)
            self.print += "]"
        self.print += "= "
        self.visit(type.value)
        self.print += "\n"

   
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

    def visitFloatLit(self, float):
        self.code.append(float.token)
        self.print += float.token + " "

    def visitCharLit(self, char):
        self.code.append(char.token)
        self.print += char.token + " "

    def visitAnalogLit(self, analog):
        self.code.append(analog.token)
        self.print += analog.token + " "

    def visitAdressLit(self, addr):
        self.code.append(addr.token)
        self.print += addr.token + " "

    def visitLevelLit(self, level):
        self.code.append(level.token)
        self.print += level.token + " "

    def visitOpLit(self, level):
        self.code.append(level.token)
        self.print += level.token + " "
    