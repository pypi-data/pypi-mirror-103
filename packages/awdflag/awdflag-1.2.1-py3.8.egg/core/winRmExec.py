try:
    import winrm
except Exception as err:
    from core.exception import AwdExceptions
    raise AwdExceptions(str(err))

def WinRmExec(host,username,password,cmd):
    try:
        wintest = winrm.Session('http://{}:5985/wsman'.format(host),auth=(username,password))
        ret = wintest.run_cmd(cmd)
        result = ret.std_out.decode("gbk")
        if not result:
            result = ret.std_err.decode("gbk")
        return result.replace('\r','')
    except Exception as e:
        return ''
