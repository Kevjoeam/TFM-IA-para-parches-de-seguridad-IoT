import subprocess

def ping(host):
    subprocess.run(f"ping {host}", shell=True)