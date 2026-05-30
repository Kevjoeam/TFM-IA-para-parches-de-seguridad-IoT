def download_update(url):
    print(f"Descargando actualización desde: {url}")
    subprocess.run(["curl", url], check=True)