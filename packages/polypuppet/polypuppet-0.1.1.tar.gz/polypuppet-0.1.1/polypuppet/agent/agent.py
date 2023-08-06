import asyncio
import multiprocessing as mp
import os
import socket
import ssl

from polypuppet import proto
from polypuppet.definitions import EOF_SIGN
from polypuppet.server import server
from polypuppet.config import Config
from polypuppet.puppet import Puppet
from polypuppet.messages import error


class Agent:
    def __init__(self):
        self._config = Config()

    async def _connect(self, ip, port, message):
        ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.VerifyMode.CERT_NONE

        try:
            sock = socket.create_connection((ip, port))
        except Exception as e:
            error.agent_cannot_connect_server(ip, port)

        wrapper = ssl_context.wrap_socket(sock)
        reader, writer = await asyncio.open_connection(sock=wrapper)
        writer.write(message.SerializeToString())
        writer.write(EOF_SIGN)
        await writer.drain()

        raw_message = await reader.readuntil(EOF_SIGN)
        raw_message = raw_message[:-len(EOF_SIGN)]
        writer.close()
        await writer.wait_closed()

        response = proto.Message()
        response.ParseFromString(raw_message)
        return response

    def connect_lan(self, message):
        ip = 'localhost'
        port = self._config['CONTROL_PORT']
        return asyncio.run(self._connect(ip, port, message))

    def connect_wan(self, message):
        ip = self._config['SERVER_DOMAIN']
        port = self._config['SERVER_PORT']
        return asyncio.run(self._connect(ip, port, message))

    def autosign(self, certname):
        message = proto.Message()
        message.type = proto.AUTOSIGN
        message.certname = certname
        response = self.connect_lan(message)
        return response.ok

    def login(self, username, password):
        message = proto.Message()
        message.type = proto.LOGIN
        message.username = username
        message.password = password
        response = self.connect_wan(message)
        if response.ok:
            puppet = Puppet()
            puppet.certname(response.certname)
            puppet.sync(noop=True)
        return response.ok

    def stop_server(self):
        message = proto.Message()
        message.type = proto.STOP
        self.connect_lan(message)
