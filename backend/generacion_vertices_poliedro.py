from math import pow, sqrt
from scipy.constants import golden as phi

def __tetraedro():
    return [(pow(-1,int((i+1)/2)), pow(-1,i), pow(-1,int(i/2))) for i in range(4)]

def __cubo():
    return [tuple(pow(-1, int(i/pow(2,j))) for j in range(3)) for i in range(8)]

def __octaedro():
    return [tuple(s if i == d else 0 for i in range(3)) for d in range(3) for s in [1, -1]]

def __dodecaedro():
    phi_2 = pow(phi, 2)
    vertices_1 = [tuple(v[(p+j)%3] for j in range(3)) for p in range(3) for i in range(4) for v in [(0, pow(-1, int(i/2)), (phi + 1) * pow(-1, i))]]
    vertices_2 = [(phi * pow(-1, int(i/4)), phi * pow(-1, int(i/2)), phi * pow(-1, int(i))) for i in range(8)]
    vertices = vertices_1 + vertices_2
    return vertices

def __icosaedro():
    return [tuple(v[(p+j)%3] for j in range(3)) for p in range(3) for i in range(4) for v in [(0, pow(-1, int(i/2)), phi * pow(-1, i))]]

def __tetraedro_truncado():
    return [tuple(a * b for a, b in zip(sign, [sqrt(2)/4 * (3 if j == i else 1) for j in range(3)])) for i in range(3) for sign in [(1,1,1), (1,-1,-1), (-1,1,-1), (-1,-1,1)]]

def __cubo_truncado():
    aux = 1 + sqrt(2)
    vertices_1 = [(pow(-1,int(i/4)), aux * pow(-1,int(i/2)), aux * pow(-1,i)) for i in range(8)]
    vertices_2 = [(aux * pow(-1,int(i/4)), pow(-1,int(i/2)), aux * pow(-1,i)) for i in range(8)]
    vertices_3 = [(aux * pow(-1,int(i/4)), aux * pow(-1,int(i/2)), pow(-1,i)) for i in range(8)]
    vertices = vertices_1 + vertices_2 + vertices_3

    return vertices

def __octaedro_truncado():
    sqrt_2 = sqrt(2)
    sqrt_2_2 = sqrt_2/2

    vertices_1 = [(sqrt_2 * pow(-1,int(i/2)), sqrt_2_2 * pow(-1,i), 0) for i in range(4)]
    vertices_2 = [(sqrt_2_2 * pow(-1,i), 0, sqrt_2 * pow(-1,int(i/2))) for i in range(4)]
    vertices_3 = [(0, sqrt_2 * pow(-1,int(i/2)), sqrt_2_2 * pow(-1,i)) for i in range(4)]
    vertices_4 = [(sqrt_2_2 * pow(-1,int(i/2)), sqrt_2 * pow(-1,i), 0) for i in range(4)]
    vertices_5 = [(sqrt_2 * pow(-1,i), 0, sqrt_2_2 * pow(-1,int(i/2))) for i in range(4)]
    vertices_6 = [(0, sqrt_2_2 * pow(-1,int(i/2)), sqrt_2 * pow(-1,i)) for i in range(4)]

    vertices = vertices_1 + vertices_2 + vertices_3 + vertices_4 + vertices_5 + vertices_6

    return vertices

