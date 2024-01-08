import numpy as np

def min_zero_row(zero_matrix, marked_zeroes):
    row_sums = np.sum(zero_matrix, axis=1)
    valid_rows = np.where(row_sums > 0)[0]
    if len(valid_rows) == 0:
        return  # Nema redova sa nulama

    min_row_index = valid_rows[np.argmin(row_sums[valid_rows])]
    # Pronalaženje indeksa prve nule u minimalnom redu
    zero_index = np.argmax(zero_matrix[min_row_index])
    # Dodavanje indeksa minimalnog reda i nule u listu obeleženih nula
    marked_zeroes.append((min_row_index, zero_index))

    # Postavljanje svih elemenata u minimalnom redu i koloni sa nulom na False
    zero_matrix[min_row_index, :] = False
    zero_matrix[:, zero_index] = False

def mark_matrix(matrix):
    current_matrix = matrix
    zero_matrix = (current_matrix == 0)
    zero_matrix_copy = zero_matrix.copy()

    marked_zeroes = []

    # Dok god ima nula u kopiji matrice nula
    while (True in zero_matrix_copy):
        min_zero_row(zero_matrix_copy, marked_zeroes)

    marked_zeroes_row = []
    marked_zeroes_col = []

    # Popunjavanje lista redovima i kolonama obeleženih nula
    for i in range(len(marked_zeroes)):
        marked_zeroes_row.append(marked_zeroes[i][0])
        marked_zeroes_col.append(marked_zeroes[i][1])

    non_marked_row = list(set(range(current_matrix.shape[0])) - set(marked_zeroes_row))
    marked_cols = []
    check_switch = True

    while check_switch:
        check_switch = False

        # Prolazak kroz sve neobeležene redove
        for i in range(len(non_marked_row)):
            row_array = zero_matrix[non_marked_row[i], :]

            # Prolazak kroz sve elemente reda
            for j in range(row_array.shape[0]):
                # Ako je element nula i kolona nije obeležena
                if row_array[j] == True and j not in marked_cols:
                    marked_cols.append(j)
                    check_switch = True

        # Prolazak kroz sve obeležene nule
        for row_num, col_num in marked_zeroes:
            if row_num not in non_marked_row and col_num in marked_cols:
                # Dodavanje reda u listu neobeleženih redova
                non_marked_row.append(row_num)
                check_switch = True

    marked_rows = list(set(range(matrix.shape[0])) - set(non_marked_row))
    return(marked_zeroes, marked_rows, marked_cols)


def adjust_matrix(matrix, cover_rows, cover_cols):
    n = len(matrix) 
    min_num = float('inf')
    for row in range(n):
        if row not in cover_rows:
            for col in range(len(matrix[row])):
                if col not in cover_cols:
                    min_num = min(min_num, matrix[row][col])
                    matrix[row][col] -= min_num
    
    for row in cover_rows:
        for col in cover_cols:
            matrix[row][col] += min_num

    return matrix

def hungarian_algorithm(matrix):
	dim = matrix.shape[0]
	current_matrix = matrix
	for row_num in range(matrix.shape[0]):
		current_matrix[row_num] = current_matrix[row_num] - np.min(current_matrix[row_num])

	for col_num in range(matrix.shape[1]):
		current_matrix[:,col_num] = current_matrix[:,col_num] - np.min(current_matrix[:,col_num])
	zero_count = 0
	
	while zero_count < dim:
		marked_zeroes, marked_rows, marked_cols = mark_matrix(current_matrix)
		zero_count = len(marked_rows) + len(marked_cols)

		if zero_count < dim:
			current_matrix = adjust_matrix(current_matrix, marked_rows, marked_cols)

	return marked_zeroes

def ans_calculation(matrix, positions):
    ans_mat = np.zeros_like(matrix)
    for i, j in positions:
        ans_mat[i, j] = matrix[i, j]
    return np.sum(ans_mat), ans_mat

cost_matrix = np.array([[10, 4, 6, 10, 12], [11, 7, 7, 9, 14], [13, 8, 12, 14, 15], [14, 16, 13, 17, 1], [17, 11, 17, 20, 19]])
print(f"Pre madjarske metode: \n{cost_matrix}")
marked_zeroes = hungarian_algorithm(cost_matrix.copy())
result, result_matrix = ans_calculation(cost_matrix, marked_zeroes)
print(f"\nNakon madjarske metode: {result:.0f}\n{result_matrix}")
marked_zeroes.sort()
for i in range(len(marked_zeroes)):
    igrac, cena = list(marked_zeroes[i])
    igrac_string = chr(ord('a') + igrac)
    print(f"Igrac {igrac_string.upper()} igra sa cenom od {result_matrix[marked_zeroes[i]]}")
