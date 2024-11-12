import matplotlib.pyplot as plt
import numpy
from interface import *

class Solution:
    def __init__(self, num_of_species):
        self.data = [[] for _ in range(num_of_species+1)]
        self.mpmath_precision = mpmath_precision
        
    def append(self, partial_solution):
        assert len(self.data) == len(partial_solution), "Incompatible solutions!"
        for i in range(len(self.data)):
            self.data[i] += partial_solution[i]
            
    def save(self, path):
        numpy.savez(path, densities = numpy.array(self.data), species = species_names)
            
    def get_latest_solution(self):
        res = []
        for i in range(1, len(self.data)):
            res.append(self.data[i][-1])
        return res
    
    def resume(self, normal_density):
        for i in range(1, len(self.data)):
            self.data[i] = list(numpy.array(self.data[i]) * normal_density)
         
    def plot(self, path):
        temperatures = self.data[0]
        densities = [self.data[_] for _ in range(1, len(self.data))]
        
        plt.clf()
        plt.cla()
        plt.figure(figsize=plt_figsize)
        for i in range(len(densities)):
            plt.plot(temperatures, densities[i], label = species_names[i])
        if len(densities) > 1:
            plt.title('Densities vs. Temperature')
        else:
            plt.title('Density vs. Temperature')
        plt.ylabel(f'Density ({density_unit})')
        plt.xlabel(f'Temperature ({temperature_unit})')
        plt.legend() 
        plt.grid()
        plt.savefig(path)