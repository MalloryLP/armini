class PrettyPrinter:
    def __init__(self):
        self.code = None

    def pp(self, prog):
        self.visitProgram(prog)
        print(self.code)

    def visitProgram(self, program):
        self.code="program\n"
        #k=program.setup.accept(self)
        k=""
        self.code+="\t"+k
        
        
    def visitSetup(self,setup):
        pass