import logging as log
import os
from datetime import datetime

import paramiko


class SftpWrapper:
    def __init__(self, host, port=22, logging=False):
        """
        :param host: Host IP address
        :param port: Host port for SFTP communication
        :param logging: Pass True parameter here to enable logging
        """
        self.host = host
        self.port = port
        self.sftp = None
        self.transport = None
        self.hkey = None
        self.pkey = None
        self.log_file = None

        if logging:
            logging_dir = "./logging"
            if not os.path.isdir(logging_dir):
                os.mkdir(logging_dir)

            self.log_file = os.path.join(logging_dir, datetime.now().strftime('paramiko%Y%m%d_%H%M%S.log'))
            log.basicConfig(filename=self.log_file)

    def host_connect(self, username, password=None, hostkey: str = None, hostkey_type: str = None, pkey: str = None,
                     pkey_type=None):
        """
        Creates an SFTP connection paramiko.SFTPClient in sftp property.
        :param username: the username to authenticate as.
        :param password: the username to authenticate as.
        :param hostkey: the host key file path, or None if you don’t want to do key verification.
        :param hostkey_type: the type of encryption used for the host key
        :param pkey: the private key file path, or None if you don’t want to do key verification.
        :param pkey_type: the type of encryption used for the private key
        """
        self.transport = paramiko.Transport((self.host, self.port))
        if self.log_file:
            log.getLogger(self.transport.get_log_channel())
        if hostkey:
            self.hkey = self._get_key(hostkey, hostkey_type)
        if pkey:
            self.pkey = self._get_key(pkey, pkey_type)

        self.transport.connect(username=username, password=password, hostkey=self.hkey, pkey=self.pkey)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

    def _get_key(self, key: str, key_type: str, password: str = None) -> paramiko.PKey:
        enc_types = {'rsa', 'dss', 'ecdsa', 'ed25519'}
        key_type = key_type.lower() if key_type else None
        if key_type and key_type.lower() not in enc_types:
            raise ValueError(f"key must be one of {enc_types}")
        if key and not os.path.isfile(key):
            raise FileNotFoundError(f"{key} not found")
        if bool(key) ^ bool(key_type):
            raise ValueError(f"key and key_type must be provided.")
        if key_type == 'rsa':
            return paramiko.RSAKey.from_private_key_file(key, password)
        if key_type == 'dss':
            return paramiko.DSSKey.from_private_key_file(key, password)
        if key_type == 'ecdsa':
            return paramiko.ECDSAKey.from_private_key_file(key, password)
        if key_type == 'ed25519':
            return paramiko.Ed25519Key.from_private_key_file(key, password)

    def upload_stuffs(self, local_path, remote_path):
        """
        Upload file to remote machine.
        :param local_path: This is the path for the file on your LOCAL machine, where python is called from
        :param remote_path: This is the path for the file on your REMOTE machine, will default to PWD
        :return: Returns paramiko.sftp_attr.SFTPAttributes object
        """
        try:
            return self.sftp.put(local_path, remote_path)
        except:
            return None

    def download_stuffs(self, local_path, remote_path):
        """
        Download file from remote machine.
        :param local_path: This is the path for the file on your LOCAL machine, where python is called from
        :param remote_path: This is the path for the file on your REMOTE machine, will default to PWD
        """
        self.sftp.get(remote_path, local_path)

    def delete_stuffs(self, remote_path: str):
        """
        Delete file from remote machine.
        :param remote_path: This is the path for the file on your REMOTE machine, will default to PWD
        """
        self.sftp.remove(remote_path)

    def list_stuffs(self, remote_path: str = '.'):
        """
        List contents of the remote path.
        :param remote_path: This is the path for the file on your REMOTE machine, will default to PWD
        :return: list containing the names of entries in a given path
        """
        return self.sftp.listdir(remote_path)

    def change_directory(self, path: str = None):
        """
        Navigate to a different path on the remote machine.
        :param path: This is the path on your REMOTE machine, will default to None
        """
        self.sftp.chdir(path=path)

    def host_disconnect(self):
        self.transport.close()
        self.sftp.close()