def __dodecaedro_truncado():
    inv_phi = 1/phi
    phi_1 = phi + 1
    phi_2 = phi + 2
    phi__2 = 2 * phi

    vertices_1 = [(0, inv_phi * pow(-1,int(i/2)), phi_2 * pow(-1,i)) for i in range(4)]
    vertices_2 = [(inv_phi * pow(-1,int(i/2)), phi_2 * pow(-1,i), 0) for i in range(4)]
    vertices_3 = [(phi_2 * pow(-1,int(i/2)), 0, inv_phi * pow(-1,i)) for i in range(4)]
    
    vertices_4 = [(inv_phi * pow(-1,int(i/4)), phi * pow(-1,int(i/2)), phi__2 * pow(-1,i)) for i in range(8)]
    vertices_5 = [(phi__2 * pow(-1,int(i/4)), inv_phi * pow(-1,int(i/2)), phi * pow(-1,i)) for i in range(8)]
    vertices_6 = [(phi * pow(-1,int(i/4)), phi__2 * pow(-1,int(i/2)), inv_phi * pow(-1,i)) for i in range(8)]
    
    vertices_7 = [(phi * pow(-1,int(i/4)), 2 * pow(-1,int(i/2)), phi_1 * pow(-1,i)) for i in range(8)]
    vertices_8 = [(phi_1 * pow(-1,int(i/4)), phi * pow(-1,int(i/2)), 2 * pow(-1,i)) for i in range(8)]
    vertices_9 = [(2 * pow(-1,int(i/4)), phi_1 * pow(-1,int(i/2)), phi * pow(-1,i)) for i in range(8)]

    vertices = vertices_1 + vertices_2 + vertices_3 + \
        vertices_4 + vertices_5 + vertices_6 + \
            vertices_7 + vertices_8 + vertices_9

    return vertices

def __icosaedro_truncado():
    phi_2 = phi + 2
    phi__3 = 3 * phi
    phi__2 = 2 * phi
    phi_2_1 = 2*phi + 1

    vertices_1 = [(0, pow(-1,int(i/2)), phi__3 * pow(-1,i)) for i in range(4)]
    vertices_2 = [(pow(-1,int(i/2)), phi__3 * pow(-1,i), 0) for i in range(4)]
    vertices_3 = [(phi__3 * pow(-1,int(i/2)), 0, pow(-1,i)) for i in range(4)]

    vertices_4 = [(pow(-1,int(i/4)), phi_2 * pow(-1,int(i/2)), phi__2 * pow(-1,i)) for i in range(8)]
    vertices_5 = [(phi_2 * pow(-1,int(i/4)), phi__2 * pow(-1,int(i/2)), pow(-1,i)) for i in range(8)]
    vertices_6 = [(phi__2 * pow(-1,int(i/4)), pow(-1,int(i/2)), phi_2 * pow(-1,i)) for i in range(8)]

    vertices_7 = [(phi * pow(-1,int(i/4)), 2 * pow(-1,int(i/2)), phi_2_1 * pow(-1,i)) for i in range(8)]
    vertices_8 = [(2 * pow(-1,int(i/4)), phi_2_1 * pow(-1,int(i/2)), phi * pow(-1,i)) for i in range(8)]
    vertices_9 = [(phi_2_1 * pow(-1,int(i/4)), phi * pow(-1,int(i/2)), 2 * pow(-1,i)) for i in range(8)]

    vertices = vertices_1 + vertices_2 + vertices_3 + \
        vertices_4 + vertices_5 + vertices_6 + \
            vertices_7 + vertices_8 + vertices_9

    return vertices

