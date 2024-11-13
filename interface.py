from reactions import *

calculation_name = "H2_H_p_e_better"

species_names = [ "H2", "H2+", "H", "H(1)", "H(2)", "H(3)", "p", "e"]

Tmin = 1
Tmaxs = [50000]
fine_degrees = [0.5]

initial_guess = [n0/ 2, 1, 1, 1, 1, 1, 1, 1]

chemical_reactions = [
    {
        "left_handed_side_coefficients":{
            "H2":1
        },
        "right_handed_side_coefficients":{
            "H":2
        },
        "reaction_K": K_of_H2_decomposition
    },
    {
        "left_handed_side_coefficients":{
            "H":1
        },
        "right_handed_side_coefficients":{
            "p":1, "e":1
        },
        "reaction_K":K_of_H_ionization
    },
    {
        "left_handed_side_coefficients":{
            "H2":1
        },
        "right_handed_side_coefficients":{
            "H2+":1, "e":1
        },
        "reaction_K":K_of_H2_primary_decomposition
    },
    {
        "left_handed_side_coefficients":{
            "H":1
        },
        "right_handed_side_coefficients":{
            "H(1)":1
        },
        "reaction_K":K_of_H_first_excitation
    },
    {
        "left_handed_side_coefficients":{
            "H":1
        },
        "right_handed_side_coefficients":{
            "H(2)":1
        },
        "reaction_K":K_of_H_second_excitation
    },
    {
        "left_handed_side_coefficients":{
            "H":1
        },
        "right_handed_side_coefficients":{
            "H(3)":1
        },
        "reaction_K":K_of_H_third_excitation
    },
]

conservation_relations = [
    {
        "coefficients":{
              "H2":2, "H": 1, "H(1)": 1, "H(2)": 1, "H(3)": 1, "H2+": 1,"p":1, 
        },
        "quantity": n0 
    },
    
    {
        "coefficients":{
            "p": 1, "e": -1, "H2+": 1
        },
        "quantity": 0
    }
]

mpmath_precision = 200
mpmath_findroot_tolerance = 1e-50

plt_figsize = (10, 6)
picture_save_path = f"pic/{calculation_name}.png"
data_save_path = f"data/{calculation_name}.npz"

temperature_unit = "K"
density_unit = "m^-3"


