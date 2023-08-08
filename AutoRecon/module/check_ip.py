import socket

def is_valid_ip(target):
    try:
        socket.inet_pton(socket.AF_INET, target)
        return True
    except socket.error:
        pass
    try:
        socket.inet_pton(socket.AF_INET6, target)
        return True
    except socket.error:
        pass
    return False  

def is_valid_asn(target):
    try:
        asn = int(target)
        return 1 <= asn <= 65535
    except ValueError:
        return False
