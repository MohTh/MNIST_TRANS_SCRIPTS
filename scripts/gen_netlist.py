import shutil
import os

def transistor(template,name,source,drain,gate,bulk):
    template = template.replace("<INST>",name)
    template = template.replace("<source>",source)
    template = template.replace("<drain>",drain)
    template = template.replace("<gate>",gate)
    template = template.replace("<bulk>",bulk)
    return template
def capacitor(template,name,plus,minus,bulk):
    template = template.replace("<INST>",name)
    template = template.replace("<PLUS>",plus)
    template = template.replace("<MINUS>",minus)
    template = template.replace("<BULK>",bulk)
    return template

def gen_circuit(dk_config,path):
    #read the pdk config files
    with open(f"{dk_config}/nmos.txt", "r") as file:
        nmos = file.read()
    with open(f"{dk_config}/nmos_sink.txt", "r") as file:
        nmos_sink = file.read()
    with open(f"{dk_config}/pmos.txt", "r") as file:
        pmos = file.read()
    with open(f"{dk_config}/cap.txt", "r") as file:
        cap = file.read()
    with open(f"{dk_config}/path.txt", "r") as file:
        path_dk = file.read()
    
    
    with open(f"{path}/netlist", "w") as file:
        #get date and time 
        import datetime
        now = datetime.datetime.now()
        file.write(f"//This netlist was generated automatically on {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write("simulator lang=spectre\n")
        file.write("global 0\n")
        file.write("parameters temperature=27\n")
        file.write(path_dk)
        file.write("\n")
        #generate 4T1C Cell 
        file.write("subckt _sub0 BL INA INB INB2 OUTn OUTp VD Vbn Vbp WL WLb gndd \n")
        file.write("\t")
        file.write(capacitor(cap,"C0","INB","gndd","gndd"))
        file.write("\n")
        file.write("\t")
        file.write(transistor(pmos,"M1","BL","INB","WLb","Vbp"))
        file.write("\n")
        file.write("\t")
        file.write(transistor(pmos,"M4","INB","net9","gndd","Vbp"))
        file.write("\n")
        file.write("\t")
        file.write(transistor(pmos,"M3","VD","OUTn","INA","INB2"))
        file.write("\n")
        file.write("\t")
        file.write(transistor(pmos,"M0","VD","OUTp","INA","net9"))
        file.write("\n")
        file.write("\t")
        file.write(transistor(nmos,"r","INB","BL","WL","Vbn"))
        file.write("\n")
        file.write("ends _sub0")
        file.write("\n")
        file.write("subckt _sub1 ")
        for i in range(20):
            file.write(f"in\<{i}\> ")
        file.write("out \n")
        for i in range(10):
            file.write("\t")
            file.write(transistor(nmos_sink,f"Msp{i}","out",f"in\<{i}\>",f"in\<{i}\>","out"))
            file.write("\n")
            file.write("\t")
            file.write(transistor(nmos_sink,f"Msn{i}","out",f"in\<{2*i}\>",f"in\<{2*i}\>","out"))
            file.write("\n")
        file.write("ends _sub1")

        file.write("\n")
        
        #generate input column
        for i in range(1000):
            file.write(transistor(pmos,f"Mi{i}","VD",f"INA\<{i}\>",f"INA\<{i}\>","VD"))
            file.write("\n")
            file.write(transistor(pmos,f"Mclr{i}","VD","CLR",f"INA\<{i}\>","VD"))
            file.write("\n")

        #generate compute column
        for i in range(10):
            for j in range(1000):
                file.write(f"Icell{j+i*1000} (BL\<{i}\> INA\<{j}\> INB\<{j+i*1000}\> INB2\<{i}\> OUTn\<{i}\> OUTp\<{i}\> VD Vbn Vbp WL\<{j}\> WLb\<{j}\> 0) _sub0")
                file.write("\n")
        
        #generate sink transistors
        file.write("Isink (")
        for i in range(10):
            file.write(f"OUTp\<{i}\> ")
        for i in range(10):
            file.write(f"OUTn\<{i}\> ")
        file.write(" 0) _sub1")
        file.write("\n")



def gen_netlist(path, number , input_netlist,CAP,dk_config):
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
    # shutil.copyfile(input_netlist, f"{path}/netlist")
    gen_circuit(dk_config,path)
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
                line = f"VVV6 (CLRNMOS 0) vsource type=pwl file=\"{stim_path}CLR_NMOS.txt\" \n"
                file3.write(line)
                line = f"VVV5 (VD 0) vsource dc=0.6 type=dc\n"
                file3.write(line)
                with open(f"{dk_config}/nmos.txt", "r") as file:
                    nmos = file.read()
                for i in range(10):
                    line=f"C00{i} (OUTp\<{i}\> 0) capacitor c={CAP}\n"
                    file3.write(line)
                    line=transistor(nmos,f"M00p1{i}","0",f"OUTp\<{i}\>",f"CLRNMOS","0")
                    file3.write(line)
                    file3.write("\n")
                    # line=f"M000{i} (OUTp\<{i}\> CLRNMOS 0 0) nch l=120.0n w=500n m=1 nf=1 sd=200n ad=8.75e-14 \\ \n"
                    # file3.write(line)
                    # line=f"as=8.75e-14 pd=1.35u ps=1.35u nrd=0.2 nrs=0.2 sa=175.00n \\ \n"
                    # file3.write(line)
                    # line=f"sb=175.00n sca=0 scb=0 scc=0\n"
                    # file3.write(line)

                    line=f"C01{i} (OUTn\<{i}\> 0) capacitor c={CAP}\n"
                    file3.write(line)
                    
                    
                    line=transistor(nmos,f"M00n1{i}","0",f"OUTn\<{i}\>",f"CLRNMOS","0")
                    # line=f"M001{i} (OUTn\<{i}\> CLRNMOS 0 0) nch l=120.0n w=500n m=1 nf=1 sd=200n ad=8.75e-14 \\ \n"
                    file3.write(line)
                    file3.write("\n")
                    # line=f"as=8.75e-14 pd=1.35u ps=1.35u nrd=0.2 nrs=0.2 sa=175.00n \\ \n"
                    # file3.write(line)
                    # line=f"sb=175.00n sca=0 scb=0 scc=0\n"
                    # file3.write(line)
                    
                    

                with open("./simul_1u_trans.txt", "r") as file2:
                    for line in file2:
                        file3.write(line)

if __name__ == "__main__":
    # gen_netlist("./data",100)
    print("Must be called from main.py")
