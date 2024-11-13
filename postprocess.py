from src.utils2 import *


if __name__ == "__main__":
    # after calculation, select functions you need and run this program to postprocess datum
    
    data_path = "data/H2_H_p_e_better.npz"
    
    pic_path = "pic/H2_H_p_e_better_showH2ion.png"
    
    # generate_picture(data_path=data_path, pic_path = pic_path, selected_species=["H2+"])
    
    # check_densities_at_temperature(T = 300, data_path = data_path)
    
    # contrast_different_curves("data/ns_of_T_with_ion.npz", "data/ns_of_T_no_ion.npz", "pic/contrast.png")
    
    contrast_different_curves(
        data_path = "data/H2_H_p_e_better.npz",
        background_data_path = "data/H2_H_p_e.npz",
        pic_path = "pic/H2_H_p_contrast.png",
        selected_species = ["H2", "H", "p"]
    )
    
    # contrast_different_curves("data/ns_of_T_g=16_rotation.npy","data/ns_of_T_g=16.npy", "pic/rotation_contrast.png")
    
    pass