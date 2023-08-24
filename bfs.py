import numpy as np
import heapq 
import copy
import time
import timeit

class stareClass(object):
    """
    Atributul special __slots__ ne permite să precizăm în mod explicit ce atribute de instanță ne așteptăm 
    să aibă instanțele noastre de obiect, cu rezultatele așteptate:

    1. Acces mai rapid la atribute.
    2. Economii de spațiu în memorie.
    """
    __slots__ = ['_stare','n','adancime']
    def __init__(self,stare=None,n=None, adancime=None):
        
        self._stare = stare
        self.n = n
        self.adancime = adancime

    def h2(self):
        return -1

    def __str__(self):
        return '\nStare:\n' + str(self._stare) + '\nAdancime: ' + str(self.adancime)

    """
    __lt__ este o metodă specială care descrie operatorul mai puțin decât în python. > este un simbol pentru operatorul mai mic
    """
    def __lt__(self,other):
        return self.h2() < other.h2()
    
    """
    __gt__ este o metodă specială care descrie operatorul mai puțin decât în python. > este un simbol pentru operatorul mai mare
    """
    def __gt__(self,other):
        return self.h2() > other.h2()
    
    """
    __eq__ este o metodă a unei clase atunci când utilizăm operatorul == pentru a compara instanțele clasei
    """
    def __eq__(self,other):
        for i in range(self.n):
            for j in range(self.n):
                if self._stare[i][j] != other._stare[i][j]:
                    return False
        return True

    """
    hash() este o funcție încorporată și returnează valoarea hash a unui obiect dacă are una. 
    Valoarea hash este un număr întreg care este folosit pentru a compara rapid cheile de dicționar în timp ce se uită la un dicționar.
    """   
    def __hash__(self):
        #tobytes() reprezinta construcția funcției octeți Python care conțin octeții de date brute din matrice.
        return hash(self._stare.tobytes())
    
    #Folosit pentru a găsi locația unei plăci goale în nod
    def find_space(self):
	    for i in range(self.n):
	        for j in range(self.n):
	            if self._stare[i][j] == 0:
	                return i,j
    
    #Folosit pentru a genera calea nodului după ce nodul obiectiv este atins
    def generare_stari(self):
        secventa = self._stare
        space_i , space_j=self.find_space()
        for row_add,col_add in [(-1,0),(1,0),(0,1),(0,-1)]:
            #deepcopy returneaza o copie adanca a secventei
            temp_secventa = copy.deepcopy(secventa)
            if space_i + row_add >= 0 and space_i + row_add < self.n and space_j + col_add >= 0 and space_j + col_add < self.n:
                temp_secventa[space_i][space_j],temp_secventa[space_i + row_add][space_j + col_add]= temp_secventa[space_i + row_add][space_j + col_add],temp_secventa[space_i][space_j]
                #yield este un cuvânt cheie care este folosit ca return, cu excepția faptului că funcția va returna un generator.
                yield stareClass(temp_secventa,self.n, self.adancime+1)

def eStareFinala(array):
    for i in range(3):
        for j in range(3):
            if(array[i][j] !=( i*3 +j)):
                return False
    return True       

"""
BFS poate returna soluția optimă, deoarece extinde întotdeauna cel mai puțin adânc nod neașteptat. 
Cu toate acestea, salvează fiecare nod pe care îl caută, 
astfel încât spațiul pe care îl ocupă este foarte mare, ceea ce este problema sa majoră. 
Când intrarea este grea, devine mai dificil pentru BFS să obțină rezultatul. 
"""
def BFS(matrice_intrare,n):
    start = timeit.default_timer()
    parinte={}
    stare_initiala = stareClass(matrice_intrare, n, 0)
    vizitat = set()
    List = [stare_initiala]
    while(len(List)):
        stare=List.pop(0)
        if eStareFinala(stare._stare):
            stop = timeit.default_timer()
            time = stop-start
            print('\nS-a ajuns la starea finala!\nAdancimea la care s-a gasit solutia:',  (stare.adancime),'\nNr. de stari vizitate:',  (stare.adancime), "\nDurata: ",format(time, '.8f'), "secunde")
            l=[]
            s=copy.deepcopy(stare)
            for i in range(s.adancime):
                l.append(stare)
                stare=parinte[stare]
            l.append(stare_initiala)
            l.reverse()
            for i in l:
                print(i)
            return True
        vizitat.add(stare)
        for copil in stare.generare_stari():
            if copil not in vizitat:
                List.append(copil)
                parinte[copil]=stare             
N = 3
l = []
for i in range(N):
    l.append(list(map(int,input().split(' '))))
matrice_intrare = np.array(l)
BFS(matrice_intrare,N)