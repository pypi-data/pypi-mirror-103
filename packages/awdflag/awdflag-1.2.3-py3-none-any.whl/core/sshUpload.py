#!/usr/bin/python
# coding:utf-8

try:
    import os
    import stat
    import paramiko
    import traceback
    from core.exception import AwdExceptions
except Exception as err:
    from core.exception import AwdExceptions

    raise AwdExceptions(str(err))


class SSH(object):

    def __init__(self, host, port=22, username="root", password=None, keyPath="/root/.ssh/id_rsa", timeout=30):
        self.ip = host
        self.port = port
        self.username = username
        self.password = password
        self.timeout = timeout
        self.keyPath = keyPath

        self.ssh = paramiko.SSHClient()
        self.t = paramiko.Transport(sock=(self.ip, self.port))

    def _password_connect(self):
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=self.ip, port=self.port, username=self.username, password=self.password)
        self.t.connect(username=self.username, password=self.password)  # sptf 远程传输的连接

    def _key_connect(self):
        self.pkey = paramiko.RSAKey.from_private_key_file(self.keyPath, )
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=self.ip, port=self.port, username=self.username, pkey=self.pkey)
        self.t.connect(username=self.username, pkey=self.pkey)

    def connect(self):
        try:
            self._key_connect()
        except Exception as e:
            self._password_connect()

    def close(self):
        self.t.close()
        self.ssh.close()

    def execute_cmd(self, cmd):
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        res, error = stdout.read(), stderr.read()
        result = res if res else error
        return result.decode()

    # 从远程服务器获取文件到本地
    def _sftp_get(self, remoteFile, localFile):
        sftp = paramiko.SFTPClient.from_transport(self.t)
        sftp.get(remoteFile, localFile)

    # 从本地上传文件到远程服务器
    def sftp_put(self, localFile, remoteFile):
        sftp = paramiko.SFTPClient.from_transport(self.t)
        sftp.put(localFile, remoteFile)

    # 递归遍历远程服务器指定目录下的所有文件
    def _get_all_files_in_remote_dir(self, sftp, remote_dir):
        all_files = list()
        if remote_dir[-1] == '/':
            remote_dir = remote_dir[0:-1]

        files = sftp.listdir_attr(remote_dir)
        for file in files:
            filename = remote_dir + '/' + file.filename
            if stat.S_ISDIR(file.st_mode):  # 如果是文件夹的话递归处理
                all_files.extend(self._get_all_files_in_remote_dir(sftp, filename))
            else:
                all_files.append(filename)
        return all_files

    def sftp_get_dir(self, remote_dir, local_dir):
        sftp = paramiko.SFTPClient.from_transport(self.t)
        all_files = self._get_all_files_in_remote_dir(sftp, remote_dir)
        for file in all_files:
            local_filename = file.replace(remote_dir, local_dir)
            local_filepath = os.path.dirname(local_filename)
            if not os.path.exists(local_filepath):
                os.makedirs(local_filepath)
            sftp.get(file, local_filename)

    # 递归遍历本地服务器指定目录下的所有文件
    @staticmethod
    def _get_all_files_in_local_dir(local_dir):
        all_files = list()

        for root, dirs, files in os.walk(local_dir, topdown=True):
            for file in files:
                filename = os.path.join(root, file)
                all_files.append(filename)

        return all_files

    def sftp_put_dir(self, local_dir, remote_dir):
        sftp = paramiko.SFTPClient.from_transport(self.t)

        if remote_dir[-1] == "/":
            remote_dir = remote_dir[0:-1]

        all_files = self._get_all_files_in_local_dir(local_dir)
        for file in all_files:
            remote_filename = file.replace(local_dir, remote_dir)
            remote_path = os.path.dirname(remote_filename)
            try:
                sftp.stat(remote_path)
            except Exception as e:
                os.popen('mkdir -p %s' % remote_path)

            sftp.put(file, remote_filename)
            # print('ssh get dir from master failed.')
            # print(traceback.format_exc())

    def checkFile(self, dst_path):
        sftp = paramiko.SFTPClient.from_transport(self.t)
        sftp.stat(dst_path)


def SSHExec(host, port, username, password, command, dst_path=None, keyPath="/root/.ssh/id_rsa"):
    conn = SSH(host=host, port=port, username=username, password=password, keyPath=keyPath, timeout=30)
    conn.connect()
    if dst_path:
        return conn.checkFile(dst_path)
    return conn.execute_cmd(command)


def SSHUpload(host, port, username, password, src_path, dst_path, keyPath="/root/.ssh/id_rsa"):
    conn = SSH(host=host, port=port, username=username, password=password, keyPath=keyPath, timeout=30)
    conn.connect()
    if os.path.isdir(src_path):
        conn.sftp_put_dir(src_path, dst_path)
    else:
        conn.sftp_put(src_path, dst_path)

    return conn.checkFile(dst_path)
