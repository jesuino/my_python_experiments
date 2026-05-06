from enum import Enum
from collections import deque

N_CANIBAIS = 3
N_MISSIONARIOS = 3
CAP_BARCO = 3


class Lado(Enum):
    DIREITO = 0
    ESQUERDO = 1

    def outro(self):
        return Lado.ESQUERDO if self.value == Lado.DIREITO.value else Lado.DIREITO


class Estado:
    def __init__(self, m, c, l):
        self.m = m
        self.c = c
        self.l = l

    def __str__(self):
        return f"M{self.m},C{self.c},{self.l.name}"

    @staticmethod
    def inicial():
        return Estado(N_MISSIONARIOS, N_CANIBAIS, Lado.ESQUERDO)

    def eh_solucao(self):
        return (
            self.m == 0
            and self.c == 0
            and self.l == Lado.ESQUERDO
            or self.m == N_MISSIONARIOS
            and self.c == N_CANIBAIS
            and self.l == Lado.DIREITO
        )

    def eh_valido(self):
        outro = self.outro()
        return (self.m >= self.c or self.m == 0) and (
            outro.m >= outro.c or outro.m == 0
        )

    def imprimir(self):
        print(f" {self} | {self.outro()}")

    def outro(self):
        return Estado(N_MISSIONARIOS - self.m, N_CANIBAIS - self.c, self.l.outro())

    def transportados(self, novo):
        if novo.m == self.m and novo.c == self.c:
            return 0
        t_missionarios = novo.m - self.outro().m
        t_canibais = novo.c - self.outro().c
        return t_missionarios + t_canibais

    def proximos(self):
        novos = []
        # gera todas as possibilidades de acordo com a capacidade do barco
        for i in range(CAP_BARCO + 1):
            prox_m = (self.outro().m + i) if self.m != 0 else N_MISSIONARIOS
            for j in range(CAP_BARCO + 1):
                prox_c = (self.outro().c + j) if self.c != 0 else N_CANIBAIS
                novo = Estado(prox_m, prox_c, self.outro().l)
                novos.append(novo)
                if prox_c == N_CANIBAIS or self.c == 0:
                    break
            if prox_m == N_MISSIONARIOS or self.m == 0:
                break
        novos = [
            n for n in novos if n.eh_valido() and 0 < self.transportados(n) <= CAP_BARCO
        ]
        return novos


class Arvore:
    def __init__(self, estado):
        self.raiz = No(None, estado)

    def resolver(self):
        n, no_final = self.busca_largura()
        if no_final is None:
            raise Exception("Não foi possível encontrar uma solução")
        return n, no_final

    def busca_largura(self, max_nos=300):
        fila = deque([self.raiz])
        visitados = 0
        while fila and visitados < max_nos:
            visitados += 1
            no = fila.popleft()
            if no.estado.eh_solucao():
                return visitados, no
            if not no.filhos:
                no.abrir()
            fila.extend(no.filhos)


class No:
    def __init__(self, pai, estado, filhos=None):
        self.pai = pai
        self.estado = estado
        self.filhos = filhos

    def abrir(self):
        self.filhos = [No(self, f) for f in self.estado.proximos()]
        return self.filhos

    def caminho(self):
        caminho = []
        no = self
        while no is not None:
            caminho.append(no.estado)
            no = no.pai
        return caminho[::-1]

    def caminho_str(self):
        caminho = self.caminho()
        return " -> ".join(str(c) for c in caminho)


# inicial = Estado(0, 1, Lado.ESQUERDO)
inicial = Estado.inicial()

# Usado para debugar a geração de estados
# proximos = inicial.proximos()
# for p in proximos:
#      print(f'  >{p}')
#      _proximos = p.proximos()
#      for pp in _proximos:
#          print(f'    >{pp}')

arvore = Arvore(inicial)
nos_visitados, solucao = arvore.resolver()
print(f"Solução encontrada após visitar {nos_visitados} nós: \n{solucao.caminho_str()}")
