# awdflag

## 目前实现的功能

- 支持 Windows/Linux下发 flag
- Flag传输类型
    - 文件类型
    - mysql

    - sqlserver

    - oracle

    - 可以带密码zip压缩文件
- Windows
    - 命令执行方式
        - SMB 执行
        - WMI 执行
        - WinRm 执行
- Linux
- 命令执行方式
    - paramiko



### 压缩文件

```
src_path = '/tmp/flag.txt'
zip_path = '/tmp/flag.txt.zip'
awdflag.zipEnc(src_path=src_path,dst_path=zip_path,passwd='zippassword',nopass=False)
```



### Windows 传输代码

```
host = i['ip']
src_code = i['name']
src_path = '/tmp/privilege.txt'
dst_path = 'C:/Users/Administrator/flag.txt'
AWD.winFile(host, username, password, src_path, dst_path, src_code, i['type'])
```



### Linux 传输代码

```
host = i['ip']
src_code = i['name']
src_path = '/tmp/privilege.txt'
dst_path = '/root/flag.txt'
AWD.linuxFile(host, port, username, password, src_path, dst_path, src_code, i['type'])
```



## 建议系统

- Window server 2008 r2 sp1 及以上 

-  或者 Window 安装 **WPF5.1**及以上版本的主机
- Linux支持 SFTP, 安装了 openssh-server 即可


### 具体样例请参考 

[Linux 传输模板](examples/linux_examples.py)  &&  [windows 传输模板](examples/win_examples.py)

