class ArminiVisitor():
    def __init__(self):
        self.print = ""
        self.include = ""
        self.define = ""
        self.declarations = ""

        self.setup = "\nvoid setup(){\n"
        self.main = "\nvoid loop(){\n"

        self.file = None

        self.tab = "\t"

    def pp(self, program):
        self.visitProgram(program)
        print("\n============ ARMINI PRETTY PRINTER ============\n")
        self.file = self.include + "\n" + self.define + "\n" + self.declarations + self.setup + "}\n" + self.main + "\n}"
        print(self.file)
        print("\n========== END ARMINI PRETTY PRINTER ==========\n")

    def visit(self, node):
        node.accept(self)

    def visitProgram(self, program):
        self.visit(program.setup)
        self.visit(program.main)