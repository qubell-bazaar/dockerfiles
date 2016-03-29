import os
import yaml
import base64
import time
import struct

directory = "/vms"

class FakeVm:
    def __init__(self, vmid, model):
        self.vmid = vmid
        self.model = model

    @property
    def name(self):
        return self.model.get('name')

    @name.setter
    def name(self, value):
        self.model['name'] = value

    @name.deleter
    def name(self):
        del self.model['name']

    @property
    def color(self):
        return self.model.get('color')

    @color.setter
    def color(self, value):
        self.model['color'] = value

    @color.deleter
    def color(self):
        del self.model['color']

    def __str__(self):
        return "FakeVm({}, {}, {})".format(self.vmid, self.color, self.name)

    def __repr__(self):
        return str(self)

def load_fake_vm(vmid):
    fpath = os.path.join(directory, vmid)
    if os.path.exists(fpath):
        with open(fpath, "r") as f:
            return FakeVm(vmid, yaml.safe_load(f))
    else:
        return None

def load_fake_vms():
    results = []
    for f in os.listdir(directory):
        fpath = os.path.join(directory, f)
        if os.path.isfile(fpath):
            results.append(load_fake_vm(f))
    return results

def load_fake_vm_ids():
    results = []
    for f in os.listdir(directory):
        fpath = os.path.join(directory, f)
        if os.path.isfile(fpath):
            results.append(f)
    return results

def fake_vm_exists(vmid):
    return os.path.isfile(os.path.join(directory, vmid))

def save_fake_vm(vm):
    fpath = os.path.join(directory, vm.vmid)
    with open(fpath, "w") as f:
        yaml.safe_dump(vm.model, f)

def destroy_fake_vm(vmid):
    fpath = os.path.join(directory, vmid)
    os.remove(fpath)

def generate_id():
    timestamp = int("".join(str(time.time()).split('.')))
    timestamp_bytes = bytes(struct.unpack("8B", struct.pack("L", timestamp)))
    return "vm-{}".format(base64.b16encode(timestamp_bytes).decode('utf-8').lower())

