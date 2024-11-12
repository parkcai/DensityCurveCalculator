from reactions import *

calculation_name = "ns_of_T_with_ion"

# species_names = ["H2", "H", "p", "e", "H2+"]
species_names = [ "H", "p", "e",]

Tmin = 1
Tmaxs = [10000]
fine_degrees = [0.05]

initial_guess = [n0, 1, 1]

chemical_reactions = [
    # {
    #     "left_handed_side_coefficients":{
    #         "H2":1
    #     },
    #     "right_handed_side_coefficients":{
    #         "H":2
    #     },
    #     "reaction_K": K_of_H2_decomposition
    # },
    {
        "left_handed_side_coefficients":{
            "H":1
        },
        "right_handed_side_coefficients":{
            "p":1, "e":1
        },
        "reaction_K":K_of_H_ionization
    },
    # {
    #     "left_handed_side_coefficients":{
    #         "H2":1
    #     },
    #     "right_handed_side_coefficients":{
    #         "H2+":1, "e":1
    #     },
    #     "reaction_K":K_of_H2_primary_decomposition
    # }
    # ,
    # {
    #     "left_handed_side_coefficients":{
    #         "e":1
    #     },
    #     "right_handed_side_coefficients":{
    #         "e+":1, "e":2
    #     },
    #     "reaction_K":K_of_electron_pair
    # }
]

conservation_relations = [
    {
        "coefficients":{
              "H": 1, "p":1, 
        },
        "quantity": n0
    },
    
    {
        "coefficients":{
            "p": 1, "e": -1,
        },
        "quantity": 0
    }
]

mpmath_precision = 200
mpmath_findroot_tolerance = 1e-40

picture_save_path = f"pic/{calculation_name}.png"
plt_figsize = (10, 6)
data_save_path = f"data/{calculation_name}.npz"

temperature_unit = "K"
density_unit = "m^-3"


