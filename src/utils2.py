import numpy
import matplotlib.pyplot as plt
from interface import plt_figsize, density_unit, temperature_unit



def generate_picture(data_path, pic_path, selected_species = None):
    zipped_data = numpy.load(data_path, allow_pickle=True)
    data = zipped_data["densities"]
    species = zipped_data["species"]
    data = list(data)
    
    temperatures = data[0]
    densities = [data[_] for _ in range(1, len(data))]
    
    plt.clf()
    plt.cla()
    plt.figure(figsize=plt_figsize)
    
    if selected_species == None:
        for i in range(len(densities)):
            plt.plot(temperatures, densities[i], label = species[i])
    else:
        for selected_item in selected_species:
            assert selected_item in species, "Unknown species selected: "+selected_item+"!" 
        for i in range(len(densities)):
            if species[i] in selected_species:
                plt.plot(temperatures, densities[i], label = species[i])
            
    if len(selected_species) > 1:
        plt.title('Densities vs. Temperature')
    else:
        plt.title('Density vs. Temperature')
    plt.ylabel(f'Density ({density_unit})')
    plt.xlabel(f'Temperature ({temperature_unit})')
    plt.legend() 
    plt.grid()
    plt.savefig(pic_path)
        
def contrast_different_curves(data_path, background_data_path, pic_path, selected_species = None):
    zipped_data1 = numpy.load(data_path, allow_pickle=True)
    data1 = zipped_data1["densities"]
    species1 = zipped_data1["species"]
    data1 = list(data1)
    
    temperatures1 = data1[0]
    densities1 = [data1[_] for _ in range(1, len(data1))]
    
    zipped_data2 = numpy.load(background_data_path, allow_pickle=True)
    data2 = zipped_data2["densities"]
    species2 = zipped_data2["species"]
    data2 = list(data2)
    
    temperatures2 = data2[0]
    densities2 = [data2[_] for _ in range(1, len(data2))]
    
    for i in range(len(temperatures1)):
        assert temperatures1[i] == temperatures2[i], "Incompatible temperatures!"
        
    
    
    if selected_species == None:
        count = 0
        colors = plt.cm.viridis(numpy.linspace(0, 1, len(set(species1) & set(species2))))
        for i in range(len(species1)):
            for j in range(len(species2)):
                if species2[j] == species1[i]:
                    count += 1
                    plt.plot(temperatures1, densities1[i], label = species1[i], color = colors[count - 1])
                    plt.plot(temperatures1, densities2[j], linestyle = "--", color = colors[count - 1])
                
        if count > 1:
            plt.title('Densities vs. Temperature')
        else:
            plt.title('Density vs. Temperature')
        plt.ylabel(f'Density ({density_unit})')
        plt.xlabel(f'Temperature ({temperature_unit})')
        plt.legend() 
        plt.grid()
        plt.savefig(pic_path)
    else:
        for species in selected_species:
            assert species in species1, "Unknown species selected!"
            assert species in species2, "Unknown species selected!"
        count = 0
        colors = plt.cm.viridis(numpy.linspace(0, 1, len(set(species1) & set(species2))))
        for species in selected_species:
            for i in range(len(species1)):
                if species1[i] == species:
                    for j in range(len(species2)):
                        if species2[j] == species:
                            count += 1
                            plt.plot(temperatures1, densities1[i], label = species1[i], color = colors[count - 1])
                            plt.plot(temperatures1, densities2[j], linestyle = "--", color = colors[count - 1])
        if count > 1:
            plt.title('Densities vs. Temperature')
        else:
            plt.title('Density vs. Temperature')
        plt.ylabel(f'Density ({density_unit})')
        plt.xlabel(f'Temperature ({temperature_unit})')
        plt.legend() 
        plt.grid()
        plt.savefig(pic_path)
                            


def check_densities_at_temperature(T, data_path):
    zipped_data = numpy.load(data_path, allow_pickle=True)
    data = zipped_data["densities"]
    species = zipped_data["species"]
    data = list(data)
    
    temperatures = data[0]
    densities = [data[_] for _ in range(1, len(data))]
    
    index = 0
    while  index != len(temperatures) and temperatures[index] < T: index += 1
    if index == len(temperatures): assert False, f"Temperature {T}{temperature_unit} not in the calculated range!"
    
    print("")
    print("--------------------------------------------------------------------")
    print(f"At temperature {T}{temperature_unit}, species have densities listed respectively below:")
    for i in range(len(densities)):
        print(species[i] + f": {float(densities[i][index]):.4e} {density_unit}")
    print("--------------------------------------------------------------------")
    print("")