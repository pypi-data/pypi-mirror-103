try:
    import winrm
except Exception as err:
    from core.exception import AwdExceptions

    raise AwdExceptions(str(err))


def WinRmExec(host, username, password, cmd, port=5985):
    conn = winrm.Session("http://{}:{}/wsman".format(host, port), auth=(username, password))
    ret = conn.run_cmd(cmd)
    result = ret.std_out.decode("gbk")
    if not result:
        result = ret.std_err.decode("gbk")
    return result.replace('\r', '')
