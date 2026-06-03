import os

def download_update(url):
    # Inyección de comando (CWE-78)
    print(f"Descargando actualización desde: {url}")
    os.system("curl " + url) 

if __name__ == "__main__":
    download_update("http://firmware.local/v1")