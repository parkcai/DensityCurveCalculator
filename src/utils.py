from mpmath import findroot
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy
import os
import shutil
import random
import string


from interface import *
from src.solution import *
from src.parsed_interface import *

def calculate():
    
    
    parsed_interface = ParsedInterface()
    
    parsed_interface.normal_density = n0
    
    solution = Solution(num_of_species=len(species_names))
    
    Ts = [Tmin] + Tmaxs
    has_solution_flag = 0
    for i in range(1, len(Ts)):
        current_Tmin = Ts[i-1]
        current_Tmax = Ts[i]
        if has_solution_flag == 0:
            partial_solution = solve_equations(Tmin=current_Tmin, Tmax=current_Tmax, 
                                            fine_degree=fine_degrees[i-1], 
                                            initial_guess=[j/parsed_interface.normal_density for j in initial_guess ], 
                                            parsed_interface=parsed_interface)
            has_solution_flag = 1
        else:
            partial_solution = solve_equations(Tmin=current_Tmin, Tmax=current_Tmax, 
                                       fine_degree=fine_degrees[i-1], 
                                       initial_guess=solution.get_latest_solution(), 
                                       parsed_interface=parsed_interface)
        solution.append(partial_solution)
    
    solution.resume(parsed_interface.normal_density)
    
    solution.plot(picture_save_path)
    
    solution.save(data_save_path)

def equations_of_T(T, parsed_interface):
    def equations(*args):
        res = []
        
        species_name_to_index = parsed_interface.species_name_to_index
        normal_density = parsed_interface.normal_density
        chemical_reaction_powers_lhs = parsed_interface.chemical_reaction_powers_lhs
        chemical_reaction_powers_rhs = parsed_interface.chemical_reaction_powers_rhs
        
        for i in range(len(chemical_reactions)):
            
            chemical_reaction = chemical_reactions[i]
            chemical_reaction_power_lhs = chemical_reaction_powers_lhs[i]
            chemical_reaction_power_rhs = chemical_reaction_powers_rhs[i]
            
            current_equation = 0
            
            rhs_coeffs = chemical_reaction["right_handed_side_coefficients"]
            lhs_coeffs = chemical_reaction["left_handed_side_coefficients"]
            
            rhs_exp = (normal_density ** chemical_reaction_power_rhs)
            lhs_exp = (normal_density ** chemical_reaction_power_lhs) *  chemical_reaction["reaction_K"](T)
            
            for species in rhs_coeffs.keys():
                rhs_exp *= (args[species_name_to_index[species]] ** rhs_coeffs[species]) 
            current_equation += rhs_exp
            for species in lhs_coeffs.keys():
                lhs_exp *= (args[species_name_to_index[species]] ** lhs_coeffs[species]) 
            current_equation -= lhs_exp
            res.append(current_equation)
        for i in range(len(conservation_relations)):
            conservation_relation = conservation_relations[i]
            current_equation = 0
            for species in conservation_relation["coefficients"].keys():
                current_equation += args[species_name_to_index[species]] * conservation_relation["coefficients"][species]
            current_equation -= conservation_relation["quantity"] / normal_density
            res.append(current_equation)
        return res
        
        # automatic parse is convenient, but it will slow down the calculation a little bit (by about 15%)
        # you may want to manually write your equations here
        
        # example code:
        # nH2 = args[0]
        # nH2_ion = args[1]
        # nH = args[2]
        # np = args[3]
        # ne = args[4]
        # return [
        #     (nH * 2) * n0 - K_of_H2_decomposition(T) * nH2,
        #     np * ne * n0 - K_of_H_ionization(T) * nH ,
        #     nH2_ion*ne*n0 - K_of_H2_primary_decomposition(T)*nH2,
        #     np + nH + 2 * nH2 + 2*nH2_ion- 1,
        #     nH2_ion+np - ne
        # ]

    return equations     

def solve_equations(Tmin, Tmax, fine_degree, initial_guess, parsed_interface):
    temperatures = []
    densities = [[] for _ in range(len(species_names))] 
    current_guess = initial_guess
    if fine_degree >= 1:
        for i in tqdm(range(Tmin*fine_degree,Tmax*fine_degree)):
            T = i / fine_degree
            temperatures.append(T)
            current_solution = findroot(equations_of_T(T, parsed_interface), tuple(current_guess), tol = mpmath_findroot_tolerance)
            for j in range(len(densities)):
                densities[j].append(current_solution[j])
            current_guess = current_solution
    else:
        delta_T = int(1 / fine_degree)
        for i in tqdm(range(Tmin, Tmax, delta_T)):
            T = i 
            temperatures.append(T)
            current_solution = findroot(equations_of_T(T, parsed_interface), tuple(current_guess), tol = mpmath_findroot_tolerance)
            for j in range(len(densities)):
                densities[j].append(current_solution[j])
            current_guess = current_solution
    return [temperatures] + densities



def clear_folder(folder_path):

    if not os.path.exists(folder_path):
        print(f"File path {folder_path} does not exist.")
        return
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path) 
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path) 
            print(f"{file_path} deleted.")
        except Exception as e:
            print(f"{file_path} can't be deleted. Error: {e}")
            
def generate_random_string(length):
    characters = string.ascii_letters + string.digits  
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string
    
def clear_data_and_picture():
    print("")
    print("--------------------------------------------------")
    print("Are you sure to delete all datum and pictures? ")
    key_string = generate_random_string(4)
    input_string = input(f"Type {key_string} if yes:")
    if input_string == key_string:
        clear_folder("data")
        clear_folder("pic")
        print("Deletion completed.")
    else:
        print("Deletion canceled.")
    print("--------------------------------------------------")
    print("")
    
    

if __name__ == "__main__":
    pass