from azure.storage.blob import BlobServiceClient
import os
import json
import random
import shutil
from datetime import datetime, timezone

AZURE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=dprdocker;AccountKey=ubRDzyf/RTVZEW1BZPo06s4x8mGBbsUcHWYDIYzvzgSAVTFMqir8Q3qY/RysyoLBhU5OXnicRk5m+AStxzzF0w==;EndpointSuffix=core.windows.net"
CONTAINER_NAME = "retraining-data"
DEST_CONTAINER = "ai-weight"
################################
path_file = "utils/path.json"
LOCAL_MODEL_PATH = os.path.expanduser(
    "~/StteelCorrAI/src/python/projects/ai_corrosion_detection/ml_outputs/static/detectron/model_final.pth"
)
def load_json(path_file: str):
    # Try to fetch from Azure Blob Storage
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)
    blob_client = container_client.get_blob_client(path_file)

    if blob_client.exists():
        download_stream = blob_client.download_blob()
        return json.loads(download_stream.readall())
    else:
        raise FileNotFoundError(f"File {path_file} not found locally or in Azure Blob.")


data = load_json(path_file)
new_filename = data["filename"]
print(f"Renaming model to: {new_filename}")

DEST_MODEL_PATH = os.path.join(os.path.dirname(LOCAL_MODEL_PATH), new_filename)

shutil.move(LOCAL_MODEL_PATH, DEST_MODEL_PATH)



print(f"✅ Model renamed to {DEST_MODEL_PATH}")

# Upload renamed model into ai-weight container
blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
dest_container_client = blob_service_client.get_container_client(DEST_CONTAINER)

with open(DEST_MODEL_PATH, "rb") as f:
    blob_client = dest_container_client.get_blob_client(new_filename)
    blob_client.upload_blob(f, overwrite=True)
    print(f"☁️ Uploaded {new_filename} to Azure Blob in container '{DEST_CONTAINER}'")



print("Upload Done!")
