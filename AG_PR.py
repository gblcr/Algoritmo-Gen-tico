import random
from operator import itemgetter
import numpy as np


def first_pop(custo):                               #Função qe cria a primeira população.
                                                    # Para tal recebe o vetor custo.
    firstpop = np.empty((10,11), dtype = int)       # Cria uma matriz para armazenar a primeira população.
    C = np.empty(4)                                 # E um vetor para armazenar o custo de cada release.

    for i in range(10):

        for j in range(10):
            
            n = random.randint(0,3)                 # Sorteia numeros entre 0 e 3.
            firstpop[i][j] = n

        firstpop[i][10] = 0

    return firstpop


def fitness(p, w, risco , X, V):                    # Função que calcula a aptidão.
    
    score = 0
    importancia = np.zeros(10)                      # Cria um vetor vazio de 10 posições para armazenar 
                                                    # o valor da importancia.
    for k in range(10):
        X[k][10] = 0
        for i in range(10):
            
            for j in range(3):
                importancia[i] += w[j] * V[i][j]    # Calculo da importancia
            
            if X[k][i] != 0:
                X[k][10] += (importancia[i] * (len(p) - X[k][i] + 1) - (risco[i] * X[k][i]))   # Calculo da aptidão.
                importancia[i] = 0


def select_Matriz(A):                                   # Função que organiza uma matriz de acordo com uma determinada coluna e seleciona os 10 melhores elementos.
                                                        # Recebe como parametro uma amtriz A.
    B = np.empty((20, 11), dtype = int)                 # Matriz para armazenar a amtriz A organizada.
    C = np.empty((10, 11), dtype = int)                 # Matriz para armazenar os 10 melhores elementos de A.

    B = sorted(A, reverse = True, key = itemgetter(10)) # Organiza A em ordem inversa(do maior para o menor).
    
    for i in range (10):                                # Seleciona os 10 melhores elementos.
        for j in range (11):
            C[i][j] = B[i][j]

    return C
	

def crossover(pop):     # Função que realiza o crossover de dois cromossomos.

    newPop = np.empty((10, 11), dtype = int)

    for k in range(5):
        binT1 = random.randint(0,9)
        binT2 = random.randint(0,9)
        crosstax = random.randint (0,100)
        
        if (crosstax <= 90):            # Taxa de cruzamento
        	for i in range (0,9,2):
        		for j in range (0,5):
        			newPop[i][j] = pop[binT1][j]
        			newPop[i+1][j] = pop[binT2][j]

        		for j in range(5,10):
        			newPop[i][j] = pop[binT2][j]
        			newPop[i+1][j] = pop[binT1][j]

        else:
        	for i in range (0,9,2):
        		for j in range (10):
        			newPop[i][j] = pop[i][j]
        			newPop[i+1][j] = pop[i+1][j]
              
    return newPop


def mutation(pop):                                  # Funçao de mutação.

	for i in range (10):                            # Percorre a matriz sorteando a taxa de mutação.
		for j in range (10):
			mutationTax = random.randint(0,100)

			if mutationTax <= 1:                    # Se esse valor for de 1%.
				pop [i][j] = random.randint(0,3)    # sorteamos um novo laro para o gene.
     


def fix_pop(pop, custo):            # Função que penaliza os cromossomos em que o custo ultrapasse $125.

    C = np.empty(4) 

    for i in range(10):             # Soma o custo de cada cromossomo.

        for j in range(10):

            if pop[i][j] == 1:                  
                C[1] += custo[j]

            elif pop[i][j] == 2:
                C[2] += custo[j]

            elif pop[i][j] == 3:
                C[3] += custo[j]

            if custo[j] <= 125:     # Se o valor nao passar $125 mantemos o mesmo valor.
                pop[i][j] = pop[i][j]

            else:                   # Caso contrario colocamos 0 no lugar.
                pop[i][j] = 0


def concatenate(A, B):                  # Função que concatena as duas matrizes.

    C = np.empty((20,11), dtype = int)  # Matriz para armazenar a matriz concatenada.

    for i in range (10):                # Laço for que cria a matriz concatenada.
        for j in range (11):
            C[i][j] = A[i][j]
            C[i+10][j] = B[i][j]

    return C
      

def main():

    # soma = 0      # Variaveis para determinar a amedia de
    # media = 0     # cada população.

    pop = np.empty((10,11), dtype = int)    # Armazena a população.
    newpop = np.empty((10,11), dtype = int) # Armazena a nova população apos o crossover e a mutação.
    aux = np.empty((20,11), dtype = int)    # Armazena a concatenação de pop e newpop.

    releases = [1, 2, 3]                             # Numero de releases possiveis em que cada gene/requisito pode estar.
    relevancia = [3, 4, 2]                           # Relevancia de cada cliente.
    risco = [3, 6, 2, 6, 4, 8, 9, 7, 6, 6]           # Risco de cada requisito.
    custo = [60, 40, 40, 30, 20, 20, 25, 70, 50, 20] # Custo de cada requisito.
    clientes = [[10, 10, 5],                         # Valor de cada cliente.
                [8, 10, 6],
                [6, 4, 8],
                [5, 9, 1],
                [7, 7, 5],
                [8, 6, 2],
                [6, 6, 4],
                [9, 8, 3],
                [6, 7, 5],
                [10, 10, 7]]

    pop = first_pop(custo)  # Gera a primeira populaçao, a penaliza e calcula seu fitness.
    fix_pop(pop, custo)
    fitness(releases, relevancia, risco, pop, clientes)
    
    '''for j in range (10):         # Função para determinar o fitness e a media de cada população
            soma+=pop [j][10]  
            media =soma/10 

    print ("fitness:",pop [0][10])
    print ("media:",media)
    soma = 0
    media =0'''
    
    for i in range(500):        # Realiza a operação: crossover -> mutação -> penalização -> calcula o fitness -> concatena -> seleciona os 10 melhores
        newpop = crossover(pop) # Repete esse procedimento 500 vezes
        mutation(newpop)
        fix_pop(pop, custo)
        fitness(releases, relevancia, risco, newpop, clientes)
        aux = concatenate(pop, newpop)
        pop = select_Matriz(aux)   

        '''for j in range (10):     # Função para determinar o fitness e a media de cada população
            soma+=pop [j][10]  
            media =soma/10 

        print ("fitness:",pop [0][10])
        print ("media:",media)
        soma = 0
        media =0'''
    #print(pop)     # Imprime a populaçao final.
    print("Solução: ", pop[0][:10]) # Imprime a melhor solução.
    print("Fitness: ", pop[0][10])  # Imprime o fitness da melhor solução.

if __name__ == "__main__":
    main()