import asyncio
import pathlib
import socket
import ssl

from polypuppet import proto
from polypuppet import Config
from polypuppet import PuppetServer, Puppet
from polypuppet.definitions import POLYPUPPET_PEM_NAME, EOF_SIGN
from polypuppet.messages import info, error
from polypuppet.server.person import PersonType
from polypuppet.server.cert_list import CertList
from polypuppet.server.authentication import authenticate


class Server:
    def __init__(self):
        self.config = Config()
        self.puppet = Puppet()
        self.puppetserver = PuppetServer()
        self.certlist = CertList()

    async def _read_message(self, reader):
        raw_message = await reader.readuntil(EOF_SIGN)
        raw_message = raw_message[:-len(EOF_SIGN)]
        message = proto.Message()
        message.ParseFromString(raw_message)
        return message

    async def _answer(self, writer, response):
        writer.write(response.SerializeToString())
        writer.write(EOF_SIGN)
        await writer.drain()

    async def agent_message_handler(self, reader, writer):
        message = await self._read_message(reader)
        response = proto.Message()
        response.type = proto.RESPONSE

        if message.type == proto.LOGIN:
            certname = await self.login(message.username, message.password)
            if certname is not None:
                response.certname = certname
                response.ok = True
        await self._answer(writer, response)

    async def control_message_handler(self, reader, writer):
        message = await self._read_message(reader)
        response = proto.Message()
        response.type = proto.RESPONSE

        if message.type == proto.AUTOSIGN:
            response.ok = self.certlist.check_and_remove(message.certname)
        elif message.type == proto.STOP:
            await self.stop()
        await self._answer(writer, response)

    async def login(self, username, password):
        person = authenticate(username, password)
        if not person.valid():
            return
        certname = ''
        if person.type == PersonType.STUDENT:
            certname += 'student.'
            certname += person.group.replace('/', '.') + '.'
        certname += username.split('@')[0]
        self.puppetserver.clear_certname(certname)
        self.certlist.append(certname)
        return certname

    def get_ssl_context(self):
        ssldir = pathlib.Path(self.config['SSLDIR'])
        ssl_cert = ssldir / ('certs/' + POLYPUPPET_PEM_NAME + '.pem')
        ssl_private = ssldir / ('private_keys/' + POLYPUPPET_PEM_NAME + '.pem')
        if not ssl_cert.exists() or not ssl_private.exists():
            error.must_call_setup_server()

        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        ssl_context.load_cert_chain(ssl_cert, ssl_private)
        return ssl_context

    async def _create_ssl_connection(self, ip, port, handler):
        ssl_context = self.get_ssl_context()
        try:
            sock = socket.create_server((ip, port))
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

        except Exception as e:
            error.server_cannot_bind(ip, port, e)
        wrapper = ssl_context.wrap_socket(sock, server_side=True)
        return await asyncio.start_server(handler, sock=wrapper)

    async def run(self):
        server_ip = self.config['SERVER_DOMAIN']
        server_port = int(self.config['SERVER_PORT'])
        control_ip = 'localhost'
        control_port = int(self.config['CONTROL_PORT'])

        self.agent_connection = await self._create_ssl_connection(
            server_ip, server_port, self.agent_message_handler)
        self.control_connection = await self._create_ssl_connection(
            control_ip, control_port, self.control_message_handler)

        await asyncio.wait([self.agent_connection.serve_forever(), self.control_connection.serve_forever()])
        info.server_stopped()

    async def stop(self):
        self.agent_connection.close()
        self.control_connection.close()
        await asyncio.gather(self.agent_connection.wait_closed(), self.control_connection.wait_closed())


def main():
    server = Server()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
