from nmb.NetBIOS import NetBIOS
from core.winRmExec import WinRmExec


def GetHostName(host, username, password, timeout=30):
    bios = NetBIOS()
    hostname = bios.queryIPForName(host, timeout=timeout)
    bios.close()

    if hostname:
        return hostname[0]

    hostname = WinRmExec(host, username, password, 'hostname')
    if hostname:
        return hostname
    else:
        return False
