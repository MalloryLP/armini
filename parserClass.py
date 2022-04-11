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
            print("Expected : ", kind, "  but have : ", next.kind)
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
    
    def parse_program(self):
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
            setup.instances.append(self.parse_instantiations())
        return setup
    
    def parse_main(self):
        main = astClass.Main()
        while self.showNext().kind in ["INT", "CHAR", "FLOAT"]:
            main.dcls.append(self.parse_type_declarations())
        self.expect("LOOP")
        self.expect("LBRACE")
        while self.showNext().kind in ["IDENTIFIER", "IF", "WHILE", "SET", "READ", "SERIAL", "I2C", "SPI"]:
                main.body.append(self.parse_statements())
        self.expect("RBRACE")
        return main

    def parse_statements(self):
        CMP = self.showNext().kind
        if CMP == "IDENTIFIER":
            statement = self.parse_assignation()
        elif CMP == "IF":
            statement = self.parse_if()
        elif CMP == "WHILE":
            statement = self.parse_while()
        elif CMP == "SET":
            statement = self.parse_set()
        elif CMP == "READ":
            statement = self.parse_read()
        elif CMP == "SERIAL":
            statement = self.parse_serial()
        elif CMP == "I2C":
            statement = self.parse_i2c()
        elif CMP == "SPI":
            statement = self.parse_spi()
        return statement

    def parse_spi(self):
        spi = astClass.SendSpi()
        self.expect("SPI")
        self.expect("LPAREN")
        spi.data = astClass.Ident(self.expect("IDENTIFIER"))
        self.expect("TO")
        spi.slave = astClass.Ident(self.expect("IDENTIFIER"))
        self.expect("RPAREN")
        return spi

    def parse_i2c(self):
        i2c = astClass.SendI2c()
        self.expect("I2C")
        self.expect("LPAREN")
        i2c.data = astClass.Ident(self.expect("IDENTIFIER"))
        self.expect("TO")
        i2c.slave = astClass.Ident(self.expect("IDENTIFIER"))
        self.expect("RPAREN")
        return i2c

    def parse_serial(self):
        serial = astClass.SendSerial()
        self.acceptIt()
        self.expect("LPAREN")
        serial.data = astClass.Ident(self.expect("IDENTIFIER"))
        self.expect("RPAREN")
        return serial

    def parse_read(self):
        read = astClass.Read()
        self.acceptIt()
        read.data = astClass.Ident(self.expect("IDENTIFIER"))
        return read

    def parse_set(self):
        set_ = astClass.Set()
        self.acceptIt()
        set_.pin = astClass.Ident(self.expect("IDENTIFIER"))
        self.expect("TO")
        CMP = self.showNext().kind
        if CMP in ["HIGH", "LOW"]:
            self.acceptIt()
            set_.level = CMP
        return set_

    def parse_block(self):
        block = []
        while self.showNext().kind in ["IDENTIFIER", "IF", "WHILE", "SET", "READ", "SERIAL", "I2C", "SPI"]:
            block.append(self.parse_statements())
        return block

    def parse_if(self):
        if_ = astClass.If()
        self.acceptIt()
        self.expect("LPAREN")
        if_.cond = self.parse_binary()
        self.expect("RPAREN")
        self.expect("LBRACE")
        while self.showNext().kind in ["IDENTIFIER", "IF", "WHILE", "SET", "READ", "SERIAL", "I2C", "SPI"]:
            if_.body = self.parse_block()
        self.expect("RBRACE")
        if self.showNext().kind == "ELSE":
            self.acceptIt()
            self.expect("LBRACE")
            while self.showNext().kind in ["IDENTIFIER", "IF", "WHILE", "SET", "READ", "SERIAL", "I2C", "SPI"]:
                if_.else_ = self.parse_block()
            self.expect("RBRACE")
        return if_

    def parse_while(self):
        while_ = astClass.While()
        self.acceptIt()
        self.expect("LPAREN")
        while_.cond = self.parse_binary()
        self.expect("RPAREN")
        self.expect("LBRACE")
        while self.showNext().kind in ["IDENTIFIER", "IF", "WHILE", "SET", "READ", "SERIAL", "I2C", "SPI"]:
            while_.body = self.parse_block()
        self.expect("RBRACE")
        return while_

    def parse_assignation(self):
        assign = astClass.Assign()
        assign.lhs = astClass.Ident(self.expect("IDENTIFIER"))
        assign.op = astClass.OpLit(self.expect("ASSIGN"))
        assign.rhs = self.parse_binary()
        return assign

    def parse_binary(self):
        binary = astClass.Binary()
        CMP = self.showNext().kind
        if CMP in ["INTEGER_LIT", "CHAR_LIT", "FLOAT_LIT", "IDENTIFIER"]:
            if CMP == "IDENTIFIER":
                binary.lhs = astClass.Ident(self.expect("IDENTIFIER"))
            elif CMP == "CHAR_LIT":
                binary.lhs = astClass.CharLit(self.expect("CHAR_LIT"))
            elif CMP == "FLOAT_LIT":
                binary.lhs = astClass.FloatLit(self.expect("FLOAT_LIT"))
            elif CMP == "INTEGER_LIT":
                binary.lhs = astClass.IntLit(self.expect("INTEGER_LIT"))
        CMP = self.showNext()
        if CMP.kind in ["ADD", "SUB", "MUL", "DIV", "LT", "LTE", "GT", "GTE"]:
            binary.op = astClass.OpLit(CMP.value)
            self.acceptIt()
            CMP = self.showNext().kind
            if CMP in ["INTEGER_LIT", "CHAR_LIT", "FLOAT_LIT", "IDENTIFIER"] and self.tokens[1].kind not in ["ADD", "SUB", "MUL", "DIV"]:
                if CMP == "IDENTIFIER":
                    binary.rhs = astClass.Ident(self.expect("IDENTIFIER"))
                elif CMP == "CHAR_LIT":
                    binary.rhs = astClass.CharLit(self.expect("CHAR_LIT"))
                elif CMP == "FLOAT_LIT":
                    binary.rhs = astClass.FloatLit(self.expect("FLOAT_LIT"))
                elif CMP == "INTEGER_LIT":
                    binary.rhs = astClass.IntLit(self.expect("INTEGER_LIT"))
            else:
                binary.rhs = self.parse_binary()
        return binary


    def parse_type_declarations(self):
        CMP = self.showNext().kind
        if CMP == "INT":
            declaration = self.parse_int_declarations()
        if CMP == "CHAR":
            declaration = self.parse_char_declarations()
        if CMP == "FLOAT":
            declaration = self.parse_float_declarations()
        return declaration

    def parse_int_declarations(self):
        var = astClass.Declaration()
        var.type = astClass.Ident(self.expect("INT"))
        var.name = astClass.Ident(self.expect("IDENTIFIER"))
        self.expect("ASSIGN")
        var.value = astClass.IntLit(self.expect("INTEGER_LIT"))
        return var

    def parse_char_declarations(self):
        var = astClass.Declaration()
        var.type = astClass.Ident(self.expect("CHAR"))
        var.name = astClass.Ident(self.expect("IDENTIFIER"))
        self.expect("ASSIGN")
        var.value = astClass.CharLit(self.expect("CHAR_LIT"))
        return var

    def parse_float_declarations(self):
        var = astClass.Declaration()
        var.type = astClass.Ident(self.expect("FLOAT"))
        var.name = astClass.Ident(self.expect("IDENTIFIER"))
        self.expect("ASSIGN")
        var.value = astClass.FloatLit(self.expect("FLOAT_LIT"))
        return var

    def parse_instantiations(self):
        CMP = self.showNext().kind
        if CMP == "PIN":
            self.acceptIt()
            instance = self.parse_pins_declaration()
        if CMP == "ADC":
            self.acceptIt()
            instance = self.parse_adcs_declaration()
        if CMP == "SPI":
            self.acceptIt()
            instance = self.parse_spis_declaration()
        if CMP == "I2C":
            self.acceptIt()
            instance = self.parse_i2cs_declaration()
        if CMP == "SERIAL":
            self.acceptIt()
            instance = self.parse_serial_declaration()
        return instance
    
    def parse_pins_declaration(self):
        pin = astClass.PinInstance()
        self.expect("LBRACE")
        while self.showNext().kind == "new":
            pin.dcls.append(self.parse_pin_declaration())
        self.expect("RBRACE")
        return pin

    def parse_adcs_declaration(self):
        adc = astClass.AdcInstance()
        self.expect("LBRACE")
        while self.showNext().kind == "new":
            adc.dcls.append(self.parse_adc_declaration())
        self.expect("RBRACE")
        return adc

    def parse_spis_declaration(self):
        spi = astClass.SpiInstance()
        self.expect("LBRACE")
        spi.name = astClass.Ident(self.expect("IDENTIFIER"))
        self.expect("COLON")
        spi.SCK = astClass.IntLit(self.expect("INTEGER_LIT"))
        self.expect("COMMA")
        spi.MISO = astClass.IntLit(self.expect("INTEGER_LIT"))
        self.expect("COMMA")
        spi.MOSI = astClass.IntLit(self.expect("INTEGER_LIT"))
        while self.showNext().kind == "new":
            spi.dcls.append(self.parse_spi_declaration())
        self.expect("RBRACE")
        return spi

    def parse_i2cs_declaration(self):
        spi = astClass.I2cInstance()
        self.expect("LBRACE")
        spi.name = astClass.Ident(self.expect("IDENTIFIER"))
        self.expect("COLON")
        spi.SCK = astClass.IntLit(self.expect("INTEGER_LIT"))
        self.expect("COMMA")
        spi.SCL = astClass.IntLit(self.expect("INTEGER_LIT"))
        while self.showNext().kind == "new":
            spi.dcls.append(self.parse_i2c_declaration())
        self.expect("RBRACE")
        return spi
    
    def parse_pin_declaration(self):
        declaration = astClass.Pin()
        self.expect("new")
        declaration.name = astClass.Ident(self.expect("IDENTIFIER"))
        self.expect("COLON")
        declaration.nb = astClass.IntLit(self.expect("INTEGER_LIT"))
        self.expect("COMMA")
        if self.showNext().kind in ["OUTPUT", "INPUT"]:
            declaration.level = astClass.Ident(self.showNext().kind)
            self.acceptIt()
        return declaration

    def parse_adc_declaration(self):
        declaration = astClass.Adc()
        self.expect("new")
        declaration.name = astClass.Ident(self.expect("IDENTIFIER"))
        self.expect("COLON")
        declaration.nb = astClass.AnalogLit(self.expect("ANALOG_LIT"))
        self.expect("COMMA")
        if self.showNext().kind in ["OUTPUT", "INPUT"]:
            declaration.level = astClass.Ident(self.showNext().kind)
            self.acceptIt()
        return declaration

    def parse_spi_declaration(self):
        declaration = astClass.Componant()
        self.expect("new")
        declaration.name = astClass.Ident(self.expect("IDENTIFIER"))
        self.expect("COLON")
        declaration.nb = astClass.IntLit(self.expect("INTEGER_LIT"))
        return declaration

    def parse_i2c_declaration(self):
        declaration = astClass.Componant()
        self.expect("new")
        declaration.name = astClass.Ident(self.expect("IDENTIFIER"))
        self.expect("COLON")
        declaration.nb = astClass.AdressLit(self.expect("ADRESS_LIT"))
        return declaration

    def parse_serial_declaration(self):
        declaration = astClass.Serial()
        self.expect("LBRACE")
        declaration.bauds = astClass.AdressLit(self.expect("INTEGER_LIT"))
        self.expect("RBRACE")
        return declaration