def __cuboctaedro():
    return [(0 if j == 0 else [-1, 1][i//2], 0 if j == 1 else [-1, 1][i%2], 0 if j == 2 else [-1, 1][(i//2+i%2)%2]) for j in range(3) for i in range(4)]

def __cuboctaedro_truncado():
    sqrt_2_1 = 1 + sqrt(2)
    sqrt_2_2_1 = 1 + 2*sqrt(2)

    vertices_1 = [(pow(-1,int(i/4)), sqrt_2_1 * pow(-1,int(i/2)), sqrt_2_2_1 * pow(-1,i)) for i in range(8)]
    vertices_2 = [(sqrt_2_1 * pow(-1,int(i/4)), sqrt_2_2_1 * pow(-1,int(i/2)), pow(-1,i)) for i in range(8)]
    vertices_3 = [(sqrt_2_2_1 * pow(-1,int(i/4)), pow(-1,int(i/2)), sqrt_2_1 * pow(-1,i)) for i in range(8)]
    vertices_4 = [(sqrt_2_1 * pow(-1,int(i/4)), pow(-1,int(i/2)), sqrt_2_2_1 * pow(-1,i)) for i in range(8)]
    vertices_5 = [(pow(-1,int(i/4)), sqrt_2_2_1 * pow(-1,int(i/2)), sqrt_2_1 * pow(-1,i)) for i in range(8)]
    vertices_6 = [(sqrt_2_2_1 * pow(-1,int(i/4)), sqrt_2_1 * pow(-1,int(i/2)), pow(-1,i)) for i in range(8)]

    vertices = vertices_1 + vertices_2 + vertices_3 + \
        vertices_4 + vertices_5 + vertices_6
    return vertices

def __icosidodecaedro():
    phi_2 = phi/2
    phi_1_2 = 1 / (2*phi)

    vertices_1 = [(pow(-1,int(i)), 0, 0) for i in range(2)]
    vertices_2 = [(0, pow(-1,int(i)), 0) for i in range(2)]
    vertices_3 = [(0, 0, pow(-1,int(i))) for i in range(2)]

    vertices_4 = [(phi_2 * pow(-1,int(i/4)), phi_1_2 * pow(-1,int(i/2)), 0.5 * pow(-1,i)) for i in range(8)]
    vertices_5 = [(phi_1_2 * pow(-1,int(i/4)), 0.5 * pow(-1,int(i/2)), phi_2 * pow(-1,i)) for i in range(8)]
    vertices_6 = [(0.5 * pow(-1,int(i/4)), phi_2 * pow(-1,int(i/2)), phi_1_2 * pow(-1,i)) for i in range(8)]

    vertices = vertices_1 + vertices_2 + vertices_3 + \
        vertices_4 + vertices_5 + vertices_6

    return vertices

def __icosidodecaedro_truncado():
    phi_1 = 1 / phi
    phi_2 = 2 / phi
    phi___2 = 2 * phi
    phi__1 = 1 + phi
    phi__2 = 2 + phi
    phi__3 = 3 + phi
    phi_1_2 = 1 + 2*phi
    phi__1_2 = 2*phi - 1
    phi__1_3 = -1 + 3*phi

    vertices_1 = [(phi_1 * pow(-1,int(i/4)), phi_1 * pow(-1,int(i/2)), phi__3 * pow(-1,i)) for i in range(8)]
    vertices_2 = [(phi_1 * pow(-1,int(i/4)), phi__3 * pow(-1,int(i/2)), phi_1 * pow(-1,i)) for i in range(8)]
    vertices_3 = [(phi__3 * pow(-1,int(i/4)), phi_1 * pow(-1,int(i/2)), phi_1 * pow(-1,i)) for i in range(8)]

    vertices_4 = [(phi_2 * pow(-1,int(i/4)), phi * pow(-1,int(i/2)), phi_1_2 * pow(-1,i)) for i in range(8)]
    vertices_5 = [(phi * pow(-1,int(i/4)), phi_1_2 * pow(-1,int(i/2)), phi_2 * pow(-1,i)) for i in range(8)]
    vertices_6 = [(phi_1_2 * pow(-1,int(i/4)), phi_2 * pow(-1,int(i/2)), phi * pow(-1,i)) for i in range(8)]
    
    vertices_7 = [(phi_1 * pow(-1,int(i/4)), phi__1 * pow(-1,int(i/2)), phi__1_3 * pow(-1,i)) for i in range(8)]
    vertices_8 = [(phi__1 * pow(-1,int(i/4)), phi__1_3 * pow(-1,int(i/2)), phi_1 * pow(-1,i)) for i in range(8)]
    vertices_9 = [(phi__1_3 * pow(-1,int(i/4)), phi_1 * pow(-1,int(i/2)), phi__1 * pow(-1,i)) for i in range(8)]
    
    vertices_10 = [(phi__1_2 * pow(-1,int(i/4)), 2 * pow(-1,int(i/2)), phi__2 * pow(-1,i)) for i in range(8)]
    vertices_11 = [(2 * pow(-1,int(i/4)), phi__2 * pow(-1,int(i/2)), phi__1_2 * pow(-1,i)) for i in range(8)]
    vertices_12 = [(phi__2 * pow(-1,int(i/4)), phi__1_2 * pow(-1,int(i/2)), 2 * pow(-1,i)) for i in range(8)]
    
    vertices_13 = [(phi * pow(-1,int(i/4)), 3 * pow(-1,int(i/2)), phi___2 * pow(-1,i)) for i in range(8)]
    vertices_14 = [(3 * pow(-1,int(i/4)), phi___2 * pow(-1,int(i/2)), phi * pow(-1,i)) for i in range(8)]
    vertices_15 = [(phi___2 * pow(-1,int(i/4)), phi * pow(-1,int(i/2)), 3 * pow(-1,i)) for i in range(8)]

    vertices = vertices_1 + vertices_2 + vertices_3 + \
        vertices_4 + vertices_5 + vertices_6 + \
        vertices_7 + vertices_8 + vertices_9 + \
        vertices_10 + vertices_11 + vertices_12 + \
        vertices_13 + vertices_14 + vertices_15
    return vertices

def __cubo_romo():
    tribonacci = 1.839286755214161
    tribonacci_1 = 1/tribonacci

    vertices_1 = [(pow(-1,int(i/4)), tribonacci * pow(-1,int(i/2)), tribonacci_1 * pow(-1,i)) for i in range(8)]
    vertices_2 = [(tribonacci_1 * pow(-1,int(i/4)), pow(-1,int(i/2)), tribonacci * pow(-1,i)) for i in range(8)]
    vertices_3 = [(tribonacci * pow(-1,int(i/4)), tribonacci_1 * pow(-1,int(i/2)), pow(-1,i)) for i in range(8)]

    vertices = vertices_1 + vertices_2 + vertices_3
    return vertices

def __dodecaedro_romo():
    phi_2 = phi/2
    phi_1_2 = 1 / (2*phi)

    vertices_1 = [(pow(-1,int(i)), 0, 0) for i in range(2)]
    vertices_2 = [(0, pow(-1,int(i)), 0) for i in range(2)]
    vertices_3 = [(0, 0, pow(-1,int(i))) for i in range(2)]

    vertices_4 = [(phi_2 * pow(-1,int(i/4)), phi_1_2 * pow(-1,int(i/2)), 0.5 * pow(-1,i)) for i in range(8)]
    vertices_5 = [(phi_1_2 * pow(-1,int(i/4)), 0.5 * pow(-1,int(i/2)), phi_2 * pow(-1,i)) for i in range(8)]
    vertices_6 = [(0.5 * pow(-1,int(i/4)), phi_2 * pow(-1,int(i/2)), phi_1_2 * pow(-1,i)) for i in range(8)]

    vertices = vertices_1 + vertices_2 + vertices_3 + \
        vertices_4 + vertices_5 + vertices_6

    return vertices

def __rombicuboctaedro():
    sqrt_2_1 = 1 + sqrt(2)

    vertices_1 = [(sqrt_2_1 * pow(-1,int(i/4)), pow(-1,int(i/2)), pow(-1,i)) for i in range(8)]
    vertices_2 = [(pow(-1,int(i/4)), pow(-1,int(i/2)), sqrt_2_1 * pow(-1,i)) for i in range(8)]
    vertices_3 = [(pow(-1,int(i/4)), sqrt_2_1 * pow(-1,int(i/2)), pow(-1,i)) for i in range(8)]

    vertices = vertices_1 + vertices_2 + vertices_3
    return vertices

def __rombicosidodecaedro():
    phi__2 = pow(phi,2)
    phi__3 = pow(phi,3)
    phi___2 = 2*phi
    phi_2 = 2 + phi

    vertices_1 = [(pow(-1,int(i/4)), pow(-1,int(i/2)), phi__3 * pow(-1,i)) for i in range(8)]
    vertices_2 = [(pow(-1,int(i/4)), phi__3 * pow(-1,int(i/2)), pow(-1,i)) for i in range(8)]
    vertices_3 = [(phi__3 * pow(-1,int(i/4)), pow(-1,int(i/2)), pow(-1,i)) for i in range(8)]

    vertices_4 = [(phi__2 * pow(-1,int(i/4)), phi * pow(-1,int(i/2)), phi___2 * pow(-1,i)) for i in range(8)]
    vertices_5 = [(phi * pow(-1,int(i/4)), phi___2 * pow(-1,int(i/2)), phi__2 * pow(-1,i)) for i in range(8)]
    vertices_6 = [(phi___2 * pow(-1,int(i/4)), phi__2 * pow(-1,int(i/2)), phi * pow(-1,i)) for i in range(8)]

    vertices_7 = [(phi_2 * pow(-1,int(i/2)), 0, phi__2 * pow(-1,i)) for i in range(4)]
    vertices_8 = [(0, phi___2 * pow(-1,int(i/2)), phi_2 * pow(-1,i)) for i in range(4)]
    vertices_9 = [(phi___2 * pow(-1,int(i/2)), phi_2 * pow(-1,i), 0) for i in range(4)]

    vertices = vertices_1 + vertices_2 + vertices_3 + \
        vertices_4 + vertices_5 + vertices_6 + \
        vertices_7 + vertices_8 + vertices_9

    return vertices


poliedros = {"tetraedro": __tetraedro,
             "cubo": __cubo,
             "octaedro": __octaedro,
             "dodecaedro": __dodecaedro,
             "icosaedro": __icosaedro,
             "cuboctaedro": __cuboctaedro,
             "icosidodecaedro": __icosidodecaedro,
             "tetraedro truncado": __tetraedro_truncado,
             "cubo truncado": __cubo_truncado,
             "octaedro truncado": __octaedro_truncado,
             "dodecaedro truncado": __dodecaedro_truncado,
             "icosaedro truncado": __icosaedro_truncado,
             "cuboctaedro truncado": __cuboctaedro_truncado,
             "icosidodecaedro truncado": __icosidodecaedro_truncado,
             "cubo romo": __cubo_romo, # ARREGLAR
             "dodecaedro romo": __dodecaedro_romo, # ARREGLAR
             "rombicuboctaedro": __rombicuboctaedro,
             "rombicosidodecaedro": __rombicosidodecaedro}

poliedro_id = ["tetraedro", 
                "cubo", 
                "octaedro", 
                "dodecaedro", 
                "icosaedro", 
                "cuboctaedro", 
                "icosidodecaedro", 
                "tetraedro truncado",
                "cubo truncado",
                "octaedro truncado",
                "dodecaedro truncado",
                "icosaedro truncado",
                "cuboctaedro truncado",
                "icosidodecaedro truncado",
                "cubo romo",
                "dodecaedro romo",
                "rombicuboctaedro",
                "rombicosidodecaedro"]

forma_caras = {"tetraedro": [3], 
                "cubo": [4], 
                "octaedro": [3], 
                "dodecaedro": [5], 
                "icosaedro": [3], 
                "cuboctaedro": [3,4], 
                "icosidodecaedro": [3,5], 
                "tetraedro truncado": [3,6],
                "cubo truncado": [3,8],
                "octaedro truncado": [4,6],
                "dodecaedro truncado": [3,10],
                "icosaedro truncado": [5,6],
                "cuboctaedro truncado": [4,6,8],
                "icosidodecaedro truncado": [4,6,10],
                "cubo romo": [3,4],
                "dodecaedro romo": [3,5],
                "rombicuboctaedro": [3,4],
                "rombicosidodecaedro": [3,4,5]}

def generar_vertices(poliedro):
    return poliedros[poliedro]()