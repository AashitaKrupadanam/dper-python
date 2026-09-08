#!/bin/bash
#SBATCH --job-name=fish_school
#SBATCH --output=fish_%j.out
#SBATCH --error=fish_%j.err
#SBATCH --time=08:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=16G
#SBATCH --partition=standard

module load python/gcc/9.4.0/nocuda/linux-rhel8-zen2/3.8.12

source ~/added-mass/new_environment.py/bin/activate

export NUMBA_CACHE_DIR=$SLURM_TMPDIR/.numba_cache
mkdir -p $NUMBA_CACHE_DIR

cd ~/added-mass

echo "Start: $(date)"
python3 school_main.py
echo "End: $(date)"