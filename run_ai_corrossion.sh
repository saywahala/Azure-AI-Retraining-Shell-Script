#!/bin/bash
set -e

LOGFILE="$HOME/ai_logs/ai_corrosion_$(date +'%Y%m%d_%H%M%S').log"

{
    echo "=== Starting AI Corrosion Pipeline at $(date) ==="
    # Load conda from miniconda3
    . /home/azureuser/miniconda3/etc/profile.d/conda.sh
#    echo "=== source created==="
    conda activate sc
    echo "conda activate"

    cd ~/StteelCorrAI/src/python/projects/ai_corrosion_detection
    
    . ../../../../dist/export/python/virtualenvs/project_ai_corrosion_detection_pipeline/3.11.13/bin/activate
    echo "Soource22 activated"
    export PYTHONPATH=$(pwd)/../../libs/common:$PYTHONPATH
    export APP_DOTENV_PATH=.local_dev/.env
    echo "env set"
    echo "Pulling latest code from Git..."
    
    #git pull
    #dvc pull

# Remove dataset folders (only if they exist)
    [ -d resources/data/dataset/images ] && rm -r resources/data/dataset/images
    [ -d resources/data/dataset/labels ] && rm -r resources/data/dataset/labels

# Remove ml_outputs only if it exists
    [ -d ml_outputs ] && rm -r ml_outputs

    #rm -r resources/data/dataset/images/
    #rm -r resources/data/dataset/labels/
    #rm -r ml_outputs
    echo "pull done"
    echo "Running DVC pipeline..."
    # 1️⃣ Run hello-world stage
    dvc repro hello-world

# 2️⃣ Run dataset download
    dvc repro download_dataset

# 3️⃣ Split train/val
    dvc repro split-train-val 

# 4️⃣ Calculate mean/std
    dvc repro calculate-mean-std

# 5️⃣ Add false positives to train set
    dvc repro add-false-positives-to-train
    python mv.py
    dvc repro train --single-item --no-run-cache
    echo "training start"
   
    echo "=== Finished at $(date) ==="

   python upload_blob.py
 echo "=== upload done === "
#    python stop.py
} | tee -a "$LOGFILE"
