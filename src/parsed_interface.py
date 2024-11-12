import numpy
from interface import *


def check_interface_format():
    assert len(species_names) == len(initial_guess), "Incompatible settings: species_names and initial_guess should have the same length!"
    assert len(Tmaxs), "Wrong setting: Tmaxs should have at least one Tmax!"
    assert len(Tmaxs) == len(fine_degrees), "Incompatible settings: Tmaxs and fine_degrees should have the same length!"
    for fine_degree in fine_degrees:
        assert isinstance(fine_degree, int) or (fine_degree < 1 and fine_degree > 0), "Wrong setting: fine_degrees should be an integer or a real number between 0 and 1!"
    for chemical_reaction in chemical_reactions:
        assert "left_handed_side_coefficients" in chemical_reaction, "Wrong setting: every chemical reaction should have attribute 'left_handed_side_coefficients'!"
        for species in chemical_reaction["left_handed_side_coefficients"].keys():
            assert species in species_names, "Wrong setting: every species in chemical reactions' left_handed_side_coefficients should belong to species_names!"
            assert isinstance(chemical_reaction["left_handed_side_coefficients"][species], int) and chemical_reaction["left_handed_side_coefficients"][species]>0, "Wrong setting: every left-handed-side coefficient in chemical reactions should be a positive integer!"
        assert "right_handed_side_coefficients" in chemical_reaction, "Wrong setting: every chemical reaction should have attribute 'right_handed_side_coefficients'!"
        for species in chemical_reaction["right_handed_side_coefficients"].keys():
            assert species in species_names, "Wrong setting: every species in chemical reactions' right_handed_side_coefficients should belong to species_names!"
            assert isinstance(chemical_reaction["right_handed_side_coefficients"][species], int) and chemical_reaction["right_handed_side_coefficients"][species]>0, "Wrong setting: every right-handed-side coefficient in chemical reactions should be a positive integer!"
        assert "reaction_K" in chemical_reaction, "Wrong setting: every chemical reaction should have attribute 'reaction_K'!"
    for conservation_relation in conservation_relations:
        assert "coefficients" in conservation_relation, "Wrong setting: every conservation relation should have attribute 'coefficients'!"
        for species in conservation_relation["coefficients"].keys():
            assert species in species_names, "Wrong setting: every species in conservation relations' coefficients should belong to species_names!"
        assert "reaction_K" in chemical_reaction, "Wrong setting: every chemical reaction should have attribute 'reaction_K'!"
        assert "quantity" in conservation_relation, "Wrong setting: every conservation relation should have attribute 'quantity'!"
    
    print("")
    print("--------------------------------------------------------------------------------------------")
    print(f"Name of calculation: {calculation_name}")
    
    print("")
    
    print("Considering system with species ", end="")
    for i in range(len(species_names)):
        print(species_names[i], end="")
        if i != len(species_names) - 1:
            print(", ",end="")
        else:
            print("")
    
    print("")
    
    print("Considering the following chemical reactions:")
    count = 1
    for chemical_reaction in chemical_reactions:
        print(f"{count}. ", end = "")
        lhs = list(chemical_reaction["left_handed_side_coefficients"].keys())
        lhs_dict = chemical_reaction["left_handed_side_coefficients"]
        for i in range(len(lhs)):
            if lhs_dict[lhs[i]] != 1:
                print(lhs_dict[lhs[i]], end="")
                print(" ", end="")
            print(lhs[i],end="")
            if i != len(lhs) - 1:
                print(" + ", end="")
            else:
                print(" == ", end="")
        rhs = list(chemical_reaction["right_handed_side_coefficients"].keys())
        rhs_dict = chemical_reaction["right_handed_side_coefficients"]
        for i in range(len(rhs)):
            if rhs_dict[rhs[i]]!=1:
                print(rhs_dict[rhs[i]], end="")
                print(" ", end="")
            print(rhs[i],end="")
            if i != len(rhs) - 1:
                print(" + ", end="")
            else:
                print("")
        count += 1
    
    print("")
    
    print("Considering the following conservation relations:")
    count = 1
    for conservation_relation in conservation_relations:
        print(f"{count}. ", end = "")
        current_dict = conservation_relation["coefficients"]
        current_list = list(current_dict.keys())
        if current_dict[current_list[0]] < 0:
            print("-",end="")
        for i in range(len(current_list)):
            if abs(current_dict[current_list[i]])!=1:
                print(f"{abs(current_dict[current_list[i]])} ", end="")
            print(f"n{current_list[i]}",end="")
            if i != len(current_list) - 1:
                if current_dict[current_list[i+1]] >= 0:
                    print(" + ",end="")
                else:
                    print(" - ",end="")
            else:
                print(" = ",end="")
        print(f"{conservation_relation['quantity']:.4e}")
        count += 1
    
    print("")
    
    print(f"Calculation starting at temperature {Tmin}{temperature_unit} with initial guess")
    print("(",end="")
    for i in range(len(initial_guess)):
        print(f"n{species_names[i]}={initial_guess[i]:.2e}",end="")
        if i != len(initial_guess) - 1:
            print(", ",end="")
    print(f")")
    
    print("")
    
    count = 1
    print("Calculation stages:")
    Ts = [Tmin] + Tmaxs
    for i in range(len(Tmaxs)):
        current_Tmin = Ts[i]
        current_Tmax = Ts[i+1]
        fine_degree = fine_degrees[i]
        print(f"{count}. Tmin: {current_Tmin}{temperature_unit}, Tmax: {current_Tmax}{temperature_unit}",end="    ")
        print(f"densities calculated every {1/fine_degree if isinstance(fine_degree, int) else int(1/fine_degree)}{temperature_unit}")
        count += 1
    
    print("")
    
    print(f"The data will be saved in {data_save_path}, and the picture will be saved in {picture_save_path}.")
    print("--------------------------------------------------------------------------------------------")
    print("")




class ParsedInterface:
    def __init__(self):
        check_interface_format()
        self.normal_density = numpy.max([conservation_relation["quantity"] for conservation_relation in conservation_relations])
        self.species_name_to_index = dict()
        for i in range(len(species_names)):
            self.species_name_to_index[species_names[i]] = i
        self.chemical_reaction_powers_lhs = []
        self.chemical_reaction_powers_rhs = []
        for chemical_reaction in chemical_reactions:
            lhs_total = numpy.sum([chemical_reaction["left_handed_side_coefficients"][species] for species in chemical_reaction["left_handed_side_coefficients"].keys()])
            rhs_total = numpy.sum([chemical_reaction["right_handed_side_coefficients"][species] for species in chemical_reaction["right_handed_side_coefficients"].keys()])
            least_coefficient = numpy.minimum(lhs_total, rhs_total)
            chemical_reaction_power_lhs = lhs_total - least_coefficient
            chemical_reaction_power_rhs = rhs_total - least_coefficient
            self.chemical_reaction_powers_lhs.append(chemical_reaction_power_lhs)
            self.chemical_reaction_powers_rhs.append(chemical_reaction_power_rhs)
            
    def print(self):
        print("")
        print("--------------------------------------------------------------------")
        print("interface.py is parsed as:")
        print(f"normal density: {self.normal_density:.4e}")
        print("species_name_to_index:")
        print(self.species_name_to_index)
        print("chemical_reaction_powers_lhs:")
        print(self.chemical_reaction_powers_lhs)
        print("chemical_reaction_powers_rhs:")
        print(self.chemical_reaction_powers_rhs)
        print("--------------------------------------------------------------------")
        print("")