import shutil
import os
def gen_netlist(path, number , input_netlist):
    current_path = os.getcwd()
    stim_path = current_path + "/stimul/"
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
    shutil.copyfile(input_netlist, f"{path}/netlist")
    with open(f"{path}/netlist", "a") as file3:
            # for i in range(number):
            #     folder_name = f"{path}/image_{i}"
            #     INA=[]
            #     print(f"{folder_name}/image.txt")
            #     with open(f"{folder_name}/image.txt", "r") as file:
            #         for line in file:
            #             value = line.strip()
            #             INA.append(value)
                for i in range(10):
                    line = f"V{i+1} (INB2\<{i}\> 0) vsource dc={VBN[i]} type=dc\n"
                    file3.write(line)
                for i in range(10000):
                    line = f"V{i+10001} (INB\<{i}\> 0) vsource dc={VBP[i]} type=dc\n"
                    file3.write(line)
                for i in range(1000):
                    line = f"II{i} (INA\<{i}\> 0) isource type=pwl file=\"{stim_path}input_{i}.txt\" \n"
                    file3.write(line)
                for i in range(10):
                    line = f"VV{i} (BL\<{i}\> 0) vsource dc=0.6 type=dc\n"
                    file3.write(line)
                for i in range(1000):
                    line = f"VV{i+10} (WL\<{i}\> 0) vsource dc=0 type=dc\n"
                    file3.write(line)
                for i in range(1000):
                    line = f"VV{i+1010} (WLb\<{i}\> 0) vsource dc=1.2 type=dc\n"
                    file3.write(line)
                #add the contenents of simul.txt
                line = f"VVV1 (VD 0) vsource dc=0.6 type=dc\n"
                file3.write(line)

                line = f"VVV2 (Vbp 0) vsource dc=1.2 type=dc\n"
                file3.write(line)
                line = f"VVV3 (Vbn 0) vsource dc=0 type=dc\n"
                file3.write(line)
                line = f"VVV4 (CLR 0) vsource type=pwl file=\"{stim_path}CLR.txt\" \n"
                file3.write(line)
                line = f"VVV5 (VD 0) vsource dc=0.6 type=dc\n"
                file3.write(line)

                with open("./simul_1u_trans.txt", "r") as file2:
                    for line in file2:
                        file3.write(line)

if __name__ == "__main__":
    # gen_netlist("./data",100)
    print("Must be called from main.py")
