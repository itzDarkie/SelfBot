import paramiko

class ssh():
    def __init__(self, ip, username, password, port):
        self.ip = ip
        self.username = username
        self.password = password
        self.port = int(port)
        self.isconnect = False

    def connectto(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(self.ip, username=self.username, password=self.password, port=self.port)
            self.isconnect = True
            self.ssh = ssh
            return "Connected!"
        except:
            return "was not Connected!"
    
    def cmd(self, tcmd):
        if self.isconnect == True:
            (stdin, stdout, stderr) = self.ssh.exec_command(tcmd)
            return stdin, stdout , stderr
        else:
            return False

    def disconnect(self):
        self.ssh.close()
        self.isconnect = False
        return "Disconnected!"

