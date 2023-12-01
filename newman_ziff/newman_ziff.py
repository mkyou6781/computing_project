###Newman Ziff Algorithmn
import numpy as np
import matplotlib.pyplot as plt

"""
The code is based on 

Newman, M. E. J., & Ziff, R. M. (2000). Efficient Monte Carlo Algorithm and High-Precision Results for Percolation. Physical Review Letters, 85(19), 4104–4107. https://doi.org/10.1103/physrevlett.85.4104

Newman, M. E. J., & Ziff, R. M. (2001). Fast Monte Carlo algorithm for site or bond percolation. Physical Review E, 64(1). https://doi.org/10.1103/physreve.64.016706

"""

class LatticeDev:
    def __init__(self, L):
        self.L = L
        self.N = L ** 2

    def initialise_variable(self):
        self.empty = int(-self.N - 1)  # label which is assigned to empty lattice
        self.displacement = np.zeros((self.N, 2), dtype=int)
        self.neighbour = np.zeros((self.N, 4), dtype=int)  # nearest neighbour
        self.occ_order = np.zeros(
            self.N, dtype=int
        )  # order of which the lattice is occupied
        self.pointer = np.ones(self.N, dtype=int) * (self.empty)
        self.biggest_cluster = 0
        self.cluster_number = 0
        self.stop = False

    def assign_neighbour(self):
        for i in range(self.N):
            self.neighbour[i, 0] = (i + 1) % self.N  # right
            self.neighbour[i, 1] = (i + self.N - 1) % self.N
            self.neighbour[i, 2] = (i + self.L) % self.N
            self.neighbour[i, 3] = (i + self.N - self.L) % self.N
            if (i % self.L) == 0:
                self.neighbour[i, 1] = i + self.L - 1
            if ((i + 1) % self.L) == 0:
                self.neighbour[i, 0] = i - self.L + 1

    def get_neighbour_vector(self, origin,dest): #calculate the neighbour vector from i to j
        diff = (dest - origin)
        x = diff % self.L
        y = abs(diff) // self.L

        """if abs(x) > (self.L/2):
            x = x - self.L
        if abs(y) > (self.L/2):
            y = y - self.L"""
        
        if diff == 1 or diff == - (self.L - 1):
            return np.array([1,0])
        elif diff == -1 or diff == (self.L - 1):
            return np.array([-1,0])
        elif (diff == self.L or diff == - (self.N-self.L)):
            return np.array([0,1])
        elif (diff == (self.N-self.L) or diff == - self.L):
            return np.array([0,-1])
        else:
            print("error")

    def permutaion(self):
        self.occ_order = np.arange(self.N)
        self.occ_order = np.random.permutation(self.occ_order)

    def find_root(self, i):
        if self.pointer[i] < 0:
            return int(i)
        else:
            pointer = self.find_root(self.pointer[i])
            self.displacement[i] += self.displacement[self.pointer[i]]
            self.pointer[i] = int(pointer)
            return int(pointer)

    def check_spanning(self,site,neighbour,root):
        diff = self.displacement[site] - self.displacement[neighbour]
        if (diff[0] ** 2 + diff[1] **2) != 1:
            return True

        

    def add_site(self,site):
        s1 = int(site)
        
        self.pointer[s1] = int(-1)
        self.cluster_number += 1

        for j in range(4):
            s2 = int(self.neighbour[s1,j])

            if self.pointer[s2] != self.empty:
                
                r2 = self.find_root(s2)
                r2 = int(r2)
                r1 = self.find_root(s1)
                r1 = int(r1)
                # print("type of r2",type(r2))

                if r2 != r1:
                    if self.pointer[r1] > self.pointer[r2]:
                        self.cluster_number -= 1
                        # when the occupied site should be connected to the root at r2
                        
                        self.displacement[r1] = -self.displacement[s1] + self.get_neighbour_vector(origin=s1,dest=s2) + self.displacement[s2]
                        self.pointer[r2] += int(self.pointer[r1])
                        self.pointer[r1] = int(r2)
                        """r1 = int(r2)"""
                        
                    else:  #
                        self.cluster_number -= 1
                        self.displacement[r2] = -self.displacement[s2] + self.get_neighbour_vector(origin=s2,dest=s1) + self.displacement[s1]
                        self.pointer[r1] += int(self.pointer[r2])
                        self.pointer[r2] = int(r1)
                
                if r2 == r1:
                    self.stop = self.check_spanning(s1,s2,r1)

                if (-self.pointer[r1]) > self.biggest_cluster:
                    self.biggest_cluster = int(-self.pointer[r1])

    def prep(self):
        self.initialise_variable()
        self.assign_neighbour()
        self.permutaion()
              
def lattice_development(lattice_dev):
    
    lattice_dev.prep()
    biggest_cluster_list = []
    for i in range(lattice_dev.N):
        site = lattice_dev.occ_order[i]
        lattice_dev.add_site(site)
        biggest_cluster_list.append(lattice_dev.biggest_cluster)
        if lattice_dev.stop:
            #print("spanning cluster is detected at",i)
            break
    return i