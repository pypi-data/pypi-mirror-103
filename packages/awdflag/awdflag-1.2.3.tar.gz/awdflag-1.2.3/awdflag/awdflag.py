# coding:utf-8
# !/usr/bin/env python3
try:
    from core.logger import setLog
    from core.smbUpload import *
    from core.winRmExec import *
    from core.sshUpload import *
    from core.winRmUpload import *
    from core.smbExec import SmbExec
    from core.wmiExec import WmiExec
    from core.checkPort import CheckPort
    from core.psUpload import PowershellUp
    from core.sqlServer import MSSQL
    from core.oracle import ORACLE
    from core.zipObj import zipEnc
    import random
    import string
    import base64
    import json
    import sys
except Exception as err:
    from core.exception import AwdExceptions

    raise AwdExceptions(str(err))

logger = setLog()


def WinFile(host, username, password, dst_path, src_code="", flagFormat="flag{{}}", noZip=True):
    src_path = "/tmp/{}.txt".format(flagGenerator(16))
    if src_code == "":
        src_code = flagFormat.fromat(flagGenerator(16))

    if noZip:
        with open(src_path, 'w') as f:
            f.write(src_code)
    else:
        tmpPath = "/tmp/{}.zip".format(flagGenerator(16))
        zipEnc(src_path=src_path, dst_path=tmpPath, passwd=password, deleteSource=False)
        src_path = tmpPath

    WinRmUpload(host, username, password, src_path, dst_path)


def LinuxFile(host, port, username, password, dst_path, src_code="", flagFormat="flag{{}}", noZip=True):
    src_path = "/tmp/{}.txt".format(flagGenerator(16))
    if src_code == "":
        src_code = flagFormat.fromat(flagGenerator(16))

    if noZip:
        with open(src_path, 'w') as f:
            f.write(src_code)
    else:
        tmpPath = "/tmp/{}.zip".format(flagGenerator(16))
        zipEnc(src_path=src_path, dst_path=tmpPath, passwd=password, deleteSource=False)
        src_path = tmpPath

    # 优先使用SFTP传输方式
    SSHUpload(host, port, username, password, src_path, dst_path, keyPath="/root/.ssh/id_rsa")

    # logger.debug('{0} - {1}: \tSFTP 传输文件失败, 采用SSH命令传输 !'.format(host, types))
    # # 使用SSH命令传输方式
    # fileCode = base64.b64encode(src_path.encode('utf-8')).decode()
    # command = "echo {0}|base64 -d>{1}".format(fileCode, dst_path)
    # if SSHExec(host, port, username, password, command, dst_path, keypath="/root/.ssh/id_rsa"):
    #     logger.debug('{0} - {1}: \t文件传输成功 !'.format(host, types))
    #     return True
    # logger.debug('{0} - {1}: \t文件传输失败 !'.format(host, types))
    # return False


def linuxMysql(host, port, username, password, update_cmd):
    SSHExec(host, port, username, password, update_cmd)


def WinMysql(host, username, password, update_cmd):
    WinRmExec(host, username, password, update_cmd)


def MssqlDb(host, username, password, update_sql, select_sql, flag):
    ms = MSSQL(host=host, username=username, password=password, db="master")
    ms.ExecNonQuery(update_sql.encode('utf-8'))

    resList = ms.ExecQuery(select_sql)
    for i in resList:
        if flag in i:
            return True
    return False


def OracleDb(host, username, password, update_sql, select_sql, flag):
    od = ORACLE(host=host, username=username, password=password, db="orcl")
    od.ExecNonQuery(update_sql.encode('utf-8'))

    resList = od.ExecQuery(select_sql)
    for i in resList:
        if flag in i:
            return True
    return False


def flagGenerator(size=16, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
