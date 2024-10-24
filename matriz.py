class Matriz:
    def __init__(self, linhas, colunas, preenche=True):
        self.linhas = linhas
        self.colunas = colunas
        if preenche:
            self.matriz = self.criar_matriz()
        else:
            self.matriz = [[0] * colunas for _ in range(linhas)]

    def criar_matriz(self):
        matriz = []
        print(f"Digite os elementos da matriz {self.linhas}x{self.colunas}:")
        for i in range(self.linhas):
            linha = []
            for j in range(self.colunas):
                valor = float(input(f"Elemento [{i+1},{j+1}]: "))
                linha.append(valor)
            matriz.append(linha)
        return matriz

    def __str__(self):
        result = ""
        for linha in self.matriz:
            result += " ".join([f"{elemento:.2f}" for elemento in linha]) + "\n"
        return result

    def multiplicar(self, outra):
        if self.colunas != outra.linhas:
            raise ValueError("Multiplicação impossível: número de colunas da primeira matriz deve ser igual ao número de linhas da segunda matriz.")

        # Criar a matriz resultado sem solicitar entrada do usuário
        resultado = Matriz(self.linhas, outra.colunas, preenche=False)

        for i in range(self.linhas):
            for j in range(outra.colunas):
                for k in range(self.colunas):
                    resultado.matriz[i][j] += self.matriz[i][k] * outra.matriz[k][j]

        return resultado

def main():
    # Entrada para a primeira matriz
    linhas1 = int(input("Número de linhas da primeira matriz: "))
    colunas1 = int(input("Número de colunas da primeira matriz: "))
    matriz1 = Matriz(linhas1, colunas1)

    # Entrada para a segunda matriz
    linhas2 = int(input("Número de linhas da segunda matriz: "))
    colunas2 = int(input("Número de colunas da segunda matriz: "))
    matriz2 = Matriz(linhas2, colunas2)

    # Exibe as matrizes
    print("\nMatriz 1:")
    print(matriz1)

    print("Matriz 2:")
    print(matriz2)

    # Tentativa de multiplicação
    try:
        resultado = matriz1.multiplicar(matriz2)
        print("Resultado da multiplicação:")
        print(resultado)
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
