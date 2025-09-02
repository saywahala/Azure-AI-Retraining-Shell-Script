# AI Corrosion Detection – Model Upload to Azure Blob

This project provides a Python script to **rename a trained model file** (`model_final.pth`) based on metadata from a JSON file stored in Azure Blob Storage, and then upload the renamed model to another container for storage.

---

## 🚀 Workflow

1. **Fetch Metadata JSON**
   - Reads `utils/path.json` from the `retraining-data` container.
   - Extracts the `filename` field.

2. **Rename Model**
   - Renames the local trained model file  
     `~/StteelCorrAI/src/python/projects/ai_corrosion_detection/ml_outputs/static/detectron/model_final.pth`  
     to the new filename specified in `path.json`.

3. **Upload Model**
   - Uploads the renamed model into the `ai-weight` Azure Blob container.

---

## 📂 File Structure

```
StteelCorrAI/
└── src/python/projects/ai_corrosion_detection/
    ├── ml_outputs/static/detectron/model_final.pth
    ├── utils/path.json   (stored in Azure Blob `retraining-data`)
    └── upload_blob.py    (this script)
```

---

## ⚙️ Requirements

- Python 3.9+
- Install dependencies:

```bash
pip install azure-storage-blob
```

- Access to Azure Blob Storage with a valid **connection string**.

---

## 🔧 Configuration

Update the following in `upload_blob.py`:

```python
AZURE_CONNECTION_STRING = "your-azure-connection-string"
SRC_CONTAINER = "retraining-data"
DEST_CONTAINER = "ai-weight"
```

---

## ▶️ Usage

1. Train or generate your model.
2. Ensure `model_final.pth` exists at:

```
~/StteelCorrAI/src/python/projects/ai_corrosion_detection/ml_outputs/static/detectron/model_final.pth
```

3. Run the script:

```bash
python upload_blob.py
```

4. Output:
   - Model is renamed to `data['filename']` (from JSON).
   - Renamed model is uploaded to the `ai-weight` container in Azure Blob.

---

## 📌 Example

If `path.json` contains:

```json
{
  "filename": "corrosion_model_v1.pth"
}
```

Then:
- Local file `model_final.pth` → renamed to `corrosion_model_v1.pth`
- Uploaded to container `ai-weight/corrosion_model_v1.pth`

---

## ✅ Notes

- The script uses `shutil.move`, so the old file (`model_final.pth`) will be replaced with the renamed one locally.
- Set `overwrite=True` in upload to always replace old versions in Blob.
- You can extend the script to **delete local file after upload** if needed.

---
