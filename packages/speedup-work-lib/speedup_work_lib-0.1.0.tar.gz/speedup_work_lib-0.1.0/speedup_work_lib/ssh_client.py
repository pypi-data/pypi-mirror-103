#!/usr/bin/env python
"""
.. current_module:: ssh_client.py
.. created_by:: Darren Xie
.. created_on:: 06/07/2021

This python script is base script to set up MIS development environment.
"""
import sys
from datetime import datetime
from io import StringIO

import paramiko

TIME_FORMAT = '%H:%M:%S'


class SshClient:
    """A wrapper of paramiko.SSHClient"""
    TIMEOUT = 10

    def __init__(self, host, port, username, password, key=None, passphrase=None):
        self.username = username
        self.password = password
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if key is not None:
            key = paramiko.RSAKey.from_private_key(StringIO(key), password=passphrase)
        try:
            self.client.connect(host, port, username=username, password=password, pkey=key, timeout=self.TIMEOUT)
        except Exception as e:
            raise Exception(f"Cannot connect to the SSH server: {str(e)}")

    def close(self):
        if self.client is not None:
            self.client.close()
            self.client = None

    def execute(self, command, sudo=False, verbose=False):
        if verbose:
            self._print_log(f"Running command: [{command}]")
        feed_password = False
        if sudo and self.username != "root":
            command = "sudo -S -p '' %s" % command
            feed_password = self.password is not None and len(self.password) > 0
        stdin, stdout, stderr = self.client.exec_command(command, timeout=self.TIMEOUT)
        if feed_password:
            stdin.write(self.password + "\n")
            stdin.flush()
        return {'out': stdout.readlines(),
                'err': stderr.readlines(),
                'retval': stdout.channel.recv_exit_status()}

    def _print_log(self, msg=''):
        """print out the log message"""
        sys.stdout.write(f"[{datetime.now().strftime(TIME_FORMAT)}]: {msg}\n")
