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

    