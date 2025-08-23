import requests

# Azure credentials
TENANT_ID = "b4f289ee-915d-4c36-af37-aa6df263926c"
CLIENT_ID = "392a236e-ee6d-43da-af33-12d04d6c2f44"
CLIENT_SECRET = "dI_8Q~TjUMtagPPYQmr9dMHSFtMWQ0nWS~iDWbDO"
SUBSCRIPTION_ID = "88ef4c03-73d7-465d-89cf-66d75658b062"
RESOURCE_GROUP = "steelcorr_ai_model2"
VM_NAME = "ai1"
LOCATION = "East US (Zone 1)"
API_VERSION = "2023-03-01"

# Get Azure access token
def get_access_token():
    url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "resource": "https://management.azure.com/"
    }
    resp = requests.post(url, data=payload)
    resp.raise_for_status()
    return resp.json()["access_token"]

# Stop VM
def stop_vm():
    token = get_access_token()
    url = f"https://management.azure.com/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{RESOURCE_GROUP}/providers/Microsoft.Compute/virtualMachines/{VM_NAME}/powerOff?api-version=2023-03-01"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.post(url, headers=headers)
    if resp.status_code in [200, 202]:
        print(f"🛑 VM '{VM_NAME}' is stopping...")
    else:
        raise Exception(f"❌ Failed to stop VM: {resp.text}")

if __name__ == "__main__":
    stop_vm()
