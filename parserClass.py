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
        pass

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

    
