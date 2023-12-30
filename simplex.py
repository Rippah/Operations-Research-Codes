import numpy as np
from itertools import combinations

def assert_matrix(A, b, C, problem):
    assert problem in ['max', 'min'], "Problem mora biti 'max' ili 'min'"
    assert A.shape[0] == b.shape[0], "Broj redova u A mora biti jednak broju redova u b"
    assert A.shape[1] == C.shape[1], "Broj kolona u A mora biti jednak broju kolona u C"
    
def check_singular(matrix):
    if np.linalg.matrix_rank(matrix) < matrix.shape[0]:
        raise ValueError("Matrica je singularna. Potrebno je primeniti pivotiranje.")

def print_solution(bases_var, not_bases_var, hat_b, problem, Z):
    for i in range(len(bases_var)):
        print(f'X{bases_var[i] + 1} = {np.round(hat_b[i][0])}')
        
    non_bases = [f'X{i + 1}' for i in range(len(not_bases_var)) if i not in bases_var]
    for x in non_bases:
        print(f'{x} = ', end='')
    print('0')
    
    if problem == 'max':
        print(f'Z_max = {Z[0][0]}')
    else:
        print(f'Z_min = {Z[0][0]}')    

def simplex(A, b, C, problem='max'):
    # Provera ulaznih parametara
    assert_matrix(A, b, C, problem)

    # Ako je problem minimizacije, promenite znakove koeficijenata ciljne funkcije
    if problem == 'min':
        C = -C

    # Inicijalizacija
    (m, n) = np.shape(A)
    identity_matrix = np.eye(m)
    zero_matrix = np.zeros((1, len(b)))

    A = np.hstack((A, identity_matrix))
    C = np.hstack((C, zero_matrix))

    (m, n) = np.shape(A)

    check_singular(A[:, :n])
    
    # Pronalaženje mogućih kombinacija baznih promenljivih
    var_combinations = list(combinations([*range(n)], len(b)))
    
    # Izračunavanje inverza matrice B
    for i in var_combinations:
        bases_var = list(i)
        not_bases_var = [x for x in range(n) if x not in bases_var]
        
        try:
            Binv = np.linalg.inv(A[:, bases_var])
            Xb = np.matmul(Binv, b)
            
            if not (np.any(Xb < 0)):
                break
        except:
            pass 
        
    omega = np.matmul(C[:, bases_var], Binv)
    
    # Glavna petlja
    iteration = 1
    while True:
        hat_b = np.matmul(Binv, b)
        Zi = []
        
        for j in not_bases_var:
            Zj = np.matmul(omega, A[:, j])
            Zi.append(Zj - C[:, j])
                    
        if problem == 'max':
            stop_condition = min(Zi) >= 0
        else:
            stop_condition = max(Zi) <= 0

        print(f"\nIteracija {iteration}:")

        print("Bazne Varijable (Xb):", bases_var)
        print("Nebazne Varijable:", not_bases_var)
        print("Trenutno Resenje (Zi):", np.matmul(C[:, bases_var], hat_b)[0][0])

        if stop_condition:
            Z = np.matmul(C[:, bases_var], hat_b)
            print_solution(bases_var, not_bases_var, hat_b, problem, Z)
            return

        k = np.argmin(Zi)
        k = not_bases_var[k]
        
        Yk = np.matmul(Binv, np.vstack((A[:, k])))
        Yk = Yk.reshape(-1)  # Preoblikovanje Yk u jednodimenzionalni niz
        hat_b = hat_b.reshape(-1)  # Preoblikovanje hat_b u jednodimenzionalni niz
        Yk_div_hat_b = (np.divide(hat_b, Yk, out = np.zeros_like(Yk), where = Yk != 0))  
        r = np.argmin(Yk_div_hat_b)
        
        new_not_bases_var = bases_var.pop(r)
        bases_var.append(k)
        
        not_bases_var.remove(k)       
        not_bases_var.append(new_not_bases_var)
        
        bases_var.sort()
        not_bases_var.sort()
        Binv = np.linalg.inv(A[:, bases_var])

        iteration += 1

# Definisanje problema
A = np.array([[1, 0, 1, 0, 0],
              [0, 2, 0, 1, 0],
              [3, 2, 0, 0, 1]])

b = np.array([[4],
              [12],
              [18]])  # Vrednost na desnoj strani drugog ograničenja

C = np.array([[3, 5, 0, 0, 0]])

user_input = input("Unesite 'min' za minimizaciju ili 'max' za maksimizaciju: ").lower()

# Poziv funkcije za rešavanje
simplex(A, b, C, problem=user_input)
