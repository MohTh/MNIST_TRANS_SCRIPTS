#!/bin/bash


# Paths to the scripts
NETLIST_GEN_AND_TRAIN="./scripts/main.py"
SPECTRE_SIM_SCRIPT="./scripts/eval.sh"
EVAL_PY="./scripts/eval.py"
PERF_PY="./scripts/perf.py"



if [ "$1" == "--EVAL" ]; then
  # Check if the third argument is provided
  if [ -z "$2" ]; then
    echo "Usage: $0 --EVAL <data_parent_folder> <number_of_images>"
    exit 1
  fi
  
  # Eval script
python3 "$EVAL_PY" "${1}" "${2}"

# Check if the Python script executed successfully
if [ $? -ne 0 ]; then
  echo "Python eval script execution failed."
  exit 1
fi





# PERF script
python3 "$PERF_PY"

# Check if the Python script executed successfully
if [ $? -ne 0 ]; then
  echo "Python perf script execution failed."
  exit 1
fi
  exit 0
fi








if [ "$1" == "--PERF" ]; then
  
# PERF script
python3 "$PERF_PY"

# Check if the Python script executed successfully
if [ $? -ne 0 ]; then
  echo "Python perf script execution failed."
  exit 1
fi
  exit 0
fi









# Check if enough arguments are provided
if [ "$#" -lt 4 ]; then
  echo "USAGE: ./simulate.sh <output_folder_path> <number_of_images>  <t/nt> <input netlist path>"
  exit 1
fi



echo "Running netlist gen py (main.py)"

# Pass the first five arguments to the Python script
python3 "$NETLIST_GEN_AND_TRAIN" "${1}" "${2}" "${3}" "${4}"

# Check if the Python script executed successfully
if [ $? -ne 0 ]; then
  echo "Python main script execution failed."
  exit 1
fi


echo "Running DC Simulations"
# Pass the third argument to the second shell script

echo "Executing: $SPECTRE_SIM_SCRIPT ${1}"
bash "$SPECTRE_SIM_SCRIPT" "${1}"

# Check if the second shell script executed successfully
if [ $? -eq 0 ]; then
  echo "Spectre simulation shell script executed successfully."
else
  echo "Spectre simulation shell script execution failed."
fi



echo "Running Eval Py script"
# Eval script
echo "Executing: python3 $EVAL_PY ${1} ${2}"
python3 "$EVAL_PY" "${1}" "${2}"

# Check if the Python script executed successfully
if [ $? -ne 0 ]; then
  echo "Python eval script execution failed."
  exit 1
fi




echo "Running Perf Py script"
# PERF script
python3 "$PERF_PY"

# Check if the Python script executed successfully
if [ $? -ne 0 ]; then
  echo "Python perf script execution failed."
  exit 1
fi





