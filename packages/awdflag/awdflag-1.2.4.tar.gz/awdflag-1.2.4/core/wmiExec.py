import ntpath, random, string, time
from impacket.dcerpc.v5.dcomrt import DCOMConnection
from impacket.smbconnection import SMBConnection
from impacket.dcerpc.v5.dcom import wmi
from impacket.dcerpc.v5.dtypes import NULL


def gen_random_string(length=10):
    return ''.join(random.sample(string.ascii_letters, int(length)))


class WMIEXEClass:
    def __init__(self, target, username, password, domain='', doKerberos=False, aesKey=None, kdcHost=None,
                 hashes=None, share='C$'):
        self.__target = target
        self.__username = username
        self.__password = password
        self.__domain = domain
        self.__lmHash = ''
        self.__ntHash = ''
        self.__share = share
        self.__output = None
        self.__outputBuffer = b''
        self.__share_name = gen_random_string(6)
        self.__smbConnection = SMBConnection(self.__target, self.__target)
        self.__shell = 'cmd.exe /Q /c '
        self.__pwd = 'C:\\'
        self.__aesKey = aesKey
        self.__kdcHost = kdcHost
        self.__doKerberos = doKerberos
        self.__retOutput = True
        self.__ntlmFallback = True

        self.__smbConnection.login(self.__username, self.__password)

        if hashes is not None:
            # This checks to see if we didn't provide the LM Hash
            if hashes.find(':') != -1:
                self.__lmHash, self.__ntHash = hashes.split(':')
            else:
                self.__ntHash = hashes

        if self.__password is None:
            self.__password = ''
        self.__dcom = DCOMConnection(self.__target, self.__username, self.__password, self.__domain, self.__lmHash,
                                     self.__ntHash, self.__aesKey, oxidResolver=True, doKerberos=self.__doKerberos,
                                     kdcHost=self.__kdcHost)
        iInterface = self.__dcom.CoCreateInstanceEx(wmi.CLSID_WbemLevel1Login, wmi.IID_IWbemLevel1Login)
        iWbemLevel1Login = wmi.IWbemLevel1Login(iInterface)
        iWbemServices = iWbemLevel1Login.NTLMLogin('//./root/cimv2', NULL, NULL)
        iWbemLevel1Login.RemRelease()

        self.__win32Process, _ = iWbemServices.GetObject('Win32_Process')

    def execute(self, command, output=True):
        self.__retOutput = output
        if self.__retOutput:
            self.__smbConnection.setTimeout(100000)
        self.execute_handler(command)
        self.__dcom.disconnect()
        try:
            if isinstance(self.__outputBuffer, str):
                return self.__outputBuffer
            return self.__outputBuffer
        except UnicodeDecodeError:
            return self.__outputBuffer.decode('cp437')

    def cd(self, s):
        self.execute_remote('cd ' + s)
        if len(self.__outputBuffer.strip('\r\n')) > 0:
            print(self.__outputBuffer)
            self.__outputBuffer = b''
        else:
            self.__pwd = ntpath.normpath(ntpath.join(self.__pwd, s))
            self.execute_remote('cd ')
            self.__pwd = self.__outputBuffer.strip('\r\n')
            self.__outputBuffer = b''

    def output_callback(self, data):
        self.__outputBuffer += data

    def execute_handler(self, data):
        if self.__retOutput:
            try:
                self.execute_remote(data)
            except Exception as e:
                self.cd('\\')
                self.execute_remote(data)
        else:
            self.execute_remote(data)

    def execute_remote(self, data):
        self.__output = '\\Windows\\Temp\\' + gen_random_string(6)

        command = self.__shell + data
        if self.__retOutput:
            command += ' 1> ' + '\\\\127.0.0.1\\%s' % self.__share + self.__output + ' 2>&1'

        self.__win32Process.Create(command, self.__pwd, None)
        self.get_output_remote()

    def get_output_remote(self):
        while True:
            try:
                self.__smbConnection.getFile(self.__share, self.__output, self.output_callback)
                break
            except Exception as e:
                if str(e).find('STATUS_SHARING_VIOLATION') >= 0:
                    time.sleep(1)
                else:
                    pass
        self.__smbConnection.deleteFile(self.__share, self.__output)


def WmiExec(host, username, password, command):
    exec_method = WMIEXEClass(host, username, password)
    return exec_method.execute(command)
