import requests
import urllib3
import json

# SSL hatalarını gizle
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- AYARLAR ---
INPUT_FILE = "domains.txt"   
OUTPUT_FILE = "evreka.txt"   
TARGET_VERSIONS = ["1.82.7", "1.82.8"] # Bu versiyonlar özel olarak işaretlenecek
KEYWORD = "LiteLLM"
TIMEOUT = 4 
# --------------

def check_url(url):
    """
    Sistemin LiteLLM olup olmadığını kontrol eder. 
    LiteLLM ise (True, Versiyon) döner.
    """
    full_url = f"{url.strip('/')}/openapi.json"
    try:
        response = requests.get(full_url, timeout=TIMEOUT, verify=False)
        
        if response.status_code == 200:
            content = response.text
            
            # Anahtar kelime kontrolü (Büyük/küçük harf duyarsız)
            if KEYWORD.lower() in content.lower():
                version = "Bilinmiyor" # Varsayılan değer
                try:
                    data = response.json()
                    version = data.get("info", {}).get("version", "Bilinmiyor")
                except:
                    pass # JSON parse edilemezse versiyon "Bilinmiyor" kalır
                
                return True, version
    except:
        pass
    return False, None

def main():
    try:
        with open(INPUT_FILE, "r") as f:
            targets = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Hata: {INPUT_FILE} bulunamadı!")
        return

    print(f"[*] {len(targets)} hedef taranıyor...")
    print(f"[*] Kriter: İçerikte '{KEYWORD}' geçmesi yeterli.\n")

    for target in targets:
        clean_target = target.replace("http://", "").replace("https://", "")
        
        variations = [
            f"http://{clean_target}",
            f"https://{clean_target}",
            f"http://{clean_target}:4000",
            f"https://{clean_target}:4000"
        ] if ":" not in clean_target else [f"http://{clean_target}", f"https://{clean_target}"]

        found_any = False
        for url in variations:
            print(f"[*] Deneniyor: {url}", end="\r") 
            is_litellm, ver = check_url(url)
            
            if is_litellm:
                # Özel bir versiyon mu?
                tag = "[ZAFİYETLİ OLABİLİR]" if ver in TARGET_VERSIONS else ""
                
                result_msg = f"[+] LITELLM BULUNDU: {url} | Versiyon: {ver} {tag}"
                print("\n" + result_msg)
                
                # Her halükarda dosyaya yazıyoruz
                with open(OUTPUT_FILE, "a") as out:
                    out.write(f"{url} | Versiyon: {ver} {tag}\n")
                
                found_any = True
                break 
        
    print("\n\n[+] Tarama bitti. Tüm LiteLLM sistemleri -> " + OUTPUT_FILE)

if __name__ == "__main__":
    main()
