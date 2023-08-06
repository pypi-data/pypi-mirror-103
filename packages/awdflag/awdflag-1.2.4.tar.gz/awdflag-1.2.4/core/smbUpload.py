from core.getHostName import GetHostName
from smb.SMBConnection import SMBConnection
from smb import smb_structs
import ntpath
import os


def SmbConnect(host, username, password):
    hostname = GetHostName(host, username, password)
    if hostname == "":
        raise ConnectionError('Hostname 获取失败 !')
    smb_structs.SUPPORT_SMB2 = True
    try:
        conn = SMBConnection(username, password, 'localhost', hostname, use_ntlm_v2=True)
        conn.connect(host, 139)
        return conn
    except Exception as e:
        raise ConnectionError('连接SMB失败, 请确认目标139端口正常: {0}, 正在退出脚本!'.format(e))


def SmbUpload(conn, src_path, dst_path):
    if conn:
        src_path = os.path.abspath(src_path)
        share_driver, dst_filename = ntpath.splitdrive(dst_path)
        if not share_driver:
            raise ConnectionError('上传路径异常, 请检查{0}'.format(dst_path))
        share_driver = share_driver[:-1] + '$'
        dst_filename = dst_filename.replace('//', '/').replace('/', '\\')
        with open(src_path, 'rb') as file_obj:
            conn.storeFile(share_driver, dst_filename, file_obj)
