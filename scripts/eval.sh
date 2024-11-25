
if [ -z "$1" ]; then
  echo "Please provide the Netlist parent directory"
  exit 1
fi

#parent_directory_relative="./data_m0.2_M1_V0.6"
parent_directory_relative="$1"
parent_directory=$(readlink -f "$parent_directory_relative")

# Check if the current item is a directory
    
        echo "Processing folder: $parent_directory"
        
        # Run your command inside the folder
        # Example command:
        cd "$parent_directory" && spectre -64 ++aps +mt=32 netlist +log ./psf/spectre.out -format psfascii -raw ./psf
        #cd "$parent_directory" && /eda/cadence/2019-20/RHELx86/SPECTRE_19.10.063/bin/spectre -64 ++aps +mt=32 netlist +log ./psf/spectre.out -format psfascii -raw ./psf
        
        #rm -rf ./netlist.ahdlSimDB
        #psf -i ./psf/tran.tran.tran -o ../out/tran.psfascii

	#    rm -rf ./psf
	    cd ..
        printf "\033[0K\r"
    	

