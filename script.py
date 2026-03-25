import requests
import urllib3
import json

# Hide SSL issues
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- CONFIGS ---
INPUT_FILE = "domains.txt"   
OUTPUT_FILE = "evreka.txt"   
TARGET_VERSIONS = ["1.82.7", "1.82.8"] # These versions will be specifically flagged
KEYWORD = "LiteLLM"
TIMEOUT = 4 
# --------------

def check_url(url):
    """
    Checks if the system is LiteLLM. 
    Returns (True, Version) if LiteLLM is detected.
    """
    full_url = f"{url.strip('/')}/openapi.json"
    try:
        response = requests.get(full_url, timeout=TIMEOUT, verify=False)
        
        if response.status_code == 200:
            content = response.text
            
            # Keyword check (Case-insensitive)
            if KEYWORD.lower() in content.lower():
                version = "Unknown" # Default value
                try:
                    data = response.json()
                    version = data.get("info", {}).get("version", "Unknown")
                except:
                    pass # Keep as "Unknown" if JSON parsing fails
                
                return True, version
    except:
        pass
    return False, None

def main():
    try:
        with open(INPUT_FILE, "r") as f:
            targets = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} not found!")
        return

    print(f"[*] Scanning {len(targets)} targets...")
    print(f"[*] Criterion: Keyword '{KEYWORD}' must be present in content.\n")

    for target in targets:
        # Clean protocol if already present in the list
        clean_target = target.replace("http://", "").replace("https://", "")
        
        # Prepare variations for ports and protocols
        if ":" not in clean_target:
            variations = [
                f"http://{clean_target}",
                f"https://{clean_target}",
                f"http://{clean_target}:4000",
                f"https://{clean_target}:4000"
            ]
        else:
            # If port is already specified, only try http and https
            variations = [f"http://{clean_target}", f"https://{clean_target}"]

        found_any = False
        for url in variations:
            # \r used to keep the terminal output clean during scanning
            print(f"[*] Trying: {url}", end="\r") 
            is_litellm, ver = check_url(url)
            
            if is_litellm:
                # Check for specific vulnerable versions
                tag = "[POTENTIALLY VULNERABLE]" if ver in TARGET_VERSIONS else ""
                
                result_msg = f"[+] LITELLM FOUND: {url} | Version: {ver} {tag}"
                print("\n" + result_msg)
                
                # Write results to file
                with open(OUTPUT_FILE, "a") as out:
                    out.write(f"{url} | Version: {ver} {tag}\n")
                
                found_any = True
                break 
        
    print("\n\n[+] Scan finished. All LiteLLM systems saved to -> " + OUTPUT_FILE)

if __name__ == "__main__":
    main()
