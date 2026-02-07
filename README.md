# Sistema Gráfico Interativo 2D/3D

> Implementação de um sistema gráfico educacional com suporte a primitivas 2D e estruturas 3D projetadas

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![NumPy](https://img.shields.io/badge/NumPy-013243?logo=numpy&logoColor=white)](https://numpy.org/)
[![tkinter](https://img.shields.io/badge/GUI-tkinter-yellow)](https://docs.python.org/3/library/tkinter.html)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🚀 Sobre o Projeto

Este projeto é uma implementação educacional de um **Sistema Gráfico Interativo** desenvolvido em Python. Ele permite a criação, visualização e manipulação de objetos gráficos primitivos (pontos, linhas, polígonos) em um ambiente 2D, com suporte a estruturas 3D projetadas.

O sistema utiliza conceitos fundamentais de **Computação Gráfica**, com foco em **paradigma funcional** através de transformações matriciais puras e composição de operações geométricas.

### 🎯 Destaques Técnicos

- **Paradigma Funcional:** Todas as transformações são funções puras (matrizes 4x4)
- **Matemática Rigorosa:** Coordenadas homogêneas e álgebra linear aplicada
- **Composição de Transformações:** Múltiplas operações combinadas via multiplicação matricial
- **Arquitetura Modular:** Separação clara entre lógica matemática e interface gráfica
- **Zero Efeitos Colaterais:** Objetos nunca são modificados in-place, apenas transformados

---

## 💡 Funcionalidades

### 1. Primitivas Gráficas

O sistema suporta a criação interativa dos seguintes objetos:

| Primitiva | Descrição | Exemplo de Uso |
|-----------|-----------|----------------|
| **Ponto** | Coordenada única (x, y) | Marcadores, referências |
| **Linha** | Reta entre dois pontos | Bordas, conexões |
| **Polilinha** | Sequência de linhas conectadas | Caminhos, contornos |
| **Polígono** | Forma fechada | Formas 2D, projeções 3D |
| **Polígono 3D** | Estruturas como cubos, casas | Visualização 3D básica |

### 2. Transformações Geométricas

Todas as transformações são implementadas como **funções puras** que retornam novas matrizes 4x4:

#### ✅ Translação
```python
# Função pura: retorna matriz de transformação
def translation_matrix(dx, dy, dz):
    return np.array([
        [1, 0, 0, dx],
        [0, 1, 0, dy],
        [0, 0, 1, dz],
        [0, 0, 0, 1 ]
    ])
```

#### ✅ Rotação
- Em torno da **origem**
- Em torno do **centro do objeto** (centroide)
- Em torno de um **ponto arbitrário**
- Escolha de eixos: **X, Y, Z**

```python
# Composição funcional: rotação ao redor do centro
def rotate_around_center(object, angle, axis):
    center = calculate_centroid(object)  # Puro
    
    # Composição de 3 transformações puras
    T1 = translation_matrix(-center.x, -center.y, 0)
    R  = rotation_matrix(angle, axis)
    T2 = translation_matrix(center.x, center.y, 0)
    
    # Multiplicação de matrizes (associativa, comutativa para rotações)
    return T2 @ R @ T1  # Operador @ = np.matmul
```

#### ✅ Escalonamento
- Em relação à **origem**
- Em relação ao **centro do objeto**

#### ✅ Transformações Avançadas
- **Reflexão (Espelhamento):** Eixos X e Y
- **Cisalhamento (Shear):** Distorção nos eixos X e Y

### 3. Visualização e Navegação (Viewport)

#### Window-to-Viewport Mapping

```python
# Função pura: World Coordinates → Screen Coordinates
def world_to_viewport(point, world_window, viewport):
    # Transformação afim pura
    sx = (viewport.width / world_window.width)
    sy = (viewport.height / world_window.height)
    
    screen_x = (point.x - world_window.x_min) * sx
    screen_y = (point.y - world_window.y_min) * sy
    
    return Point(screen_x, screen_y)
```

#### Controles de Navegação
- **Panning:** ⬆️ ⬇️ ⬅️ ➡️ (movimentação da câmera)
- **Zoom:** 🔍 Zoom In/Out
- **Eixos de Referência:** Visualização dos eixos X e Y

---

## 🛠️ Arquitetura Funcional

O projeto segue uma arquitetura que separa **cálculos puros** de **efeitos colaterais**:

```
┌─────────────────────────────────────────┐
│          Interface (tkinter)            │  ← Efeitos colaterais (I/O)
│         graphic_system.py               │
└──────────────┬──────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│      Camada de Apresentação              │
│         viewport.py                      │  ← Mapeamento World→Screen
└──────────────┬───────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│    Transformações (Funções Puras)        │
│      transformations.py                  │  ← Álgebra linear pura
│   - translation_matrix()                 │
│   - rotation_matrix()                    │
│   - scale_matrix()                       │
│   - compose_transformations()            │
└──────────────┬───────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│      Objetos Gráficos (Dados)            │
│    graphic_object.py, polygon3d.py       │  ← Estruturas imutáveis
└──────────────────────────────────────────┘
```

### Paradigma Funcional Aplicado

#### ✅ **Funções Puras**
Todas as transformações são determinísticas:

```python
# ANTES (Imperativo - mutação)
def rotate_object(obj, angle):
    obj.points = apply_rotation(obj.points, angle)  # ❌ Mutação!

# DEPOIS (Funcional - imutável)
def rotate_object(obj, angle):
    rotation_matrix = build_rotation_matrix(angle)  # Puro
    new_points = transform_points(obj.points, rotation_matrix)  # Puro
    return Object(new_points)  # Novo objeto, original intacto
```

#### ✅ **Composição de Transformações**
Múltiplas transformações são combinadas via multiplicação de matrizes:

```python
# Composição funcional
def complex_transform(obj):
    T1 = translation_matrix(10, 0, 0)
    R  = rotation_matrix(45, 'Z')
    S  = scale_matrix(2, 2, 1)
    
    # Composição: T1 ∘ R ∘ S
    final_matrix = T1 @ R @ S
    
    return apply_matrix(obj, final_matrix)
```

#### ✅ **Separação de Efeitos**
- **Puro:** Cálculos matemáticos (`transformations.py`)
- **Impuro:** Renderização na tela (`graphic_system.py`)

---

## 📊 Conceitos Matemáticos Implementados

### Coordenadas Homogêneas (4x4)

Permite unificar transformações lineares e afins:

```python
# Ponto em coordenadas homogêneas
point = [x, y, z, 1]

# Matriz de transformação genérica 4x4
T = [
    [a, b, c, tx],  # Linha 1: escala/rotação + translação X
    [d, e, f, ty],  # Linha 2: escala/rotação + translação Y
    [g, h, i, tz],  # Linha 3: escala/rotação + translação Z
    [0, 0, 0, 1 ]   # Linha 4: coordenada homogênea
]

# Transformação
new_point = T @ point  # Multiplicação matriz-vetor
```

### Exemplos de Matrizes

#### Translação
```python
T(dx, dy, dz) = [
    [1, 0, 0, dx],
    [0, 1, 0, dy],
    [0, 0, 1, dz],
    [0, 0, 0, 1 ]
]
```

#### Rotação (eixo Z)
```python
R_z(θ) = [
    [cos(θ), -sin(θ), 0, 0],
    [sin(θ),  cos(θ), 0, 0],
    [0,       0,      1, 0],
    [0,       0,      0, 1]
]
```

#### Escala
```python
S(sx, sy, sz) = [
    [sx, 0,  0,  0],
    [0,  sy, 0,  0],
    [0,  0,  sz, 0],
    [0,  0,  0,  1]
]
```

---

## 🚀 Como Executar

### 1. Pré-requisitos

- Python 3.8 ou superior
- tkinter (geralmente já vem com Python)

**Linux:** Se tkinter não estiver instalado:
```bash
sudo apt-get install python3-tk  # Debian/Ubuntu
```

### 2. Instalação

Clone o repositório e instale as dependências:

```bash
git clone https://github.com/joaov-godinho/sistemagrafico.git
cd sistemagrafico
pip install -r requirements.txt
```

### 3. Execução

```bash
python main.py
```

### 4. Interface de Uso

1. **Adicionar Objetos:** Clique em "Adicionar Objeto" e selecione a primitiva
2. **Aplicar Transformações:** Selecione um objeto e clique em "Transformar"
3. **Navegação:**
   - Use os botões de seta para mover a viewport
   - Use Zoom In/Out para aproximar/afastar

---

## 📁 Estrutura do Projeto

```
sistemagrafico/
├── main.py                      # Ponto de entrada
├── graphic_system.py            # Interface principal (tkinter)
├── viewport.py                  # World-to-Screen mapping (puro)
├── transformations.py           # Matrizes de transformação (puro)
├── graphic_object.py            # Classes de objetos gráficos
├── polygon3d.py                 # Estruturas 3D
├── add_object_window.py         # UI: adicionar objetos
├── transformation_window.py     # UI: aplicar transformações
├── input_window.py              # UI: entrada de dados
├── matriz.py                    # Utilitário: multiplicação de matrizes
└── README.md
```

---

## 🧪 Exemplos de Uso

### Criar um Quadrado e Rotacioná-lo

```python
# 1. Criar quadrado em (0,0) com lado 100
square = Polygon([
    Point(0, 0),
    Point(100, 0),
    Point(100, 100),
    Point(0, 100)
])

# 2. Rotacionar 45° ao redor do centro
center = calculate_centroid(square)  # Puro: (50, 50)

T1 = translation_matrix(-50, -50, 0)    # Move para origem
R  = rotation_matrix(45, 'Z')           # Rotaciona
T2 = translation_matrix(50, 50, 0)      # Volta para posição original

final_transform = T2 @ R @ T1
rotated_square = apply_transform(square, final_transform)
```

---

## 🔮 Roadmap Futuro

- [ ] Implementar algoritmo de Clipping (Cohen-Sutherland)
- [ ] Algoritmo de preenchimento de polígonos (Scan-Line)
- [ ] Projeção perspectiva (atualmente apenas ortogonal)
- [ ] Suporte a curvas de Bézier
- [ ] Exportação para SVG
- [ ] Testes automatizados para funções matemáticas
- [ ] Diagrama UML da arquitetura

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Áreas sugeridas:

- 📐 Implementar transformações adicionais
- 🎨 Melhorar a interface gráfica
- 🧪 Adicionar testes unitários
- 📚 Expandir documentação matemática
- 🐛 Corrigir bugs

Para contribuir:
1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/NovaTransformacao`)
3. Commit (`git commit -m 'Adiciona transformação de projeção'`)
4. Push (`git push origin feature/NovaTransformacao`)
5. Abra um Pull Request

---

## 📚 Referências

- Foley, J. D., et al. (1996). *Computer Graphics: Principles and Practice*
- Hughes, J. F., et al. (2013). *Computer Graphics: Principles and Practice (3rd Edition)*
- [LearnOpenGL - Transformations](https://learnopengl.com/Getting-started/Transformations)

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## ✉️ Contato

**João Vitor Godinho**  
📧 joaovitor.godinho@outlook.com  
🔗 [LinkedIn](https://www.linkedin.com/in/joão-vb-godinho/)  
💻 [GitHub](https://github.com/joaov-godinho)

---

<div align="center">
  
**⭐ Se este projeto te ajudou a entender Computação Gráfica, dê uma estrela!**

*Desenvolvido como material educacional para a disciplina de Computação Gráfica*

</div>
