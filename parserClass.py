import astClass

class Parser:
    def __init__(self):
        pass

    def expect(self, kind):
        next = self.showNext()
        if next.kind == kind:
            self.acceptIt()
        else:
            print("EXPECT ERROR : syntaxe error line : " + str(self.showNext().position))
            exit()
        return next.value

    def showNext(self):
        return self.tokens[0]

    def acceptIt(self):
        self.tokens = self.tokens[1:]
        return self.tokens

    def parse(self, tokens):
        self.tokens = tokens
        ast = self.parse_program()
        return ast
    
    def parse_program(self, level=0):
        program = astClass.Program()
        self.expect("SETUP")
        self.expect("LBRACE")
        program.setup = self.parse_setup()
        self.expect("RBRACE")
        self.expect("PROGRAM")
        self.expect("LBRACE")
        program.main = self.parse_main()
        self.expect("RBRACE")
        return program
    
    def parse_setup(self):
        setup = astClass.Setup()
        while self.showNext().kind in ["PIN", "ADC", "SPI", "I2C", "SERIAL"]:
            setup.instances.append(self.parse_instantiation())
        return setup

    def parse_main(self):
        main = astClass.Main()
        while self.showNext().kind in ["INT", "FLOAT", "CHAR"]:
            main.declarations.append(self.parse_declaration())
        self.expect("LOOP")
        self.expect("LBRACE")
        main.statements = self.parse_statements(main.statements)
        return main

    def parse_statements(self, statements):
        while self.showNext().kind in ["IF"]:
            statements.append(self.parse_statement())
        return statements

    def parse_statement(self):
        CMP = self.showNext()
        if CMP.kind == "IF":
            statement = astClass.Statement(CMP.value, self.parse_if())
        return statement

    def parse_if(self):
        if_ = astClass.If()
        self.acceptIt()
        self.expect("LPAREN")
        if_.cond = self.parse_expression()
        self.expect("RPAREN")
        if_.block = self.parse_block()
        if self.showNext().kind == "ELSE":
            self.acceptIt()
            if_.else_ = self.parse_statement()
        return if_

    def parse_expression(self):
        binary = astClass.Binary()
        print("ICI")
        binary.lhs = self.parse_conjuction()
        while self.showNext().kind  == "DBAR":
            binary.op = self.acceptIt().kind
            binary.rhs = self.parse_conjuction()
        return binary

    def parse_conjuction(self):
        binary = astClass.Binary()
        binary.lhs = self.parse_equality()
        while self.showNext().kind  == "DAMPER":
            binary.op = self.acceptIt().kind
            binary.rhs = self.parse_equality()
        return binary

    def parse_equality(self):
        binary = astClass.Binary()
        binary.lhs = self.parse_relation()
        while self.showNext().kind  in ["DEQ", "NEQ"]:
            binary.op = self.acceptIt().kind
            binary.rhs = self.parse_relation()
        return binary

    def parse_relation(self):
        binary = astClass.Binary()
        binary.lhs = self.parse_addition()
        while self.showNext().kind  in ["LT", "LTE", "GT", "GTE"]:
            binary.op = self.acceptIt().kind
            binary.rhs = self.parse_addition()
        return binary

    def parse_addition(self):
        binary = astClass.Binary()
        binary.lhs = self.parse_term()
        while self.showNext().kind  in ["ADD", "SUB"]:
            binary.op = self.acceptIt().kind
            binary.rhs = self.parse_term()
        return binary

    def parse_term(self):
        binary = astClass.Binary()
        binary.lhs = self.parse_factor()
        while self.showNext().kind  in ["MUL", "DIV"]:
            binary.op = self.acceptIt().kind
            binary.rhs = self.parse_factor()
        return binary

    def parse_factor(self):
        unary = astClass.Unary()
        while self.showNext().kind  in ["SUB", "EXCL"]:
            unary.op = self.acceptIt().kind
        unary.e = self.parse_primary()
        return unary

    def parse_primary(self):
        CMP = self.showNext().kind
        if CMP == "INDENT":
            primary = astClass.Ident(self.acceptIt())
        elif CMP in ["INTEGER_LIT", "TRUE_LIT", "FALSE_LIT", "CHAR_LIT"]:
            if CMP == "INTEGER_LIT":
                primary = astClass.IntLit(self.acceptIt())
            elif CMP == "TRUE_LIT":
                primary = astClass.TrueLit(self.acceptIt())
            elif CMP == "FALSE_LIT":
                primary = astClass.FalseLit(self.acceptIt())
            elif CMP == "CHAR_LIT":
                primary = astClass.CharLit(self.acceptIt())
        elif CMP == "LPAREN":
            self.acceptIt()
            e = self.parse_expression()
            self.expect("RPAREN")
            primary = astClass.Parenth(e)
            return primary
        elif CMP in ["INT", "FLOAT", "CHAR"]:
            type = self.parse_type()
            self.expect("LPAREN")
            e = self.parse_expression()
            self.expect("RPAREN")
            primary = astClass.Cast()
            return primary

    def parse_type(self):
        CMP = self.showNext()
        if CMP.kind == "INT":
            type = astClass.IntType(value = CMP.value)
        elif CMP.kind == "FLOAT":
            type = astClass.FloatType(value = CMP.value)
        elif CMP.kind == "CHAR":
            type = astClass.CharType(value = CMP.value)
        elif CMP.kind == "BOOL":
            type = astClass.BoolType(value = CMP.value)
        return type

    def parse_block(self):
        block = astClass.Block()
        self.expect("LBRACE")
        block.statements = self.parse_statements()
        self.expect("RBRACE")
        return block

    def parse_declaration(self):
        CMP = self.showNext()
        if CMP.kind == "INT":
            declaration = astClass.Declaration(CMP.value, self.parse_int())
        elif CMP.kind == "FLOAT":
            declaration = astClass.Declaration(CMP.value, self.parse_float())
        elif CMP.kind == "CHAR":
            declaration = astClass.Declaration(CMP.value, self.parse_char())
        return declaration
    
    def parse_int(self):
        self.acceptIt()
        int_type = astClass.IntType()
        int_type.ident = astClass.Ident(self.expect("IDENTIFIER"))
        self.expect("ASSIGN")
        int_type.value = astClass.IntLit(self.expect("INTEGER_LIT"))
        return int_type

    def parse_float(self):
        self.acceptIt()
        float_type = astClass.FloatType()
        float_type.ident = astClass.Ident(self.expect("IDENTIFIER"))
        self.expect("ASSIGN")
        float_type.value = astClass.FloatLit(self.expect("FLOAT_LIT"))
        return float_type

    def parse_char(self):
        self.acceptIt()
        float_type = astClass.CharType()
        float_type.ident = astClass.Ident(self.expect("IDENTIFIER"))
        self.expect("ASSIGN")
        float_type.value = astClass.CharLit(self.expect("CHAR_LIT"))
        return float_type

    def parse_instantiation(self):
        CMP = self.showNext().kind
        if CMP == "PIN":
            instance = astClass.Instance(CMP, self.parse_PIN())
        elif CMP == "ADC":
            instance = astClass.Instance(CMP, self.parse_ADC())
        elif CMP == "SPI":
            instance = astClass.Instance(CMP, self.parse_SPI())
        elif CMP == "I2C":
            instance = astClass.Instance(CMP, self.parse_I2C())
        elif CMP == "SERIAL":
            instance = astClass.Instance(CMP, self.parse_SERIAL())
        return instance
            
    def parse_PIN(self):
        self.acceptIt()
        self.expect("LBRACE")
        body = self.parse_PIN_declarations()
        self.expect("RBRACE")
        return body

    def parse_ADC(self):
        self.acceptIt()
        self.expect("LBRACE")
        body = self.parse_ADC_declarations()
        self.expect("RBRACE")
        return body
    
    def parse_SPI(self):
        self.acceptIt()
        self.expect("LBRACE")
        body = self.parse_SPI_declarations()
        self.expect("RBRACE")
        return body

    def parse_I2C(self):
        self.acceptIt()
        self.expect("LBRACE")
        body = self.parse_I2C_declarations()
        self.expect("RBRACE")
        return body

    def parse_SERIAL(self):
        self.acceptIt()
        declaration = astClass.SERIALType()
        self.expect("LBRACE")
        declaration.baud = astClass.IntLit(self.expect("INTEGER_LIT"))
        self.expect("RBRACE")
        return declaration

    def parse_PIN_declarations(self):
        pin = astClass.PINType()
        while self.showNext().kind == "new":
            pin.declarations.append(self.parse_PIN_declaration())
        return pin

    def parse_PIN_declaration(self):
        declaration = astClass.PINDeclaration()
        declaration.new = self.expect("new")
        declaration.ident = astClass.Ident(self.expect("IDENTIFIER"))
        self.expect("COLON")
        declaration.pin = astClass.IntLit(self.expect("INTEGER_LIT"))
        self.expect("COMMA")
        if self.showNext().kind in ["OUTPUT", "INPUT"]:
            declaration.level = astClass.LevelLit(self.showNext().kind)
            self.acceptIt()
        return declaration

    def parse_ADC_declarations(self):
        adc = astClass.ADCType()
        while self.showNext().kind == "new":
            adc.declarations.append(self.parse_ADC_declaration())
        return adc

    def parse_ADC_declaration(self):
        declaration = astClass.PINDeclaration()
        declaration.new = self.expect("new")
        declaration.ident = astClass.Ident(self.expect("IDENTIFIER"))
        self.expect("COLON")
        declaration.pin = astClass.AnalogLit(self.expect("ANALOG_LIT"))
        self.expect("COMMA")
        declaration.level = astClass.LevelLit(self.expect("INPUT"))
        return declaration

    def parse_SPI_declarations(self):
        spi = astClass.SPIType(self.parse_SPI_declaration(), [])
        while self.showNext().kind == "new":
            spi.cs.append(self.parse_SPI_component())
        return spi
        
    def parse_SPI_declaration(self):
        declaration = astClass.SPIDeclaration()
        declaration.ident = astClass.Ident(self.expect("IDENTIFIER"))
        self.expect("COLON")
        declaration.SCK = astClass.IntLit(self.expect("INTEGER_LIT"))
        self.expect("COMMA")
        declaration.MOSI = astClass.IntLit(self.expect("INTEGER_LIT"))
        self.expect("COMMA")
        declaration.MISO = astClass.IntLit(self.expect("INTEGER_LIT"))
        return declaration

    def parse_SPI_component(self):
        cs = astClass.CSDeclaration()
        cs.new = self.expect("new")
        cs.ident = astClass.Ident(self.expect("IDENTIFIER"))
        self.expect("COLON")
        cs.pin = astClass.Ident(self.expect("INTEGER_LIT"))
        return cs

    def parse_I2C_declarations(self):
        i2c = astClass.I2CType(self.parse_I2C_declaration(), [])
        while self.showNext().kind == "new":
            i2c.slaves.append(self.parse_I2C_componant())
        return i2c

    def parse_I2C_declaration(self):
        declaration = astClass.I2CDeclaration()
        declaration.ident = astClass.Ident(self.expect("IDENTIFIER"))
        self.expect("COLON")
        declaration.SCL = astClass.IntLit(self.expect("INTEGER_LIT"))
        self.expect("COMMA")
        declaration.SDA = astClass.IntLit(self.expect("INTEGER_LIT"))
        return declaration

    def parse_I2C_componant(self):
        slave = astClass.SlaveDeclaration()
        slave.new = self.expect("new")
        slave.ident = astClass.Ident(self.expect("IDENTIFIER"))
        self.expect("COLON")
        slave.addr = astClass.AdressLit(self.expect("ADRESS_LIT"))
        return slave

    
