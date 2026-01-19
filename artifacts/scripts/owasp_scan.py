import os, time, requests, json, base64

DTRACK_URL = "http://dtrack-apiserver:8080"
API_KEY = os.getenv("DT_API_KEY")
SBOM_PATH = "/sboms/case-study/deidentified-samd.sbom.json"
OUTPUT_FILE = "vuln_list.json"

HEADERS = {
    "X-Api-Key": API_KEY,
    "Content-Type": "application/json"
}

def upload_sbom():
    with open(SBOM_PATH, "rb") as f:
        sbom_data = f.read()
    encoded_sbom = base64.b64encode(sbom_data).decode("utf-8")

    payload = {
        "projectName": "SBOM Scan",
        "projectVersion": "1.0",
        "autoCreate": True,
        "bom": encoded_sbom
    }

    resp = requests.put(
        f"{DTRACK_URL}/api/v1/bom",
        headers=HEADERS,
        data=json.dumps(payload)
    )

    print(f"Status code from upload: {resp.status_code}")
    print(f"Response body:\n{resp.text}")

    if resp.status_code not in (202, 200):
        raise Exception(f"❌ Upload failed: {resp.status_code}, {resp.text}")

    return resp.json().get("token")

def wait_for_processing(token):
    for _ in range(20):
        time.sleep(5)
        r = requests.get(f"{DTRACK_URL}/api/v1/bom/token/{token}", headers=HEADERS)
        if not r.json().get("processing"):
            return
    raise TimeoutError("SBOM processing timed out")

def get_project_uuid():
    r = requests.get(f"{DTRACK_URL}/api/v1/project?name=SBOM Scan&version=1.0", headers=HEADERS)
    return r.json()[0]["uuid"]

def get_vulnerabilities(project_uuid):
    url = f"{DTRACK_URL}/api/v1/vulnerability/project/{project_uuid}"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    
    results = []
    for vuln in r.json():
        severity = vuln.get("severity", "UNKNOWN")
        for comp in vuln.get("components", []):
            results.append({
                "cve": vuln.get("vulnId"),
                "severity": severity,
                "name": comp.get("name"),
                "version": comp.get("version")
            })
    return results

if __name__ == "__main__":
    print("Uploading SBOM...")
    token = upload_sbom()

    print("Waiting for analysis to complete...")
    wait_for_processing(token)

    print("Fetching vulnerability results...")
    uuid = get_project_uuid()
    vulns = get_vulnerabilities(uuid)

    if not vulns:
        print("No vulnerabilities found or project not analyzed correctly.")
        print("Try verifying if the SBOM was uploaded successfully and matches known vulnerable packages.")
    else:
        with open(OUTPUT_FILE, "w") as f:
            json.dump(vulns, f, indent=2)
        print(f"Saved {len(vulns)} vulnerabilities to {OUTPUT_FILE}")