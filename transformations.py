#transformations.py
import numpy as np
import math

def apply_translation(obj, dx, dy, dz=0):
    translation_matrix = np.array([
        [1, 0, 0, dx],
        [0, 1, 0, dy],
        [0, 0, 1, dz],
        [0, 0, 0, 1]
    ])
    obj.coords = [
        tuple(translation_matrix.dot([x, y, z, 1])[:3]) for x, y, z in obj.coords
    ]

def apply_rotation(obj, angle_deg, axis='z', cx=0, cy=0, cz=0):
    angle_rad = math.radians(angle_deg)
    cos_theta = math.cos(angle_rad)
    sin_theta = math.sin(angle_rad)

    # Matriz de rotação em torno de Z, X ou Y
    if axis == 'z':
        rotation_matrix = np.array([
            [cos_theta, -sin_theta, 0, 0],
            [sin_theta, cos_theta,  0, 0],
            [0,         0,          1, 0],
            [0,         0,          0, 1]
        ])
    elif axis == 'x':
        rotation_matrix = np.array([
            [1, 0,          0,           0],
            [0, cos_theta, -sin_theta,   0],
            [0, sin_theta, cos_theta,    0],
            [0, 0,          0,           1]
        ])
    elif axis == 'y':
        rotation_matrix = np.array([
            [cos_theta,  0, sin_theta,   0],
            [0,          1, 0,           0],
            [-sin_theta, 0, cos_theta,   0],
            [0,          0, 0,           1]
        ])
    else:
        raise ValueError("Eixo inválido para rotação. Escolha entre 'x', 'y', ou 'z'.")

    # Translação para o centro antes e depois da rotação
    translate_to_center = np.array([
        [1, 0, 0, -cx],
        [0, 1, 0, -cy],
        [0, 0, 1, -cz],
        [0, 0, 0, 1]
    ])
    translate_back = np.array([
        [1, 0, 0, cx],
        [0, 1, 0, cy],
        [0, 0, 1, cz],
        [0, 0, 0, 1]
    ])

    combined_matrix = translate_back @ rotation_matrix @ translate_to_center

    obj.coords = [
        tuple(combined_matrix.dot([x, y, z, 1])[:3]) for x, y, z in obj.coords
    ]


def apply_scaling(obj, scale_factor, cx=0, cy=0, cz=0):
    scaling_matrix = np.array([
        [scale_factor, 0, 0, 0],
        [0, scale_factor, 0, 0],
        [0, 0, scale_factor, 0],
        [0, 0, 0, 1]
    ])

    # Translação para o centro antes e depois do escalonamento
    translate_to_center = np.array([
        [1, 0, 0, -cx],
        [0, 1, 0, -cy],
        [0, 0, 1, -cz],
        [0, 0, 0, 1]
    ])
    translate_back = np.array([
        [1, 0, 0, cx],
        [0, 1, 0, cy],
        [0, 0, 1, cz],
        [0, 0, 0, 1]
    ])

    combined_matrix = translate_back @ scaling_matrix @ translate_to_center

    obj.coords = [
        tuple(combined_matrix.dot([x, y, z, 1])[:3]) for x, y, z in obj.coords
    ]


def apply_reflection(obj, reflect_x=False, reflect_y=False, reflect_z=False):
    reflection_matrix = np.identity(4)
    if reflect_x:
        reflection_matrix[1][1] = -1
    if reflect_y:
        reflection_matrix[0][0] = -1
    if reflect_z:
        reflection_matrix[2][2] = -1
    obj.coords = [
        tuple(reflection_matrix.dot([x, y, z, 1])[:3]) for x, y, z in obj.coords
    ]
def apply_shear(obj, shx=0, shy=0, shz=0):
    shear_matrix = np.array([
        [1, shx, shz, 0],
        [shy, 1, shz, 0],
        [shy, shx, 1, 0],
        [0, 0, 0, 1]
    ])
    obj.coords = [
        tuple(shear_matrix.dot([x, y, z, 1])[:3]) for x, y, z in obj.coords
    ]

def calculate_center(obj):
    if not obj.coords:
        return (0, 0, 0)
    xs, ys, zs = zip(*obj.coords)
    cx, cy, cz = sum(xs) / len(xs), sum(ys) / len(ys), sum(zs) / len(zs)
    return cx, cy, cz
