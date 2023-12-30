import numpy as np

def north_west_corner(cost, supply, demand):
    rows, cols = len(supply), len(demand)
    allocation = np.zeros((rows, cols))

    #Zapocinjemo od severozapada, samim tim smo na 0,0
    row, col = 0, 0
    while row < rows and col < cols:
        if supply[row] > demand[col]: #Ako smo popunili zahtev, prelazimo na sledecu kolonu
            allocation[row, col] = demand[col]
            supply[row] -= demand[col]
            col += 1
        else: #Ako nismo, ostajemo u koloni ali taj red je popunjen pa se spustamo na sledeci
            allocation[row, col] = supply[row]
            demand[col] -= supply[row]
            row += 1
    
    Z_opt = np.sum(cost * allocation)

    print("Matrica raspodele pomocu metode severozapadnog ugla:")
    print(allocation)
    print("Zopt = ", Z_opt)

def minimum_cost_method(cost, supply, demand):
    original_cost = cost.copy() #Kopiramo originalne cene jer cemo ih menjati u toku koda
    allocation = np.zeros((len(supply), len(demand)))

    while np.sum(supply) > 0 and np.sum(demand) > 0:
        min_cost_indices = np.unravel_index(np.argmin(cost, axis=None), cost.shape) #Dobijamo (row, col) ovim putem
        row, col = min_cost_indices

        if supply[row] > demand[col]: #Ako imamo vise da ponudimo nego sto je potraznja, svu potraznju cemo popuniti
            allocation[row, col] = demand[col]
            supply[row] -= demand[col]
            demand[col] = 0
        else: #Ako nemamo, moramo da damo svu ponudu i da taj red vise ne koristimo
            allocation[row, col] = supply[row]
            demand[col] -= supply[row]
            supply[row] = 0

        cost[row, col] = np.inf #Cenu postavljamo na inf nakon sto je popunimo kako ne bi usli u loop (bolje nego neki ogroman broj jer mozda bas u zadatku bude veci broj od tog)
    
    Z_opt = np.sum(original_cost * allocation)

    print("Matrica raspodele pomocu metode minimalnih cena:")
    print(allocation)
    print("Zopt = ", Z_opt)

def vogels_approximation_method(cost, supply, demand):
    original_cost = cost.copy() #Opet kopiramo jer cemo sigurno menjati vrednosti cena radi olaksanja algoritma
    allocation = np.zeros((len(supply), len(demand)))

    while np.sum(supply) > 0 and np.sum(demand) > 0:
        row_penalty = np.zeros(len(supply)) #Trazimo penale, tj row i col penalty ce sluziti
        col_penalty = np.zeros(len(demand)) #da nam nadju najvecu razliku minimalnih cena u redovima i kolonama

        for i in range(len(supply)):
            if supply[i] > 0:
                sorted_costs = np.sort(cost[i][cost[i] > 0]) #Sortiramo cene po njihovim vrednostima
                if len(sorted_costs) > 1: #Ako imamo bar 2 cene onda racunamo penale, ako nemamo penali su nula i samim tim biramo najmanju cenu
                    row_penalty[i] = sorted_costs[1] - sorted_costs[0] #Oduzimamo poslednji od pretposlednjeg, tj dve najmanje cene

        for j in range(len(demand)):
            if demand[j] > 0:
                sorted_costs = np.sort(cost[:, j][cost[:, j] > 0]) #Isto se ovde radi, samo za potraznje
                if len(sorted_costs) > 1:
                    col_penalty[j] = sorted_costs[1] - sorted_costs[0]

        max_penalty_index = np.argmax(np.concatenate((row_penalty, col_penalty)))   #Trazimo najveci penal u redovima i kolonama
        if max_penalty_index < len(supply): #Ovo je logicki odradjeno, posto smo prvo postavili redove pa kolone, pitacemo da li je indes u oblasti
            i = max_penalty_index           #duzine naseg broja ponuda, jer recimo imamo 4 ponude a indeks je 5, to znaci da on sigurno mora biti
            j = np.argmin(cost[i])          #indeks clana col_penalty jer po konkatenaciji smo prvo ubacili row_penalty (ponudu) pa tek col_penalty
        else: 
            j = max_penalty_index - len(supply) #Oduzimamo broj ponuda jer kao sto smo rekli, mi imamo 4 ponude, a indeks je 5, to ne znaci
            i = np.argmin(cost[:, j])           #da indeks pripada petoj potraznji vec prvoj pa moramo da normalizujemo po tome
                                                #Ako je izabran red onda je i indeks (red) a trazimo minimum u tom redu i obrnuto
        quantity = min(supply[i], demand[j])    #Uzimamo sta nam je manje, potrosnja ili ponuda i po tome popunjavamo slot matrice
        allocation[i, j] = quantity
        supply[i] -= quantity
        demand[j] -= quantity   #Naravno nakon toga brisemo mogucnosti ili potrebe

        if supply[i] == 0:  #Ako nam je ponuda koju smo sad iskoristili jednaka nuli, ne mozemo vise taj red koristiti
            cost[i, :] = np.inf 
        if demand[j] == 0:  #Isto vazi i za kolonu
            cost[:, j] = np.inf

    Z_opt = np.sum(original_cost * allocation)

    print("Matrica raspodele pomocu Vogelove metode:")
    print(allocation)
    print("Zopt = ", Z_opt)

def solve_transport_problem():
    # Definisanje problema
    cost = np.array([[10., 12., 0.], [8., 4., 3.], [6., 9., 4.], [7., 8., 5.]]) #Matrica troskova
    supply = np.array([20., 30., 20., 10.]) #Niz ponude
    demand = np.array([10., 40., 30.]) #Niz potraznje

    print("Izaberite metodu za rešavanje transportnog problema:")
    print("1. Metod Severozapadnog Ugla")
    print("2. Metod Minimalnih Cena")
    print("3. Vogelova Metoda")
    choice = int(input("Unesite broj izbora: "))

    if choice == 1:
        north_west_corner(cost, supply, demand)
    elif choice == 2:
        minimum_cost_method(cost, supply, demand)
    elif choice == 3:
        vogels_approximation_method(cost, supply, demand)
    else:
        print("Pokusajte drugi put nesto sto pripada tom opsegu, molim Vas.")

solve_transport_problem()