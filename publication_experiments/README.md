# Getting xStream
1. Clone the original repository from the authors: [https://github.com/cmuxstream/cmuxstream-core](https://github.com/cmuxstream/cmuxstream-core)
2. Follow the instructions in `cpp/README.md` to compile it for your environment.
3. Set the `xStream_path` parameter in `experiment_comparison/main.py` to point to your compiled xStream.

# Setting up the environment used in the experiments
The file `env_freeze.txt` contains the output of `conda list` from the environment used in the experiments. It includes more packages than strictly necessary but can be used as a reference for package versions.

# Running the experiments
Run `python main.py` from inside each experiment folder (so the current working directory is set correctly). This will start the full experiment across all datasets using 10 parallel processes. Adjust `MAX_PARALLEL_PROCESSES` to match your system's computational capacity.

- `experiment_comparison` runs 25 random seeds per dataset.  
- `experiment_ablation` runs 50 random seeds per dataset.

# Reproducing the experiments as in the publication
Each dataset folder contains a `*_seeds.txt` file listing all seeds used in the publication. Currently, there is no automatic loader for these seeds, so you must load them manually in your code.

The experiments notebook includes a safeguard to prevent overwriting results: it checks for the existence of the folder `results_namedataset` and raises an exception if it already exists.
