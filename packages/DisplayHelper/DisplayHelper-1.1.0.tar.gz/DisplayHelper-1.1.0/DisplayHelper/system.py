import json
import socket
import platform

def load_system_properties():
    uname = platform.uname()
    props = {
        "system": uname.system,
        "node": uname.node,
        "release": uname.release,
        "version": uname.version,
        "machine": uname.machine,
        "processor": uname.processor,
        'hostname': socket.gethostname()
    }
    with open('/etc/os-release', "rt") as f:
        for line in f:
            l = line.strip()
            if l and not l.startswith('#'):
                key_value = l.split('=')
                key = key_value[0].strip()
                value = '='.join(key_value[1:]).strip().strip('"')
                props[key] = value
    return props
