import papermill as pm
import concurrent.futures
import time
import os
import odds_datasets

# --- Configuration ---
INPUT_NOTEBOOK = 'experiment_comparison_onedataset.ipynb'

# The total number of jobs you want to run
TOTAL_JOBS = len(odds_datasets.datasets_names)

# V-- This is the crucial part for your request --V
# Set the maximum number of notebooks to run in parallel at any given time.
MAX_PARALLEL_PROCESSES = 10
# ^----------------------------------------------^


def run_notebook_for_index(index):
    """
    A worker function that executes one notebook for a given index.
    This function is designed to be run in a separate process.
    """
    run_id = f"index_{index}"
    output_notebook_path = os.path.join(f"output_{run_id}.ipynb")
    
    print(f"[STARTING] Job for {run_id}...")
    
    try:
        pm.execute_notebook(
           input_path=INPUT_NOTEBOOK,
           output_path=output_notebook_path,
           parameters={'dataset_index': index, 'xStream_path': 'cmuxstream-core/cpp/xstream'},
           # Suppressing kernel output from the main script's console can be helpful
           log_output=False, 
           # stdout_file=open(os.devnull, 'w')
        )
        status = "SUCCESS"
    except Exception as e:
        status = f"FAILED: {e}"
    
    print(f"[FINISHED] Job for {run_id} with status: {status}")
    return (index, status)


if __name__ == "__main__":
    print(f"Starting parallel execution of {TOTAL_JOBS} jobs.")
    print(f"Running a maximum of {MAX_PARALLEL_PROCESSES} jobs at a time.")
    
    start_time = time.time()
    
    # Use ProcessPoolExecutor to manage a pool of worker processes
    with concurrent.futures.ProcessPoolExecutor(max_workers=MAX_PARALLEL_PROCESSES) as executor:
        
        # Create a list of indices to run, e.g., from 0 to 19
        indices_to_run = range(TOTAL_JOBS)
        
        # Submit each notebook execution as a separate job to the pool
        # executor.submit() schedules the function to be run and returns a Future object
        future_to_index = {executor.submit(run_notebook_for_index, i): i for i in indices_to_run}
        
        # Use as_completed to process results as soon as they are ready
        for future in concurrent.futures.as_completed(future_to_index):
            index = future_to_index[future]
            try:
                # .result() gets the return value from our worker function
                _, status = future.result()
                # You can add more complex result handling here if needed
            except Exception as exc:
                print(f"Job for index {index} generated an exception: {exc}")

    end_time = time.time()
    
    # --- Calculate and display total time ---
    total_time = end_time - start_time
    
    print("\n" + "="*40)
    print("All jobs completed.")
    print(f"Total execution time: {total_time:.2f} seconds.")
    print(f"Number of parallel workers: {MAX_PARALLEL_PROCESSES}")
    print("="*40)