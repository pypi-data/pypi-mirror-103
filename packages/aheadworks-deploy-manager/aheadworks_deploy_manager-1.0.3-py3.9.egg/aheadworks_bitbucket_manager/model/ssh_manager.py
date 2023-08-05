import subprocess


class SshManager:

    def run_ssh_command(self, command, host, user):
        host = user + '@' + host
        ssh = subprocess.Popen(["ssh", "%s" % host, command],
                               shell=False,
                               encoding="utf-8",
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        return ssh.stdout.readlines()
