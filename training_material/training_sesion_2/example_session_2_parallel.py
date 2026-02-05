
# IMPORT SDOM MODULE
###  IMPORT PACKAGES 

import sdom
from sdom import run_solver, initialize_model, configure_logging, get_default_solver_config_dict
from sdom import load_data, export_results
import logging
import highspy
import os
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed
import copy

configure_logging(level=logging.INFO)

current_folder = os.getcwd()
print("Current folder:", current_folder)

#storage_capex_factors = [1.0, 0.9, 0.8]  # Example factors for sensitivity analysis
storage_capex_factors = [1.0, 0.9]  # Example factors for sensitivity analysis


def run_simulation_with_factor(factor, current_folder):
    """
    Run a single simulation with a specific storage CAPEX factor.
    
    Parameters:
    -----------
    factor : float
        The multiplication factor to apply to storage P_capex
    current_folder : str
        The current working directory path
        
    Returns:
    --------
    tuple : (factor, success, output_dir)
        factor: the factor used
        success: whether the optimization was successful
        output_dir: the directory where results were saved
    """
    
    print(f"\n{'='*60}")
    print(f"Starting simulation with storage_capex_factor = {factor}")
    print(f"{'='*60}\n")
    
    n_steps = 730*1  # Number of steps in the simulation (IN HOURS - RECOMENDED = 8760)
    with_resilience_constraints = False
    case = f"br_test_daily_b-factor{factor}"
    
    # Load data
    data_dir = os.path.join(current_folder, "sample_data", "br_test_daily_b")
    data = load_data(data_dir)
    
    # Modify the P_capex row by multiplying with the factor
    if "storage_data" in data and "P_Capex" in data["storage_data"].index:
        print(f"Original P_capex values:\n{data['storage_data'].loc['P_Capex']}")
        data["storage_data"].loc["P_Capex"] = data["storage_data"].loc["P_Capex"] * factor
        print(f"Modified P_capex values (factor={factor}):\n{data['storage_data'].loc['P_Capex']}\n")
    else:
        print(f"WARNING: Could not find 'P_Capex' in storage_data for factor {factor}")
    
    # Set output directory
    output_dir = os.path.join(current_folder, f'sample_results_{case}')
    
    # Initialize model
    model = initialize_model(
        data,
        n_hours=n_steps,
        with_resilience_constraints=with_resilience_constraints,
        model_name=f'SDOM_training_factor_{factor}'
    )
    
    # Configure solver
    solver_dict = get_default_solver_config_dict(
        solver_name="highs",
        executable_path=""
    )
    
    # Run solver
    best_result = run_solver(model, solver_dict)
    
    # Export results
    if best_result:
        export_results(model, case, output_dir=output_dir+"\\")
        print(f"\n{'='*60}")
        print(f"Successfully completed simulation with factor = {factor}")
        print(f"Results saved to: {output_dir}")
        print(f"{'='*60}\n")
        return (factor, True, output_dir)
    else:
        print(f"\n{'='*60}")
        print(f"FAILED: Solver did not find optimal solution for factor = {factor}")
        print(f"{'='*60}\n")
        return (factor, False, output_dir)


def main():
    """
    Main function to run parallel sensitivity analysis.
    """
    print("\n" + "="*80)
    print("STARTING PARALLEL SENSITIVITY ANALYSIS")
    print(f"Number of parallel simulations: {len(storage_capex_factors)}")
    print(f"Storage CAPEX factors: {storage_capex_factors}")
    print("="*80 + "\n")
    
    # Determine the number of workers (processes)
    # You can adjust this based on your CPU cores
    # Using min to avoid creating more workers than factors
    max_workers = min(len(storage_capex_factors), os.cpu_count()-1 or 1)
    print(f"Using {max_workers} parallel workers\n")
    
    results = []
    
    # Run simulations in parallel
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_factor = {
            executor.submit(run_simulation_with_factor, factor, current_folder): factor 
            for factor in storage_capex_factors
        }
        
        # Collect results as they complete
        for future in as_completed(future_to_factor):
            factor = future_to_factor[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as exc:
                print(f"Simulation with factor {factor} generated an exception: {exc}")
                results.append((factor, False, None))
    
    # Print summary
    print("\n" + "="*80)
    print("SENSITIVITY ANALYSIS COMPLETE - SUMMARY")
    print("="*80)
    
    successful = [r for r in results if r[1]]
    failed = [r for r in results if not r[1]]
    
    print(f"\nTotal simulations: {len(results)}")
    print(f"Successful: {len(successful)}")
    print(f"Failed: {len(failed)}")
    
    if successful:
        print("\nSuccessful simulations:")
        for factor, success, output_dir in successful:
            print(f"  - Factor {factor}: {output_dir}")
    
    if failed:
        print("\nFailed simulations:")
        for factor, success, output_dir in failed:
            print(f"  - Factor {factor}")
    
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
