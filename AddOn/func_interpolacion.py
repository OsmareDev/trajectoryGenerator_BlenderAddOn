import numpy as np

def lineal(pos_ini, pos_fin, u):
    """
        Interpolación lineal: Interpola dos valores linealmente
            Se sigue la formula:
            posicion actual = posicion final + porcentaje avanzado * (posicion final - posicion inicial)
            posX = pos_ini + u*(pos_fin-pos_ini)

        pos_ini: posicion inicial del tramo a interpolar, obtenida a traves del keyframe correspondiente
        pos_fin: posicion final del tramo a interpolar, obtenida a traves del keyframe correspondiente
        u: porcentaje del tramo (de 0 a 1) avanzado respecto al tiempo
            este se calcula de la siguiente manera:
            u = tiempo actual - tiempo inicial / tiempo final - tiempo inicial
    """
    posX = pos_ini + u*(pos_fin-pos_ini)
    return posX

def lineal_der(pos_ini, pos_fin, u):
    posX = pos_fin - pos_ini
    return posX

def lineal_der2(pos_ini, pos_fin, u):
    posX = 0
    return posX


def hermite(u, p_ini, p_fin, v_ini, v_fin):
    """
        u: porcentaje del tramo (de 0 a 1) avanzado respecto al tiempo
            este se calcula de la siguiente manera:
            u = tiempo actual - tiempo inicial / tiempo final - tiempo inicial

        p_ini: posicion inicial del tramo a interpolar, obtenida a traves del keyframe correspondiente
        p_fin: posicion final del tramo a interpolar, obtenida a traves del keyframe correspondiente
        v_ini: velocidad inicial del tramo a interpolar, obtenida a traves de la diferencia la posicion del handler derecho del keyframe con la posicion del keyframe
        v_fin: velocidad final del tramo a interpolar, obtenida a traves de la diferencia de la posicion del keyframe con la del handler izquierdo

        Interpolación de hermite: Genera un polinomio cubico de un punto a otro que usa derivadas para definir
                                    las velocidades alcanzadas para cada punto
            Se sigue la formula:
            posicion actual =   (1 - 3 * u^2 + 2 * u^3)* posicion inicial 
                                + u^2 * (3 - 2 * u) * posicion final 
                                + u * ( u - 1 )^2 * velocidad inicial 
                                + u^2 * (u - 1) * velocidad final

            Esta formula puede reordenarse separandose en las variables y convertirse en las matrices del codigo
    """

    mat_U = np.array([u**3, u**2, u, 1])
    mat_M = np.array([
                        [ 2, -2,  1,  1],
                        [-3,  3, -2, -1],
                        [ 0,  0,  1,  0],
                        [ 1,  0,  0,  0]
                    ])
    mat_B = np.array([
                        [p_ini],
                        [p_fin],
                        [v_ini],
                        [v_fin]
                    ])
    pos = np.matmul(np.matmul(mat_U, mat_M), mat_B)
    return pos

def hermite_der(u, p_ini, p_fin, v_ini, v_fin):
    mat_U = np.array([3*(u**2), 2*u, 1, 0])
    mat_M = np.array([
                        [ 2, -2,  1,  1],
                        [-3,  3, -2, -1],
                        [ 0,  0,  1,  0],
                        [ 1,  0,  0,  0]
                    ])
    mat_B = np.array([
                        [p_ini],
                        [p_fin],
                        [v_ini],
                        [v_fin]
                    ])
    pos = np.matmul(np.matmul(mat_U, mat_M), mat_B)
    return pos

def hermite_der2(u, p_ini, p_fin, v_ini, v_fin):
    mat_U = np.array([6*u, 2, 0, 0])
    mat_M = np.array([
                        [ 2, -2,  1,  1],
                        [-3,  3, -2, -1],
                        [ 0,  0,  1,  0],
                        [ 1,  0,  0,  0]
                    ])
    mat_B = np.array([
                        [p_ini],
                        [p_fin],
                        [v_ini],
                        [v_fin]
                    ])
    pos = np.matmul(np.matmul(mat_U, mat_M), mat_B)
    return pos


