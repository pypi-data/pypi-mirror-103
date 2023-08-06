try:
    from nmb.NetBIOS import NetBIOS
    from core.winRmExec import WinRmExec
    import ntpath
except Exception as err:
    from core.exception import AwdExceptions

    raise AwdExceptions(str(err))


def GetHostName(host, timeout=30):
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
