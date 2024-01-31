#!/bin/bash
#SBATCH --account=swim
#SBATCH --error=koeppen-%j.err
#SBATCH --output=koeppen-%j.out
#SBATCH --time=00:59:00
#SBATCH --qos=short
######SBATCH --partition=priority
#SBATCH --nodes=1
#SBATCH --ntasks=1
#########SBATCH --cpus-per-task=1
#SBATCH --mail-user=bijan.fallah@gmail.com
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=END

conda activate bias

set -ex
echo "i will send the job now"
python chord_plot.py
