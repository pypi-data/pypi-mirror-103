try:
    import winrm
    import base64
except Exception as err:
    from core.exception import AwdExceptions
    raise AwdExceptions(str(err))


class PsUpload:
    def __init__(self,host,username,password):
        self.host = host
        self.username = username
        self.password = password
        self._sess = winrm.Session('http://{}:5985/wsman'.format(self.host), auth=(self.username, self.password))

    def remove_file(self,location):
        ps_script = "Remove-Item {}".format(location)
        r = self._sess.run_ps(ps_script)
        if r.status_code == 1:
            return False
        return True

    def check_file(self,location):
        ps_script = "Test-Path {}".format(location)
        r = self._sess.run_ps(ps_script)
        if r.status_code == 1:
            return False
        if 'True' in r.std_out.decode('utf-8'):
            return True
        return False

    def put_file(self, location, contents):
        step = 400
        for i in range(0, len(contents), step):
                self._do_put_file(location, contents[i:i+step])

    def _do_put_file(self, location, contents):
        ps_script = """
                    $filePath = "{location}"
                    $s = @"
                    {b64_contents}
                    "@
                    $data = [System.Convert]::FromBase64String($s)
                    add-content -value $data -encoding byte -path $filePath
                    """.format(location = location, b64_contents = base64.b64encode(contents.encode('utf_16_le')).decode('ascii')).replace("  ","")

        r = self._sess.run_ps(ps_script)


def PsUpload(host, username, password,location,contents):
    winPs = PsUpload(host, username, password)
    # 判断是否存在文件, 存在则删除
    if winPs.check_file(location):
        winPs.remove_file(location)
    # 上传文件
    winPs.put_file(location,contents)
    # 检查是否成功上传文件
    if winPs.check_file(location):
        return True
    return False
