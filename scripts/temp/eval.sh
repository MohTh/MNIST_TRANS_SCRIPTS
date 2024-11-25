#!/bin/bash








# Specify the directory containing the folders

if [ -z "$1" ]; then
  echo "Please provide the Netlist parent directory"
  exit 1
fi

#parent_directory_relative="./data_m0.2_M1_V0.6"
parent_directory_relative="$1"
parent_directory=$(readlink -f "$parent_directory_relative")


i=0
# Iterate over each folder in the parent directory
for folder in "$parent_directory"/*/; do
    # Check if the current item is a directory
    if [ -d "$folder" ]; then
        # Print the folder name
      
        echo "Processing folder: $folder"
        
        # Run your command inside the folder
        # Example command:
        cd "$folder" && spectre -64 ++aps +mt=32 netlist +log ./psf/spectre.out -format psfxl -raw ./psf
        rm -rf ./netlist.ahdlSimDB
	    rm -rf ./psf
	    cd ..
        printf "\033[0K\r"
        
	    
    fi
done

