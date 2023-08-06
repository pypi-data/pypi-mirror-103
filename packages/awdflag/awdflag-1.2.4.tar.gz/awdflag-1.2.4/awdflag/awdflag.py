# coding:utf-8
# !/usr/bin/env python3
import base64

from core.sshUpload import *
from core.winRmPsrp import *
from core.sqlServer import MSSQL
from core.oracle import ORACLE
from core.zipObj import zipEnc
import datetime
import hashlib
import random
import string


def CheckTextFile(host, username, password, system, dst_path, flag, port=None, id_rsa=None):
    keyPath = "/tmp/{}-{}-src-path/id_rsa".format(host, datetime.date.today().strftime('%Y%m%d'))
    keyPath = InitIdRSA(keyPath, id_rsa=id_rsa)

    res = ""
    if system == "windows":
        if not port:
            port = 5985
        command = 'Get-Content "{}" | Where-Object {{$_ -match "{}"}}'.format(dst_path, flag)
        res = WinRmPsExec(host=host, port=port, username=username, password=password, command=command)
    elif system == "linux":
        if not port:
            port = 22
        command = "cat {}|grep '{}'".format(dst_path, flag)
        res = SSHExec(host=host, port=port, username=username, password=password, command=command, keyPath=keyPath)
    if flag in res:
        return True
    return False


def CheckMD5File(host, port, username, password, system, dst_path, noZip=True, id_rsa=None):
    src_path = InitCheckFlag(host=host, noZip=noZip)
    keyPath = "/tmp/{}-{}-src-path/id_rsa".format(host, datetime.date.today().strftime('%Y%m%d'))
    keyPath = InitIdRSA(keyPath, id_rsa=id_rsa)
    md5_sum = md5(src_path)
    res = ""
    if system == "windows":
        command = 'certutil -hashfile "{}" MD5'.format(dst_path)
        # Get-FileHash C:\Windows\notepad.exe -Algorithm MD5| Format-List
        res = WinRmPsExec(host=host, port=port, username=username, password=password, command=command)
    elif system == "linux":
        command = "md5sum {}".format(dst_path)
        res = SSHExec(host=host, port=port, username=username, password=password, command=command, keyPath=keyPath)

    md5_sum = " ".join([md5_sum[i:i + 2] for i in range(0, len(md5_sum), 2)])
    if md5_sum in res:
        return True

    return False


def TransFile(host, port, username, password, system, dst_path,
              src_code="", flagFormat="flag{{{}}}", noZip=True, zipPass="123456", id_rsa=None):
    src_path = InitGenFlag(host=host, src_code=src_code, zipPass=zipPass, flagFormat=flagFormat, noZip=noZip)
    keyPath = "/tmp/{}-{}-src-path/id_rsa".format(host, datetime.date.today().strftime('%Y%m%d'))
    keyPath = InitIdRSA(keyPath, id_rsa=id_rsa)
    # print(src_path, dst_path)
    if system == "windows":
        WinRmUpload(host=host, port=port, username=username, password=password, src_path=src_path, dst_path=dst_path)
    elif system == "linux":
        SSHUpload(host=host, port=port, username=username, password=password,
                  src_path=src_path, dst_path=dst_path, keyPath=keyPath)


def RuntimeExec(host, port, username, password, command, system, id_rsa=None):
    keyPath = "/tmp/{}-{}-src-path/id_rsa".format(host, datetime.date.today().strftime('%Y%m%d'))
    keyPath = InitIdRSA(keyPath, id_rsa=id_rsa)
    res = ""
    if system == "windows":
        res = WinRmPsExec(host=host, port=port, username=username, password=password, command=command)
    elif system == "linux":
        res = SSHExec(host=host, port=port, username=username, password=password, command=command, keyPath=keyPath)
    return res


def linuxMysql(host, port, username, password, update_cmd):
    SSHExec(host, port, username, password, update_cmd)


def WinMysql(host, username, password, update_cmd):
    WinRmPsExec(host, username, password, update_cmd)


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


def InitGenFlag(host, src_code, zipPass, flagFormat, noZip):
    src_path = "/tmp/{}-{}-src-path/".format(host, datetime.date.today().strftime('%Y%m%d'))
    tmp_path = "/tmp/{}-{}-src-path/flag.zip".format(host, datetime.date.today().strftime('%Y%m%d'))
    if not os.path.exists(src_path):
        os.makedirs(src_path)
    src_path += "flag.txt"
    if src_code == "":
        src_code = flagFormat.format(flagGenerator(16))
    with open(src_path, 'w') as f:
        f.write(src_code)
    if not noZip:
        zipEnc(src_path=src_path, dst_path=tmp_path, passwd=zipPass, deleteSource=False)
        src_path = tmp_path
    return src_path


def InitCheckFlag(host, noZip):
    src_path = "/tmp/{}-{}-src-path/flag.txt".format(host, datetime.date.today().strftime('%Y%m%d'))
    if not noZip:
        src_path = "/tmp/{}-{}-src-path/flag.zip".format(host, datetime.date.today().strftime('%Y%m%d'))
    return src_path


def InitIdRSA(keyPath, id_rsa):
    # 写入keyPath
    if id_rsa:
        id_rsa = base64.b64decode(id_rsa.encode())
        with open(keyPath, "wb") as f:
            f.write(id_rsa)
            os.chmod(keyPath, 0o600)
    else:
        keyPath = None
    return keyPath


def flagGenerator(size=16, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def md5(path):
    with open(path, "rb") as f:
        m = hashlib.md5()
        while True:
            data = f.read(10240)
            if not data:
                break

            m.update(data)
        return m.hexdigest()
