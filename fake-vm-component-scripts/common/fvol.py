import os
import yaml
import base64
import time
import struct

directory = "/volumes"

class FakeVolume:
    def __init__(self, volid, name, color, failure=None):
        self.volid = volid or generate_id()
        self.name = name
        self.color = color
        self.failure = failure

    def __str__(self):
        return "FakeVolume({}, {}, {})".format(self.volid, self.name, self.color)

    def __repr__(self):
        return str(self)

def load(volid):
    fpath = os.path.join(directory, volid)
    if os.path.exists(fpath):
        with open(fpath, "r") as f:
            model = yaml.safe_load(f)
            return FakeVolume(volid, model.get('name'), model['color'], model.get('failure'))
    else:
        return None

def load_all():
    results = []
    for f in os.listdir(directory):
        fpath = os.path.join(directory, f)
        if os.path.isfile(fpath):
            results.append(load(f))
    return results

def load_ids():
    results = []
    for f in os.listdir(directory):
        fpath = os.path.join(directory, f)
        if os.path.isfile(fpath):
            results.append(f)
    return results

def exists(volid):
    return os.path.isfile(os.path.join(directory, volid))

def save(vol):
    fpath = os.path.join(directory, vol.volid)
    with open(fpath, "w") as f:
        yaml.safe_dump({'name': vol.name, 'color': vol.color, 'failure': vol.failure}, f)

def delete(volid):
    fpath = os.path.join(directory, volid)
    os.remove(fpath)

def generate_id():
    timestamp = int("".join(str(time.time()).split('.')))
    timestamp_bytes = bytes(struct.unpack("8B", struct.pack("L", timestamp)))
    return "vol-{}".format(base64.b16encode(timestamp_bytes).decode('utf-8').lower())

