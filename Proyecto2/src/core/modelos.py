class Perro:
    def __init__(self, id_perro, sexo, celo, enfermo):
        self.id = id_perro
        self.sexo = sexo # M o H
        self.celo = celo # true o false
        self.enfermo = enfermo # true o false

class Instancia:
    def __init__(self, n, perros):
        self.n = n # tamaño de la cuadricula N x N
        self.perros = perros # lista de objetos Perro
        self.p = len(perros) # cantidad de perros

class Solucion:
    def __init__(self, posiciones):
        # indica en que perrera esta el perro i
        self.posiciones = posiciones