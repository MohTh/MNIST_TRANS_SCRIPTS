import configparser
#USAGE: python main.py <output_folder_path> <number_of_images>  <t/nt> <input netlist path>



with open('./config.txt', 'r') as file:
    # Read and display the contents
    contents = file.read()
    print(contents)
    
    
    
config=configparser.ConfigParser()
config.read('./config.txt')
cmpt_t=config.get('DEFAULT','cmpt_t')
reset_t=config.get('DEFAULT','reset_t')
trans_t=config.get('DEFAULT','trans_t')


print(cmpt_t)
print(trans_t)
