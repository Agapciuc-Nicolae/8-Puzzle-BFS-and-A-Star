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
    __slots__ = ['_stare','n','pozitie_actuala','adancime']
    def __init__(self,stare=None,n=None, adancime=None):
        self.pozitie_actuala = {}
        self._stare = stare
        self.n = n
        self.adancime = adancime
        for i in range(0, (n ** 2)):
            self.pozitie_actuala[i] = ((i// n) , (i % n))

    def h2(self):
        count=0
        count += self.adancime
        secventa = self._stare
        for i in range(self.n):
            for j in range(self.n):
                locatie_actuala = self.pozitie_actuala[secventa[i][j]]
                count = count +  (abs(locatie_actuala[0] - i)  + abs(locatie_actuala[1] - j))
        return count
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
Mai întâi mutăm spațiul gol în toate direcțiile posibile în starea de început și calculăm scorul f pentru fiecare stare. 
Aceasta se numește extinderea stării curente.
După extinderea stării curente, aceasta este împinsă în lista închisă, 
iar stările nou generate sunt împinse în lista deschisă. 
O stare cu cel mai mic scor f este selectată și extinsă din nou. 
Acest proces continuă până când starea obiectiv apare ca starea curentă. 
Practic, aici oferim algoritmului o măsură pentru a-și alege acțiunile. 
Algoritmul alege cea mai bună acțiune posibilă și continuă pe acea cale.
Acest lucru rezolvă problema generării stărilor copil redundante, deoarece algoritmul va extinde nodul cu cel mai mic scor f.
""" 
def Astar(matrice_intrare,n):
    start = timeit.default_timer()
    parinte={}
    stare_initiala = stareClass(matrice_intrare, n, 0)
    vizitat = []
    List = []
    heapq.heapify(List)
    heapq.heappush(List,stare_initiala)   
    while(len(List)):
        stare=heapq.heappop(List)
        if eStareFinala(stare._stare):
            stop = timeit.default_timer()
            time = stop-start
            print('\nS-a ajuns la starea finala!\nAdancimea la care s-a gasit solutia: ',  (stare.adancime),'\nNr. de stari vizitate: ',  (stare.adancime), "\nDurata: ",format(time, '.8f'), "secunde")
            l=[]
            for i in range(stare.adancime):
                l.append(stare)
                stare=parinte[stare]
            l.append(stare_initiala)
            l.reverse()
            for i in l:
                print(i)
            return True
        vizitat.append(stare)
        for copil in stare.generare_stari():
            if copil not in vizitat:
                heapq.heappush(List,copil)
                parinte[copil]=stare        
N = 3
l = []
for i in range(N):
    l.append(list(map(int,input().split(' '))))
matrice_intrare = np.array(l)
Astar(matrice_intrare,N)