def catmull_rom(u, p_ant, p_ini, p_fin, p_post, tau):
    """
        u: porcentaje del tramo (de 0 a 1) avanzado respecto al tiempo
            este se calcula de la siguiente manera:
            u = tiempo actual - tiempo inicial / tiempo final - tiempo inicial

        p_ant: posicion del keyframe anterior al keyframe inicial del tramo, en caso de no tener keyframe anterior se duplicaria el inicial
        p_ini: posicion inicial del tramo a interpolar, obtenida a traves del keyframe correspondiente
        p_fin: posicion final del tramo a interpolar, obtenida a traves del keyframe correspondiente
        p_post: posicion del keyframe posterior al keyframe final del tramo, en caso de ser el tramo final y no tener keyframe posterior el valor sera el de la posicion final        
        tau: valor de tension el cual sirve para aumentar o disminuir las velocidades calculadas

        Interpolación de Catmull-Rom: Genera un polinomio cubico de un punto a otro que usa las diferencias entre puntos para suplir las velocidades necesarias en hermite,
                                        de la siguiente manera:
                                        velocidad inicial = (posicion anterior a la inicial - posicion final) * tension
                                        velocidad final   = (posicion inicial - posicion posterior a la final) * tension
                                    Por lo tanto se podrian calcular las velocidades de la manera anterior y pasarselas a la funcion ya implementada de hermite
                                    
            Por lo que se pueden sustituir los valores en la formula de hermite  
            Aunque tambien se pueden sustituir en la formula de Hermite y reorganizar en forma de matrices
                quedando la formula de la siguiente manera:
            
            posicion actual =   (1 - 3 * u^2 + 2 * u^3)* posicion inicial 
                                + u^2 * (3 - 2 * u) * posicion final 
                                + u * ( u - 1 )^2 * ((posicion anterior a la inicial - posicion final) * tension) 
                                + u^2 * (u - 1) * ((posicion inicial - posicion posterior a la final) * tension)
            
            y las matrices quedarian como en el codigo
    """

    mat_U = np.array([1, u, u**2, u**3])

    mat_M = np.array([
                        [0,     1,     0,       0   ],
                        [-tau,  0,     tau,     0   ],
                        [2*tau, tau-3, 3-2*tau, -tau],
                        [-tau,  2-tau, tau-2,   tau ]
                    ])

    mat_B = np.array([
                        [p_ant],
                        [p_ini],
                        [p_fin],
                        [p_post]
                    ])

    pos = np.matmul(np.matmul(mat_U, mat_M), mat_B)
    return pos

def catmull_rom_der(u, p_ant, p_ini, p_fin, p_post, tau):

    mat_U = np.array([0, 1, 2*u, 3*(u**2)])

    mat_M = np.array([
                        [0,     1,     0,       0   ],
                        [-tau,  0,     tau,     0   ],
                        [2*tau, tau-3, 3-2*tau, -tau],
                        [-tau,  2-tau, tau-2,   tau ]
                    ])

    mat_B = np.array([
                        [p_ant],
                        [p_ini],
                        [p_fin],
                        [p_post]
                    ])

    pos = np.matmul(np.matmul(mat_U, mat_M), mat_B)
    return pos

def catmull_rom_der2(u, p_ant, p_ini, p_fin, p_post, tau):

    mat_U = np.array([0, 0, 2, 6*u])

    mat_M = np.array([
                        [0,     1,     0,       0   ],
                        [-tau,  0,     tau,     0   ],
                        [2*tau, tau-3, 3-2*tau, -tau],
                        [-tau,  2-tau, tau-2,   tau ]
                    ])

    mat_B = np.array([
                        [p_ant],
                        [p_ini],
                        [p_fin],
                        [p_post]
                    ])

    pos = np.matmul(np.matmul(mat_U, mat_M), mat_B)
    return pos


