#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import time
import paramiko


class BaseSshClient(object):
    p_sys = re.compile(r"<(?P<sysname>\S+)>")

    def __init__(self, host, user, password, port=22, timeout=10):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.timeout = timeout
        self.ssh = None
        self.sysname = None

    def __enter__(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
        self.ssh.connect(
            hostname=self.host,
            username=self.user,
            password=self.password,
            look_for_keys=False,
            timeout=self.timeout
        )
        self.chan = self.ssh.invoke_shell(width=800, height=600)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.ssh is not None:
            self.ssh.close()

    def get_sysname(self):
        if self.sysname is None:
            status, res = self.send_line("")
            if status == "end":
                m = self.p_sys.match(res[-1].strip())
                if m:
                    self.sysname = m.group("sysname")

    def _end_type(self, end_line):
        status = None
        if end_line.startswith("<") and end_line.endswith(">"):
            status = "end"
        elif end_line.startswith("[") and end_line.endswith("]"):
            status = "write"
        elif end_line.endswith(("[Y/N];", "[Y/N]")):
            status = "ask"
        elif end_line.find("---- More ----") != -1:
            status = "read"
        return status

    def _chan_send(self, cmd):
        self.chan.send(cmd)

    def _chan_revc(self):
        ret = self.chan.recv(10240)
        return ret

    def send_line(self, cmd, timeout=None):
        cmd += "\n"
        return self.send(cmd, timeout)

    def send(self, cmd, timeout=None):
        status = None
        results = []
        if timeout is None:
            timeout = self.timeout
        self.chan.settimeout(timeout)
        self._chan_send(cmd)
        send_end_flag = False
        end_line = ""
        while True:
            time.sleep(0.1)
            data = self._chan_revc()
            unit_data = end_line + data
            data_lines = unit_data.split("\r\n")
            results.extend(data_lines[:-1])
            end_line = data_lines[-1]
            status = self._end_type(end_line.strip())
            if status == "read":
                self._chan_send("\n")
                continue
            elif status in ("end", "write",) and send_end_flag is False:
                self._chan_send("\n")
                send_end_flag = True
                continue
            elif status is not None:
                results.append(end_line)
                break
        return status, results

    def answer_chan_start_ask(self):
        """
        和网络设备建立伪终端进行通信时，有时会提示需要修改密码，回复后才能进行命令的交互，默认不修改。
        :return:
        """
        status, results = self.send_line("")
        if status == "ask":
            status , res =self.send_line("N")
            results.extend(res)
        return status, results


if __name__ == '__main__':
    with BaseSshClient("126.0.0.1", "admin", "123456") as c:
        c.answer_chan_start_ask()
        sysname = c.get_sysname()
        _, lines = c.send_line("display nqa results")
    print c.sysname
    print lines

