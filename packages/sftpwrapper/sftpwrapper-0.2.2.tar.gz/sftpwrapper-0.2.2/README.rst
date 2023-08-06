sftpwrapper
===========

Overview
--------
A Python library that facilitates uploading and downloading of files to/from an SFTP server using either username/password or username/sshkey.

Install It
----------
From PyPI ::

    $ pip install sftpwrapper

New in v0.2.1
-------------
Defaults to port 22

Logging works with the new version of Paramiko

HostKey and Private Key support for connecting to SFTP server (have to provide the file path and encryption)

Code Example
------------
    from sftpwrapper import SftpWrapper

    remote_connection = SftpWrapper(host, port)
    remote_connection.host_connect(user, password)
    upload_good = remote_connection.upload_stuffs(csv_name, remote + csv_name)
    remote_connection.host_disconnect()

Dependencies
------------
* paramiko

License
--------
MIT