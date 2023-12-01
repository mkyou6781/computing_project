import matplotlib.pyplot as plt
import numpy as np
from newman_ziff.lattice_dev import LatticeDev

def largest_cluster_plot(lattice_dev):
    
    lattice_dev.prep()
    biggest_cluster_list = []
    for i in range(lattice_dev.N):
        site = lattice_dev.occ_order[i]
        lattice_dev.add_site(site)
        biggest_cluster_list.append(lattice_dev.biggest_cluster)
        """if lattice_dev.stop:
            #print("spanning cluster is detected at",i)
            break"""
    plt.plot(np.arange(lattice_dev.N) / lattice_dev.N,np.array(biggest_cluster_list))
    plt.xlabel("fraction of occupied sites")
    plt.ylabel("size of the largest cluster")
    plt.axvline(x=0.592,linestyle = "--")
    plt.show()
    return i

lattice_dev = LatticeDev(3000)
largest_cluster_plot(lattice_dev)