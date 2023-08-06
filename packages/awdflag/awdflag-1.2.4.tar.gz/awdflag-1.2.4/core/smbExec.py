from __future__ import division
from __future__ import print_function
import sys
import os
import cmd
from threading import Thread

try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser

from impacket import smbserver
from impacket.dcerpc.v5 import transport, scmr

OUTPUT_FILENAME = '__output'
BATCH_FILENAME = 'execute.bat'
SMBSERVER_DIR = '__tmp'
DUMMY_SHARE = 'TMP'
SERVICE_NAME = 'BTOBTO'
CODEC = sys.stdout.encoding


class __Autonomy__(object):
    def __init__(self):
        self._buff = ""

    def write(self, out_stream):
        self._buff += out_stream


class SMBServer(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.smb = None

    def cleanup_server(self):
        try:
            os.unlink(SMBSERVER_DIR + '/smb.log')
        except OSError:
            pass
        os.rmdir(SMBSERVER_DIR)

    def run(self):
        # Here we write a mini config for the server
        smbConfig = ConfigParser.ConfigParser()
        smbConfig.add_section('global')
        smbConfig.set('global', 'server_name', 'server_name')
        smbConfig.set('global', 'server_os', 'UNIX')
        smbConfig.set('global', 'server_domain', 'WORKGROUP')
        smbConfig.set('global', 'log_file', SMBSERVER_DIR + '/smb.log')
        smbConfig.set('global', 'credentials_file', '')

        # Let's add a dummy share
        smbConfig.add_section(DUMMY_SHARE)
        smbConfig.set(DUMMY_SHARE, 'comment', '')
        smbConfig.set(DUMMY_SHARE, 'read only', 'no')
        smbConfig.set(DUMMY_SHARE, 'share type', '0')
        smbConfig.set(DUMMY_SHARE, 'path', SMBSERVER_DIR)

        # IPC always needed
        smbConfig.add_section('IPC$')
        smbConfig.set('IPC$', 'comment', '')
        smbConfig.set('IPC$', 'read only', 'yes')
        smbConfig.set('IPC$', 'share type', '3')
        smbConfig.set('IPC$', 'path')

        self.smb = smbserver.SMBSERVER(('0.0.0.0', 445), config_parser=smbConfig)
        try:
            os.mkdir(SMBSERVER_DIR)
        except Exception as e:
            print(str(e))
            pass
        print('Setting up SMB Server')
        self.smb.processConfigFile()
        print('Ready to listen...')
        try:
            self.smb.serve_forever()
        except:
            pass

    def stop(self):
        self.cleanup_server()
        self.smb.socket.close()
        self.smb.server_close()
        self._Thread__stop()


class CMDEXEC:
    def __init__(self, username='', password=''):

        self.__username = username
        self.__password = password
        self.__port = 445
        self.__serviceName = SERVICE_NAME
        self.__domain = ''
        self.__lmhash = ''
        self.__nthash = ''
        self.__aesKey = None
        self.__doKerberos = False
        self.__kdcHost = None
        self.__share = 'C$'
        self.__mode = 'SHARE'
        self.shell = None
        self.hashes = None
        if self.hashes is not None:
            self.__lmhash, self.__nthash = hashes.split(':')

    def run(self, remoteName, remoteHost, command):
        stringbinding = r'ncacn_np:%s[\pipe\svcctl]' % remoteName
        rpctransport = transport.DCERPCTransportFactory(stringbinding)
        rpctransport.set_dport(self.__port)
        rpctransport.setRemoteHost(remoteHost)
        if hasattr(rpctransport, 'set_credentials'):
            # This method exists only for selected protocol sequences.
            rpctransport.set_credentials(self.__username, self.__password, self.__domain, self.__lmhash,
                                         self.__nthash, self.__aesKey)
        rpctransport.set_kerberos(self.__doKerberos, self.__kdcHost)

        self.shell = None
        try:
            if self.__mode == 'SERVER':
                serverThread = SMBServer()
                serverThread.daemon = True
                serverThread.start()
            self.shell = RemoteShell(self.__share, rpctransport, self.__mode, self.__serviceName)
            # self.shell.cmdloop()

            current = sys.stdout
            a = __Autonomy__()
            sys.stdout = a
            self.shell.onecmd(command)
            sys.stdout = current
            return a._buff

            if self.__mode == 'SERVER':
                serverThread.stop()
        except  (Exception, KeyboardInterrupt) as e:
            import traceback
            traceback.print_exc()
            print(str(e))
            if self.shell is not None:
                self.shell.finish()
            sys.stdout.flush()
            sys.exit(1)


class RemoteShell(cmd.Cmd):
    def __init__(self, share, rpc, mode, serviceName):
        cmd.Cmd.__init__(self)
        self.__share = share
        self.__mode = mode
        self.__output = '\\\\127.0.0.1\\' + self.__share + '\\' + OUTPUT_FILENAME
        self.__batchFile = '%TEMP%\\' + BATCH_FILENAME
        self.__outputBuffer = b''
        self.__command = ''
        self.__shell = '%COMSPEC% /Q /c '
        self.__serviceName = serviceName
        self.__rpc = rpc
        self.__scmr = rpc.get_dce_rpc()
        try:
            self.__scmr.connect()
        except Exception as e:
            print(str(e))
            sys.exit(1)

        s = rpc.get_smb_connection()

        # We don't wanna deal with timeouts from now on.
        s.setTimeout(100000)
        if mode == 'SERVER':
            myIPaddr = s.getSMBServer().get_socket().getsockname()[0]
            self.__copyBack = 'copy %s \\\\%s\\%s' % (self.__output, myIPaddr, DUMMY_SHARE)

        self.__scmr.bind(scmr.MSRPC_UUID_SCMR)
        resp = scmr.hROpenSCManagerW(self.__scmr)
        self.__scHandle = resp['lpScHandle']
        self.transferClient = rpc
        self.do_cd('')

    def finish(self):
        # Just in case the service is still created
        try:
            self.__scmr = self.__rpc.get_dce_rpc()
            self.__scmr.connect()
            self.__scmr.bind(scmr.MSRPC_UUID_SCMR)
            resp = scmr.hROpenSCManagerW(self.__scmr)
            self.__scHandle = resp['lpScHandle']
            resp = scmr.hROpenServiceW(self.__scmr, self.__scHandle, self.__serviceName)
            service = resp['lpServiceHandle']
            scmr.hRDeleteService(self.__scmr, service)
            scmr.hRControlService(self.__scmr, service, scmr.SERVICE_CONTROL_STOP)
            scmr.hRCloseServiceHandle(self.__scmr, service)
        except scmr.DCERPCException:
            pass

    def do_shell(self, s):
        os.system(s)

    def do_exit(self, s):
        return True

    def emptyline(self):
        return False

    def do_cd(self, s):
        # We just can't CD or maintain track of the target dir.
        if len(s) > 0:
            raise ConnectionError("You can't Cd under smbExec. Use Full paths.")

        self.execute_remote('cd ')
        if len(self.__outputBuffer) > 0:
            # Stripping CR/LF
            self.prompt = self.__outputBuffer.decode().replace('\r\n', '') + '>'
            self.__outputBuffer = b''

    def do_CD(self, s):
        return self.do_cd(s)

    def default(self, line):
        if line != '':
            self.send_data(line)

    def get_output(self):
        def output_callback(data):
            self.__outputBuffer += data

        if self.__mode == 'SHARE':
            self.transferClient.getFile(self.__share, OUTPUT_FILENAME, output_callback)
            self.transferClient.deleteFile(self.__share, OUTPUT_FILENAME)
        else:
            fd = open(SMBSERVER_DIR + '/' + OUTPUT_FILENAME, 'r')
            output_callback(fd.read())
            fd.close()
            os.unlink(SMBSERVER_DIR + '/' + OUTPUT_FILENAME)

    def execute_remote(self, data):
        command = self.__shell + 'echo ' + data + ' ^> ' + self.__output + ' 2^>^&1 > ' + self.__batchFile + ' & ' + \
                  self.__shell + self.__batchFile
        if self.__mode == 'SERVER':
            command += ' & ' + self.__copyBack
        command += ' & ' + 'del ' + self.__batchFile

        resp = scmr.hRCreateServiceW(self.__scmr, self.__scHandle, self.__serviceName, self.__serviceName,
                                     lpBinaryPathName=command, dwStartType=scmr.SERVICE_DEMAND_START)
        service = resp['lpServiceHandle']

        try:
            scmr.hRStartServiceW(self.__scmr, service)
        except Exception as e:
            pass
        scmr.hRDeleteService(self.__scmr, service)
        scmr.hRCloseServiceHandle(self.__scmr, service)
        self.get_output()

    def send_data(self, data):
        self.execute_remote(data)
        try:
            print(self.__outputBuffer.decode('gbk'))
        except UnicodeDecodeError:
            print(self.__outputBuffer.decode('utf-8', errors='replace'))
        self.__outputBuffer = b''


def SmbExec(host, username, password, command):
    executer = CMDEXEC(username, password)
    return executer.run(host, host, command)
