# Sistema Gráfico Interativo 2D/3D

Este projeto é uma implementação de um **Sistema Gráfico Interativo** desenvolvido em Python. Ele permite a criação, visualização e manipulação de objetos gráficos primitivos (pontos, linhas, polígonos) em um ambiente 2D, com suporte a estruturas e transformações 3D projetadas.

O sistema utiliza conceitos fundamentais de Computação Gráfica, como **Coordenadas Homogêneas**, **Transformações Geométricas** (matrizes) e mapeamento **World-to-Viewport**.

## 🚀 Funcionalidades

### 1\. Primitivas Gráficas

O sistema suporta a adição interativa dos seguintes objetos:

  * **Ponto**
  * **Linha** (Reta)
  * **Polilinha** (Sequência de linhas conectadas)
  * **Polígono** (Forma fechada, incluindo suporte básico a objetos 3D como cubos/casas)

### 2\. Transformações Geométricas

Aplicação de transformações em objetos selecionados utilizando operações matriciais:

  * **Translação:** Movimentação nos eixos X, Y e Z.
  * **Rotação:**
      * Em torno da origem.
      * Em torno do centro do objeto (centroide).
      * Em torno de um ponto arbitrário.
      * Escolha de eixos (X, Y, Z).
  * **Escalonamento (Zoom no objeto):** Em relação à origem ou ao centro do objeto.
  * **Reflexão (Espelhamento):** Em torno dos eixos X e Y.
  * **Cisalhamento (Shear):** Distorção nos eixos X e Y.

### 3\. Visualização e Navegação (Viewport)

  * **Windowing:** Mapeamento de coordenadas do mundo real para coordenadas de tela.
  * **Panning:** Movimentação da câmera (Cima, Baixo, Esquerda, Direita).
  * **Zoom:** Aproximação e afastamento da visualização (Zoom In/Out).
  * **Eixos de Referência:** Visualização dos eixos X e Y centrais.

## 🛠️ Tecnologias Utilizadas

  * **Linguagem:** Python 3.x
  * **Interface Gráfica:** `tkinter` (Biblioteca padrão do Python)
  * **Matemática/Cálculo:** `numpy` (Para operações com matrizes de transformação 4x4)

## 📦 Estrutura do Projeto

O projeto é modularizado nas seguintes classes e arquivos:

  * `main.py`: Ponto de entrada da aplicação. Inicializa a janela principal.
  * `graphic_system.py`: O "Core" do sistema. Gerencia a interface principal, a lista de objetos e a comunicação entre os módulos.
  * `viewport.py`: Responsável por converter as coordenadas do "Mundo" para as coordenadas da "Tela" (Canvas).
  * `graphic_object.py` & `polygon3d.py`: Definição das classes dos objetos gráficos e estruturas de dados.
  * `transformations.py`: Contém a lógica matemática. Implementa as matrizes de transformação (Translação, Rotação, Escala, etc.) usando `numpy`.
  * **Interfaces de Usuário:**
      * `add_object_window.py`: Janela para inserção de novos objetos e coordenadas.
      * `transformation_window.py`: Painel de controle para parametrizar e aplicar transformações.
      * `input_window.py`: Interface auxiliar para entrada de dados.
  * `matriz.py`: Um utilitário de terminal para multiplicação de matrizes genéricas (ferramenta auxiliar).

## 📋 Pré-requisitos

Para executar este projeto, você precisará do Python instalado e da biblioteca `numpy`.

1.  **Instalar Python:** [Download Python](https://www.python.org/downloads/)
2.  **Instalar dependências:**
    Abra o terminal e execute:
    ```bash
    pip install numpy
    ```
    *(Nota: O `tkinter` geralmente já vem instalado com o Python. Caso esteja no Linux e dê erro, instale o pacote `python3-tk`).*

## ▶️ Como Executar

1.  Clone ou baixe este repositório.
2.  Navegue até a pasta do projeto via terminal.
3.  Execute o arquivo principal:
    ```bash
    python main.py
    ```

## 🧠 Conceitos Matemáticos Implementados

O sistema utiliza **Matrizes de Transformação Homogênea (4x4)** para manipular os objetos. Isso permite que transformações lineares (escala, rotação) e afins (translação) sejam tratadas de forma unificada através de multiplicação de matrizes.

Exemplo de uma matriz de translação implementada (`transformations.py`):

```python
[ 1  0  0  dx ]
[ 0  1  0  dy ]
[ 0  0  1  dz ]
[ 0  0  0  1  ]
```

## 🤝 Contribuição

Sinta-se à vontade para fazer um fork deste projeto e submeter pull requests. Melhorias sugeridas:

  * Implementação de projeção perspectiva (atualmente ortogonal/projetada simples).
  * Algoritmo de *Clipping* (Recorte de Cohen-Sutherland).
  * Preenchimento de polígonos (Rasterização).

-----

**Autor:** [Seu Nome/Github]
