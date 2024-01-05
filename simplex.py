import numpy as np
from numpy.linalg import matrix_rank, LinAlgError
from itertools import combinations

# Funkcija za proveru validnosti matrice
def validate_matrix(A, b, C, problem):
    assert problem in ['max', 'min'], "Samo problemi sa minimizacijom ('min') i maksimizacijom ('max') mogu biti rešeni!"
    assert A.shape[0] == b.shape[0], "Broj redova matrice A mora biti jednak broju redova matrice b!"
    assert A.shape[1] == C.shape[1], "Broj kolona matrice A mora biti jednak broju kolona matrice C!"

# Funkcija za proveru singularnosti matrice
def check_singularity(matrix):
    if matrix_rank(matrix) < matrix.shape[0]:
        raise ValueError("Matrica ne može biti singularna!")

# Funkcija koja proverava da li je postignuto optimalno rešenje
def is_finished(differences, problem):
    return np.all(differences >= 0) if problem == 'max' else np.all(differences <= 0)

# Funkcija za ispisivanje rešenja
def print_solution(iterations, Z, solution, B_indexes, N_indexes):
    problem = "max" if Z > 0 else "min"
    print(f"\n\n***Simplex problem za {problem}:***")
    print(f"\nBroj iteracija: {iterations}")
    print(f"Z_{problem} = {Z}")
    print("\nOsnovne promenljive:")
    for i in range(len(B_indexes)):
        print(f" X{B_indexes[i]+1} = {solution[i]}")

    print("\nNebazne promenljive:")
    for i in range(len(N_indexes)):
        print(f" X{N_indexes[i]+1} =", end='')
    print(' 0')

# Funkcija koja rešava Simplex metod
def solve_simplex(A, b, C, problem, limit=20):
    validate_matrix(A, b, C, problem)

    # Dodavanje identičke matrice dimenzija A
    identity_matrix = np.eye(A.shape[0])
    zero_matrix = np.zeros((1, len(b)))
    A = np.hstack((A, identity_matrix))
    C = np.hstack((C, zero_matrix))

    (m, n) = A.shape

    check_singularity(A)
    B_indexes = [*range(n - m, n)]
    N_indexes = [i for i in range(n) if i not in B_indexes]

    try:
        B_inv = np.linalg.inv(A[:, B_indexes]) if not (np.linalg.inv(A[:, B_indexes]) @ b < 0).any() else None #Postavljamo inverznu matricu akko su sve vrednosti nenegativne
    except LinAlgError:
        pass

    if B_inv is None: #U slucaju da uslov nije ispunjen, pokusacemo da nadjemo neku drugu kombinaciju koja nije trenutna bazna i ako nadjemo takvu postace nova bazna
        combs = list(combinations([*range(n)], len(b)))

        for comb in combs:
            B_indexes = list(comb)
            N_indexes = [i for i in range(n) if i not in B_indexes]

            try:
                B_inv = np.linalg.inv(A[:, B_indexes])
                X_b = B_inv @ b

                if (X_b < 0).any():
                    break
            except LinAlgError:
                pass

    iterations = 1

    omega = C[:, B_indexes] @ B_inv #Faktor mnozenja svakog reda matrice za proveru da li smo stigli do kraja
    b_hat = B_inv @ b
    Z = C[:, B_indexes] @ b_hat

    while iterations < limit:
        differences = omega @ A[:, N_indexes] - C[:, N_indexes] #Ako je svako ai >= 0 za max ili ai <= 0 za min, onda smo nasli nase optimalno resenje

        if is_finished(differences, problem):
            Z_value = Z[0][0]
            solution = list(b_hat.flatten())
            print_solution(iterations, Z_value, solution, B_indexes, N_indexes)
            return

        k = np.argmin(differences) if problem == 'max' else np.argmax(differences) #Najnegativniji problem uzimamo za max, a najpozitivniji za min
        k_difference = differences[:, k] #Uzimamo ceo red problema
        k = N_indexes[k]

        Y_k = B_inv @ A[:, k]   #Radimo sad proveru pivot elementa
        Y_k = Y_k.reshape(B_inv.shape[0], 1)
        np.seterr(divide='ignore', invalid='ignore')
        quotient = b_hat / Y_k  #Uzimamo pivot za element koji daje adekvatnu promenu (onaj ciji element nam najvise deli red)
        pivot_row = np.argmin([val for val in quotient if val >= 0])    #Prvo delimo pivot red sa pivotom

        non_pivot_rows = [i for i in range(B_inv.shape[0]) if i != pivot_row] #Sad radimo pivotiranje ostalih redova

        e_p = Y_k[pivot_row][0]
        e_r = B_inv[pivot_row, :]

        B_inv[non_pivot_rows, :] -= [e_r * Y_k[row][0] / e_p for row in non_pivot_rows] #eij = eij - e_r * Yik / e_p gde je k element te iste kolone sa kojom se oduzima element
        b_hat[non_pivot_rows] -= b_hat[pivot_row] * Y_k[non_pivot_rows] / e_p
        omega[0] -= B_inv[pivot_row] * k_difference / e_p   #Menjamo element kojim smo uzeli da pivotiramo
        Z -= b_hat[pivot_row] * k_difference / e_p  #Menjamo nase trenutno resenje
        B_inv[pivot_row] = B_inv[pivot_row] / e_p   #Menjamo i vrednost nase matrice tako sto delimo taj red pivotom
        b_hat[pivot_row] = b_hat[pivot_row] / e_p   #Menjamo i njegov b_hat element

        tmp = N_indexes[k]  #Menjamo bazne i nebazne koeficijente
        N_indexes[k] = B_indexes[pivot_row]
        B_indexes[pivot_row] = tmp
        N_indexes.sort()

        iterations += 1

    return None

# Primeri:

A = np.array([
    [0.5, 2, 1],
    [1, 2, 4]
])

b = np.array([
    [24],
    [60]
])

C = np.array([
    [6, 14, 13]
])

solve_simplex(A, b, C, 'max')


A = np.array([
    [1, 0, 1],
    [0, 2, 0],
    [3, 2, 0,]
])

b = np.array([
    [4],
    [12],
    [18]
])

C = np.array([
    [3, 5, 0]
])

solve_simplex(A, b, C, 'max')


A = np.array([
    [1,  1,  1, 1, 1, 1],
    [2, -1, -2, 1, 0, 0],
    [0,  0,  1, 1, 2, 1]
])

b = np.array([
    [6],
    [4],
    [4]
])

C = np.array([
    [-1, -2, 1, -1, -4, 2]
])

solve_simplex(A, b, C, 'min')
