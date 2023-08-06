import asyncio
from polypuppet import Config
from polypuppet.messages import info


class CertList:
    def __init__(self):
        config = Config()
        self.certlist = []
        self.timeout = int(config['CERT_WAITTIME'])

    async def _certname_stopwatch(self, certname):
        await asyncio.sleep(self.timeout)
        info.stop_waiting_for_cert(certname)
        self.remove(certname)

    def remove(self, certname):
        if certname in self.certlist:
            self.certlist.remove(certname)

    def append(self, certname):
        self.certlist.append(certname)
        info.wait_for_cert(certname)
        asyncio.ensure_future(self._certname_stopwatch(certname))

    def check_and_remove(self, certname):
        has_certname = certname in self.certlist
        self.remove(certname)
        info.request_for_cert(certname, has_certname)
        return has_certname

    def __contains__(self, certname):
        return certname in self.certlist
