class ReportGenerator:
    def __init__(self):
        # for every type of error we have a list
        self.lexicos = []
        self.sintacticos = []
        self.estructura = []
        self.consistencia = []
        self.advertencias = []
    # methods to add errors and warnings
    def agregar_lexicos(self, lista):
        self.lexicos.extend(lista)

    def agregar_sintactico(self, error):
        self.sintacticos.append(str(error))

    def agregar_estructura(self, error):
        self.estructura.append(str(error))

    def agregar_consistencia(self, error):
        self.consistencia.append(str(error))

    def agregar_advertencia(self, advertencia):
        self.advertencias.append(str(advertencia))

    # method to check if there are any errors that should stop the program
    # that errors are lexical and syntactic errors
    def hay_errores_graves(self):
        return len(self.lexicos) > 0 or len(self.sintacticos) > 0

    def imprimir_reporte(self):
        print("\n Reporte: ")

        # we print each type of error 
        if self.lexicos:
            print("\nErrores léxicos:")
            for e in self.lexicos:
                print(e)
        if self.sintacticos:
            print("\nErrores sintacticos:")
            for e in self.sintacticos:
                print(e)
        if self.estructura:
            print("\nErrores de estructura:")
            for e in self.estructura:
                print(e)

        if self.consistencia:
            print("\nErrores de consistencia:")
            for e in self.consistencia:
                print(e)
        if self.advertencias:
            print("\nAdvertencias:")
            for a in self.advertencias:
                print(a)
        # if there are no errors at all, we print that there are no errors
        if not any([self.lexicos, self.sintacticos, self.estructura, self.consistencia]):
            print("\n No se encontraron errores.")
