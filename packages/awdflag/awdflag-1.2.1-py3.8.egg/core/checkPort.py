try:
    import socket
except Exception as err:
    from core.exception import AwdExceptions
    raise AwdExceptions(str(err))


def CheckPort(ip,port):
    """检测ip上的端口是否开放"""
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        s.connect((ip,int(port)))
        s.shutdown(2)
        return True
    except:
        return False
    finally:
        s.close()
