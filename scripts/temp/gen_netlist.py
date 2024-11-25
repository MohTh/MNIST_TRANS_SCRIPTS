import shutil
def gen_netlist(path, number , input_netlist):
    # Read values from file and assign to an array
    VBN = []
    VBP = []

    with open("./INBN3.txt", "r") as file:
        for line in file:
            value = line.strip()
            VBN.append(value)
    with open("./INBP3.txt", "r") as file:
        for line in file:
            value = line.strip()
            VBP.append(value)


    for i in range(number):
        folder_name = f"{path}/image_{i}"
        INA=[]
        print(f"{folder_name}/image.txt")
        with open(f"{folder_name}/image.txt", "r") as file:
            for line in file:
                value = line.strip()
                INA.append(value)
        shutil.copyfile(input_netlist, f"{folder_name}/netlist")
        with open(f"{folder_name}/netlist", "a") as file:
                for i in range(10000):
                    line = f"V{i+1} (LNBN\<{i}\> 0) vsource dc={VBN[i]} type=dc\n"
                    file.write(line)
                for i in range(10000):
                    line = f"V{i+10001} (LNBP\<{i}\> 0) vsource dc={VBP[i]} type=dc\n"
                    file.write(line)
                for i in range(1000):
                    line = f"II{i} (INA\<{i}\> 0) isource dc={INA[i]} type=dc\n"
                    file.write(line)
                #add the contenents of simul.txt
                with open("./simul.txt", "r") as file2:
                    for line in file2:
                        file.write(line)

if __name__ == "__main__":
    gen_netlist("./data",100)
