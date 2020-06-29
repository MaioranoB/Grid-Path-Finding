import pygame
from collections import deque
from random import random
from math import inf,sqrt

PRETO = (0,0,0)
BRANCO = (255,255,255)
VERMELHO = (255,0,0)
VERDE = (0,255,0)
AZUL = (0,0,255)
AMARELO = (255,255,0)

largura_tela = 600
n_linhas = 50  #numero de linhas da grid
n_colunas = n_linhas
muro_porcentagem = 0.24 #chance de um no ser muro
W = largura_tela / n_linhas
H = largura_tela / n_colunas



#FUNÇÕES AUXILIARES NO A* E NO BEST FIRST SEARCH
def pop_menor_dist(lista):  #percorre a lista de tras pra frente e retorna o no com a menor dist     
    index = len(lista) - 1
    menor = lista[index]  
    for i in range(index,-1,-1):
        if lista[i].dist < menor.dist:
            menor = lista[i]
            index = i
    return lista.pop(index)

def heuristica(a,b,func):
    if func == "dist_euclidiana":
        return sqrt((a.x - b.x)**2 + (a.y - b.y)**2)
    if func == "dist_manhattan":
        return abs(a.x - b.x) + abs(a.y - b.y)

class Node():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visitado = False
        self.vizinhos = []
        self.dist = inf
        self.g = inf
        self.pai = None
        self.muro = False

    def __repr__(self):
        return (f"Node({self.x} {self.y})") #so pra debugar

    def show(self,cor):
        global tela
        if self.muro == False:
            pygame.draw.rect(tela, cor, (self.x * W, self.y * H , W-1, H-1))
        else:
            pygame.draw.rect(tela, PRETO, (self.x * W, self.y * H , W-1, H-1))
        pygame.display.update((self.x * W, self.y * H , W-1, H-1)) #faz o update apenas do rect que foi alterado

    def add_vizinhos(self,grid): #implementar vizinhos diagonais dps
        self.vizinhos = [] #tem q zerar os vizinhos pra quando for embaralhar os muros
        if self.muro == False: #muro nao tem vizinho
            x = self.x
            y = self.y
            if (x > 0 and grid[x-1][y].muro == False): #cima
                self.vizinhos.append(grid[x-1][y])

            if (y > 0 and grid[x][y-1].muro == False): #esquerda
                self.vizinhos.append(grid[x][y-1])

            if (x < (n_linhas - 1) and grid[x+1][y].muro == False): #baixo
                self.vizinhos.append(grid[x+1][y]) 

            if (y < (n_colunas - 1) and grid[x][y+1].muro == False ): #direita
                self.vizinhos.append(grid[x][y+1]) 

    def embaralha(self): 
        self.muro = False
        if (random() < muro_porcentagem):
            self.muro = True

