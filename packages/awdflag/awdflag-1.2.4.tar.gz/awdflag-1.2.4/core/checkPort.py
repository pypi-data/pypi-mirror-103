import socket


def CheckPort(ip, port):
    """检测ip上的端口是否开放"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(5)
        s.connect((ip, int(port)))
    except Exception as e:
        raise ConnectionError("{}:{} 连接异常: {}".format(ip, port, e))
    finally:
        s.close()
