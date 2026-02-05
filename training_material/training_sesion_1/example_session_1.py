
# IMPORT SDOM MODULE

import sdom
from sdom import run_solver, initialize_model, configure_logging, get_default_solver_config_dict
from sdom import load_data, export_results
import logging
import highspy
import os
import subprocess

configure_logging(level= logging.INFO)

current_folder = os.getcwd()
print("Current folder:", current_folder)



n_steps = 730*1  
# Number of steps in the simulation (IN HOURS - RECOMENDED = 8760)
with_resilience_constraints = False
 # If True, the model will include resilience constraints, which ensure that the system can withstand certain disruptions or failures. If False, the model will not include these constraints.
#case = "br_test_daily_b" 
case = "Data" 
# Case name, used for naming output files

#data_dir = os.path.join(current_folder, "sample_data", "br_test_daily_b") 
data_dir = os.path.join(current_folder, "SDOM_Hokkaido", "Data") 

#INCLUDE THE FOLDER PATH WHERE YOU HAVE THE INPUT .CSV FILES SDOM REQUIRES (Python version does not requires txt files)
data = load_data( data_dir ) 
output_dir = os.path.join(current_folder, f'sample_results_{case}')

#THIS INNITIALIZES ALL SETS, PARAMETERS, VARIABLES, EXPRESIONS AND CONSTRAINTS IN THE MODEL. YOU CAN EXPLORE "model" variable to see the model that was builded
# The sdom model is builded by blocks of components, such as thermal, hydro, pv, wind, storage, imports, exports, etc. Each block contains the variables, expressions and constraints related to that component.
model = initialize_model( 
    data, 
    n_hours = n_steps, 
    with_resilience_constraints = with_resilience_constraints,
    model_name='SDOM_training'
    )

# UNCOMMENT TO ADD A SIMPLE CUSTOM CONSTRAINT
# from pyomo.core import Var, Constraint, Expression
# block = model.storage
# block.min_Pinstalled_constraint = Constraint( block.j, rule = lambda m,j: m.Pdis[j] >= 500 )  # Set a minimum installed power capacity of 500 MW for the storage technology 'Li-Ion-4h'

#Get a dictionary with default solver configurations
solver_dict = get_default_solver_config_dict(
    solver_name="highs", 
    executable_path=""
    )

## addd gap 
solver_dict["options"]["mip_rel_gap"] = 0.5
#Run the solver and get a solution.
best_result = run_solver(model, solver_dict)

if best_result:
    export_results(model, case, output_dir=output_dir+"\\")
else:
    print(f"Solver did not find an optimal solution for given data and with resilience constraints = {with_resilience_constraints}, skipping result export.")

# Call the script "plots_capacity_donut.py" using the local virtual environment's Python interpreter
venv_python = os.path.join(current_folder, ".venv", "Scripts", "python.exe")
#script_path = os.path.join("sample_results_Data", "sdom_plots.py")

script_path = os.path.join("training_material", "training_sesion_1", "sdom_plots.py")
subprocess.run([venv_python, script_path], check=True)
a=1