class Grid():
    def __init__(self): #passar start e end como parametro?
        self.grid = []
        for i in range(n_linhas): #cirar a matriz 2d de nos
            self.grid.append([])
            for j in range(n_colunas):
                self.grid[i].append(Node(i,j))
                self.grid[i][j].show(BRANCO)
        
    def init(self): #configura os vizinhos e mostra a grid     
        self.start.muro = False
        self.end.muro = False
        for i in range(n_linhas):
            for j in range(n_colunas):
                self.grid[i][j].add_vizinhos(self.grid)
                self.grid[i][j].show(BRANCO)
        self.start.show(AZUL)
        self.end.show(AZUL)
        
    def grid_aleatoria(self): #muda os muros de lugar
        for i in range(n_linhas):
            for j in range(n_colunas):
                self.grid[i][j].embaralha()
        self.init() #recalcula os vizinhos e mostra a nova grid

    def set_start(self,a,b):
        self.start = self.grid[a][b]
        self.start.show(AZUL)
        
    def set_end(self,a,b):
        self.end = self.grid[a][b]
        self.end.show(AZUL)

    def set_muro(self,a,b):
        self.grid[a][b].muro = True
        self.grid[a][b].show(PRETO)
    
    def bfs(self):
        for i in range(n_linhas):  #desmarcar todos 
            for j in range(n_colunas):
                self.grid[i][j].visitado = False
                self.grid[i][j].pai = None
                self.grid[i][j].show(BRANCO)
                #self.grid[i][j].dist = 0
        self.start.visitado = True #marcar start
        fila = deque()
        fila.append(self.start)
        while(fila): #enquanto a fila n estiver vazia
            v = fila.popleft()
            v.show(VERDE)
            if v == self.end: #early exit
                break
            for w in v.vizinhos: #p cada vizinho w de v
                if w.visitado == False:
                    w.visitado = True
                    fila.append(w) 
                    w.pai = v
                    #w.dist = v.dist +1
        #mostrar o caminho dps que termina a bfs            
        if (self.end.visitado == False): 
            self.start.show(AZUL)
            self.end.show(AZUL)
            print("Não existe caminho") 
            return 
        self.reconstroi_caminho()
    
    def best_first_search(self,func_dist):
        for i in range(n_linhas):
            for j in range(n_colunas):
                self.grid[i][j].dist = inf
                self.grid[i][j].pai = None
                self.grid[i][j].show(BRANCO)
                
        self.start.dist = heuristica(self.start, self.end, func_dist)
        pq = [] #define uma fila de prioridade vazia
        pq.append(self.start)
        while pq: #enquanto a fila nao estiver vazia
            u = pop_menor_dist(pq) #selecione u em S, tal que dist[u] é minima
            u.show(VERDE)
            if u == self.end:
                self.reconstroi_caminho()
                return
            for v in u.vizinhos: #pra cada viznho v de u
                if v.dist == inf: #mesmo que se v ainda nao foi visitado
                    v.dist = heuristica(v, self.end, func_dist)
                    pq.append(v)
                    v.pai = u
        print("Não existe caminho")
        self.start.show(AZUL)
        self.end.show(AZUL)
        
    def a_star(self,func_dist): 
        for i in range(n_linhas):
            for j in range(n_colunas):
                self.grid[i][j].dist = inf
                self.grid[i][j].g = inf
                self.grid[i][j].show(BRANCO)
        # f = g + h
        self.start.g = 0
        self.start.dist = self.start.g + heuristica(self.start,self.end,func_dist) 

        openSet = []
        openSet.append(self.start)

        while openSet:
            atual = pop_menor_dist(openSet) #This operation can occur in O(1) time if openSet is a min-heap or a priority queue
            atual.show(VERDE)

            if atual == self.end:
                self.reconstroi_caminho()
                return
            
            for vizinho in atual.vizinhos:
                g_temp = atual.g + 1
                if g_temp < vizinho.g:
                    vizinho.pai = atual
                    vizinho.g = g_temp
                    vizinho.dist =  vizinho.g + heuristica(vizinho,self.end,func_dist)
                    if vizinho not in openSet:
                        openSet.append(vizinho)
                        vizinho.show(VERMELHO)
        print("Não existe caminho")
        self.start.show(AZUL)
        self.end.show(AZUL)

    def reconstroi_caminho(self):
        caminho = self.end
        while caminho:
            caminho.show(AZUL)
            caminho = caminho.pai

    def config_inicial(self):
        aux = 0
        print("\nEscolha uma posição inicial:")
        while True:
            config = pygame.event.wait()
            if config.type == pygame.MOUSEBUTTONDOWN and aux == 0:
                mx,my = pygame.mouse.get_pos()
                mx = int(mx / W)
                my = int(my / H)
                self.set_start(mx,my)
                print("Escolha uma posição final:")
                aux+=1
            elif config.type == pygame.MOUSEBUTTONDOWN and aux == 1:
                mx,my = pygame.mouse.get_pos()
                mx = int(mx / W)
                my = int(my / H)
                self.set_end(mx,my)
                print("Escolha a posição dos muros e (ENTER) quando acabar:")
                aux+=1
            elif pygame.mouse.get_pressed()[0] and aux == 2:
                mx,my = pygame.mouse.get_pos()
                mx = int(mx / W)
                my = int(my / H)
                self.set_muro(mx,my)
            elif config.type == pygame.KEYDOWN and aux == 2:
                if config.key == pygame.K_RETURN:
                    self.init()
                    print("\nCOMANDOS:")
                    print("(Esc) Pra sair")
                    print("(<-)  Pra gerar uma nova grid manualmente")
                    print("(->)  Pra gerar uma nova grid aleatória")
                    print("(b)   BFS")
                    print("(e)   Best First Search - heuristica euclidiana")
                    print("(m)   Best First Search - heuristica manhattan")
                    print("(a)   A* - heuristica manhattan")
                    print("(s)   A* - heuristica euclidiana\n")
                    break

    def nova_grid(self):
        for i in range(n_linhas):
            for j in range(n_colunas):
                self.grid[i][j].muro = False
                self.grid[i][j].show(BRANCO)
        self.config_inicial()


def main():
    global tela
    pygame.init()
    tela = pygame.display.set_mode((largura_tela,largura_tela))
    pygame.display.set_caption("Path Finding")

    main_grid = Grid()
    main_grid.config_inicial()

    run = True
    while run:
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN:
            if   event.key == pygame.K_RIGHT:   main_grid.grid_aleatoria()
            elif event.key == pygame.K_LEFT:    main_grid.nova_grid()
            elif event.key == pygame.K_b:       main_grid.bfs()
            elif event.key == pygame.K_e:       main_grid.best_first_search("dist_euclidiana")
            elif event.key == pygame.K_m:       main_grid.best_first_search("dist_manhattan")
            elif event.key == pygame.K_a:       main_grid.a_star("dist_manhattan")
            elif event.key == pygame.K_s:       main_grid.a_star("dist_euclidiana")
            elif event.key == pygame.K_ESCAPE:  run = False #telca esc
        elif event.type == pygame.QUIT: run = False #fechar a janela
    pygame.quit()
    return

main()