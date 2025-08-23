import requests
import time

# === CONFIG ===
TENANT_ID = "b4f289ee-915d-4c36-af37-aa6df263926c"
CLIENT_ID = "392a236e-ee6d-43da-af33-12d04d6c2f44"
CLIENT_SECRET = "dI_8Q~TjUMtagPPYQmr9dMHSFtMWQ0nWS~iDWbDO"
SUBSCRIPTION_ID = "88ef4c03-73d7-465d-89cf-66d75658b062"
RESOURCE_GROUP = "steelcorr_ai_model2"
VM_NAME = "ai1"
LOCATION = "East US (Zone 1)"
API_VERSION = "2023-03-01"

# === 1. Get Access Token ===
print("🔑 Getting Azure access token...")
token_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/token"

payload = {
    "grant_type": "client_credentials",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "resource": "https://management.azure.com/"
}

resp = requests.post(token_url, data=payload)   # ✅ use data=, NOT json=
resp.raise_for_status()
ACCESS_TOKEN = resp.json().get("access_token")
if not ACCESS_TOKEN:
    raise Exception("❌ Failed to get Azure access token")
print("✅ Got access token")
print(ACCESS_TOKEN)
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# === 2. Start VM ===
print(f"▶️ Starting VM: {VM_NAME}")
start_url = f"https://management.azure.com/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{RESOURCE_GROUP}/providers/Microsoft.Compute/virtualMachines/{VM_NAME}/start?api-version={API_VERSION}"
print(start_url)
resp = requests.post(start_url, headers=headers)
print(resp)
if resp.status_code not in [200, 202]:
    raise Exception(f"❌ Failed to start VM: {resp.text}")
print("⏳ VM start initiated")

# === 3. Wait until VM is running ===
status_url = f"https://management.azure.com/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{RESOURCE_GROUP}/providers/Microsoft.Compute/virtualMachines/{VM_NAME}/instanceView?api-version={API_VERSION}"

while True:
    resp = requests.get(status_url, headers=headers)
    resp.raise_for_status()
    statuses = resp.json().get("statuses", [])
    power_state = [s["code"] for s in statuses if s["code"].startswith("PowerState/")]
    if power_state:
        print(f"   VM status: {power_state[0]}")
        if power_state[0] == "PowerState/running":
            print("✅ VM is running")
            break
    time.sleep(10)

# # === 4. Run Script Inside VM ===
# print("▶️ Running script inside VM...")
# run_url = f"https://management.azure.com/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{RESOURCE_GROUP}/providers/Microsoft.Compute/virtualMachines/{VM_NAME}/runCommand?api-version={API_VERSION}"

# script_payload = {
#     "commandId": "RunShellScript",   # For Linux VM. Use "RunPowerShellScript" for Windows.
#     "script": [
#         "echo Hello from inside VM >> /tmp/hello.txt",
#         "sudo systemctl restart nginx"
#     ]
# }

# resp = requests.post(run_url, headers=headers, json=script_payload)
# resp.raise_for_status()

# print("✅ Script executed inside VM")
# print("Output:", resp.json())

