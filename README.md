# AI Corrosion Detection Pipeline

This project automates training and retraining for corrosion detection using Azure resources.  
It includes scripts for starting/stopping VMs, running pipelines, and managing model weights in Azure Blob Storage.

---

## 📂 Project Structure

```
├── run_ai_corrosion.sh       # Script to start the pipeline
├── stop_ai_corrosion.sh      # Script to stop the pipeline
├── upload_blob.py            # Upload trained model weights to Azure Blob
├── start_vm.py               # Start VM via Azure API
├── stop_vm.py                # Stop VM via Azure API
├── utils/
│   └── path.json             # JSON file with metadata (e.g., new filename for model)
└── README.md
```

---

## 🚀 Requirements

- Python 3.11+
- Miniconda or Conda environment
- Azure CLI (`az`) installed and logged in
- Azure credentials for API-based VM start/stop
- Azure Storage account connection string

Install dependencies:

```bash
pip install requests azure-storage-blob
```

---

## ▶️ Running the Pipeline

To run the corrosion detection pipeline:

```bash
bash run_ai_corrosion.sh
```

This will:
1. Activate Conda environment  
2. Pull latest code  
3. Clean datasets  
4. Run `dvc repro` pipeline  
5. Train the model  

Logs are stored via `systemd` (`journalctl -u ai_corrosion.service -f`).

---

## ⏹ Stopping the Pipeline

```bash
bash stop_ai_corrosion.sh
```

This will gracefully stop the running process managed by systemd.

---

## ☁️ Start/Stop VM via API

We use **Python scripts with Azure REST API** to control VM lifecycle.

### 🔹 Start VM

```bash
python start_vm.py
```

**start_vm.py**
```python
import requests
import os

TENANT_ID = os.getenv("AZURE_TENANT_ID")
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID")
RESOURCE_GROUP = "myResourceGroup"
VM_NAME = "ai1"

# 1. Get Access Token
token_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/token"
payload = {
    "grant_type": "client_credentials",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "resource": "https://management.azure.com/"
}
token = requests.post(token_url, data=payload).json()["access_token"]

# 2. Start VM
url = f"https://management.azure.com/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{RESOURCE_GROUP}/providers/Microsoft.Compute/virtualMachines/{VM_NAME}/start?api-version=2022-11-01"
headers = {"Authorization": f"Bearer {token}"}
res = requests.post(url, headers=headers)
print("Start VM Response:", res.status_code, res.text)
```

### 🔹 Stop VM

```bash
python stop_vm.py
```

**stop_vm.py**
```python
import requests
import os

TENANT_ID = os.getenv("AZURE_TENANT_ID")
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID")
RESOURCE_GROUP = "myResourceGroup"
VM_NAME = "ai1"

# 1. Get Access Token
token_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/token"
payload = {
    "grant_type": "client_credentials",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "resource": "https://management.azure.com/"
}
token = requests.post(token_url, data=payload).json()["access_token"]

# 2. Stop VM
url = f"https://management.azure.com/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{RESOURCE_GROUP}/providers/Microsoft.Compute/virtualMachines/{VM_NAME}/powerOff?api-version=2022-11-01"
headers = {"Authorization": f"Bearer {token}"}
res = requests.post(url, headers=headers)
print("Stop VM Response:", res.status_code, res.text)
```

---

## 📦 Upload Model to Azure Blob

After training, the model (`model_final.pth`) is renamed using `utils/path.json`  
and uploaded to the `ai-weight` container.

```bash
python upload_blob.py
```

---

## 🔄 Automation

You can configure **systemd service** to automatically run `run_ai_corrosion.sh` when VM starts.  
Logs can be monitored via:

```bash
journalctl -u ai_corrosion.service -f
```

---

## 📜 License
MIT
