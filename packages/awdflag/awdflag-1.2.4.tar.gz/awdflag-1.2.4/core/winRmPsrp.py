from pypsrp.client import Client


def WinRmUpload(host, username, password, src_path, dst_path, port=None):
    client = Client(host, port=port, username=username, password=password, ssl=False, auth="ntlm")
    client.copy(src_path, dst_path)


def WinRmPsExec(host, username, password, command, port=None):
    client = Client(host, port=port, username=username, password=password, ssl=False, auth="ntlm")
    output, streams, had_errors = client.execute_ps(command)
    if not had_errors:
        return output
    raise ConnectionError("{} 执行PS命令失败".format(host))


def WinRmCMDExec(host, username, password, command, port=None):
    client = Client(host, port=port, username=username, password=password, ssl=False, auth="ntlm")
    output, streams, had_errors = client.execute_cmd(command=command)
    if not had_errors:
        return output
    raise ConnectionError("{} 执行PS命令失败".format(host))
