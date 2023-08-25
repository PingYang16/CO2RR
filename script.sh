#!/usr/bin/env bash

#SBATCH --nodes=1
#SBATCH --gpus=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=20G
#SBATCH --time=336:00:00
#SBATCH --job-name=pretrain
#SBATCH --output stdout.%j
#SBATCH --error stderr.%j
#SBATCH --partition=gpu-long

#######################################################################
ulimit -s unlimited
module add anaconda/2022.10
eval "$(conda shell.bash hook)"
conda activate torchdrug
#######################################################################         
srun --unbuffered python ./transfer_learning.py 

exit 0