def bezier(u, p_ini, b_ini, b_fin, p_fin): 
    """
        u: porcentaje del tramo (de 0 a 1) avanzado respecto al tiempo
            este se calcula de la siguiente manera:
            u = tiempo actual - tiempo inicial / tiempo final - tiempo inicial

        p_ini: posicion inicial del tramo a interpolar, obtenida a traves del keyframe correspondiente
        b_ini: punto auxiliar inicial usado en la interpolacion de bezier para calcular la derivada en el punto, como en el caso de hermite hemos usado la diferencia entre 
                la posicion del handle derecho del keyframe - la posicion del propio keyframe
        b_fin: punto auxiliar final usado en la interpolacion de bezier para calcular la derivada en el punto, como en el caso de hermite hemos usado la diferencia entre
                la posicion del keyframe final - la posicion del handle izquierdo del keyframe
        p_fin: posicion final del tramo a interpolar, obtenida a traves del keyframe correspondiente

        Interpolación de Bezier: Genera un polinomio cubico a traves de dos puntos de posicion y dos puntos auxiliares intermedios que controlan la forma de la curva

        (Ejemplo1)
        Si asumimos que todos los puntos estan equitativamente distanciados entre ellos en el espacio entonces podemos usar la forma:
            Teniendo 3 puntos P0, P1, P2 se pueden usar para resolver la ecuación parabolica P(u) = au^2 + bu + c
            Tenemos el primer punto  P(0)   =   a*0 + b*0 + c = c         ===>      P0 = c
            Tenemos el segundo punto P(0.5) =   a*0.5^2 + b*0.5 + c       ===>      P1 = a*0.5^2 + b*0.5 + c (conocemos c, que es P0)
            Tenemos el tercer punto  P(1)   =   a*1^2 + b*1 + c           ===>      P1 = a + b + c (conocemos c, que es P0)
        Nos quedan 2 ecuaciones con 2 incognitas que son resolubles

        Pero esto no sucede en la mayoria de casos ya que los puntos de control se usan indistintamente de la posicion del anterior y conforme hagan falta, es por eso que pueden 
            haber varios puntos juntos y luego tener varios separados.
        Buscamos entonces una forma general de poder resolverlo, para ello usaremos la derivada de una "cuerdas" que nos proporcionarán la velocidad de salida y entrada a los 
            puntos de cada intervalo. El resultado de esta deribada se puede expresar como una matriz de 4x4 y usarse para producir un polinomio cubico interpolador en el anterior 
            ejemplo (Ejemplo1)
    """
    mat_U = np.array([u**3, u**2, u, 1])
    
    matrix = [
                [-1,  3, -3,  1],
                [ 3, -6,  3,  0],
                [-3,  3,  0,  0],
                [ 1,  0,  0,  0]
            ]

    mat_M = np.array(matrix) 
    mat_B = np.array([
                        [p_ini],
                        [b_ini],
                        [b_fin],
                        [p_fin]
                    ])
    pos = np.matmul(np.matmul(mat_U, mat_M), mat_B)
    return pos

def bezier_der(u, p_ini, b_ini, b_fin, p_fin): 
    
    mat_U = np.array([3*(u**2), 2*u, 1, 0])
    
    matrix = [
                [-1,  3, -3,  1],
                [ 3, -6,  3,  0],
                [-3,  3,  0,  0],
                [ 1,  0,  0,  0]
            ]

    mat_M = np.array(matrix) 
    mat_B = np.array([
                        [p_ini],
                        [b_ini],
                        [b_fin],
                        [p_fin]
                    ])
    pos = np.matmul(np.matmul(mat_U, mat_M), mat_B)
    return pos

def bezier_der2(u, p_ini, b_ini, b_fin, p_fin): 
    
    mat_U = np.array([6*u, 2, 0, 0])
    
    matrix = [
                [-1,  3, -3,  1],
                [ 3, -6,  3,  0],
                [-3,  3,  0,  0],
                [ 1,  0,  0,  0]
            ]

    mat_M = np.array(matrix) 
    mat_B = np.array([
                        [p_ini],
                        [b_ini],
                        [b_fin],
                        [p_fin]
                    ])
    pos = np.matmul(np.matmul(mat_U, mat_M), mat_B)
    return pos