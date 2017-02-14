from __future__ import print_function
import sys
import threading
import re
import socket
import paramiko

# windows does not have termios...
try:
    import termios
    import tty
    has_termios = True
    import select
except ImportError:
    has_termios = False


class ShellHandler(object):
    # https://stackoverflow.com/questions/35821184/implement-an-interactive-shell-over-ssh-in-python-using-paramiko

    def __init__(self, host, username, password):
        self.ssh = paramiko.SSHClient()
        
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(host,
                         username=username,
                         password=password)

        self.channel = channel = self.ssh.invoke_shell()
        self.interactive_shell(channel)

    def __del__(self):
        self.ssh.close()

    def interactive_shell(self, chan):
        if has_termios:
            self.posix_shell(chan)
        else:
            self.windows_shell(chan)

    def windows_shell(self, chan):
        # https://github.com/paramiko/paramiko/blob/master/demos/interactive.py
        sys.stdout.write("Line-buffered terminal emulation. Press F6 or ^Z to send EOF.\r\n\r\n")
        command = ""
        
        def write_all(sock):
            # get rid of 'coloring and formatting' special characters
            formatting = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]')
            
            while True:
                data = sock.recv(9999)
                if not data:
                    sys.stdout.write('\r\n*** EOF ***\r\n\r\n')
                    sys.stdout.flush()
                    break
                
                # don't print the command we just typed in
                output = formatting.sub("", data)
                if output.lstrip().startswith(command):
                    output = output[len(command):]

                sys.stdout.write(output)  
                sys.stdout.flush()
        
        writer = threading.Thread(target=write_all, args=(chan,))
        writer.start()

        if __name__ == "__main__":
            try:
                while True:
                    command = raw_input("").strip()  # sys.stdin.read(1)
                    #if not command:
                        #break
                    self.execute(command)
            except (EOFError, socket.error):
                # user hit ^Z or F6, or exited the SSH session
                pass

    def execute(self, command):
        try:
            self.channel.send(command)
            self.channel.send("\r")
        except (EOFError, socket.error):
            # user hit ^Z or F6, or exited the SSH session
            pass

    def posix_shell(self, chan):
        oldtty = termios.tcgetattr(sys.stdin)
        try:
            tty.setraw(sys.stdin.fileno())
            tty.setcbreak(sys.stdin.fileno())
            chan.settimeout(0.0)

            while True:
                r, w, e = select.select([chan, sys.stdin], [], [])
                if chan in r:
                    try:
                        x = u(chan.recv(1024))
                        if len(x) == 0:
                            sys.stdout.write('\r\n*** EOF\r\n')
                            break
                        sys.stdout.write(x)
                        sys.stdout.flush()
                    except socket.timeout:
                        pass
                if sys.stdin in r:
                    x = sys.stdin.read(1)
                    if len(x) == 0:
                        break
                    chan.send(x)

        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)

# # # #


def main(env, usr, pwd):
    shell = ShellHandler(env,
                         username=usr,
                         password=pwd)

# # # #


if __name__ == "__main__":
    import getpass
    
    username = raw_input("Username: ")
    password = getpass.getpass("Password: ")

    main("epic-cde", username, password) #, commands)
