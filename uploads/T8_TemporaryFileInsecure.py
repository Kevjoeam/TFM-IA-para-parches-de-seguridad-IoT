import tempfile

def save_data(data):
    tmp = tempfile.mktemp()
    
    with open(tmp, "w") as f:
        f.write(data)