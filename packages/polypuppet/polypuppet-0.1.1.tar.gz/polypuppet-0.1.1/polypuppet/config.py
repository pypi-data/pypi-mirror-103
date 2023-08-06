import configparser
from polypuppet.definitions import CONFIG_PATH
from polypuppet.messages import error


class Config:
    def __getitem__(self, value):
        value = str(value).lower()
        return self.flat[value]

    def __setitem__(self, key, value):
        for k in self.config:
            if key in self.config[k]:
                self.flat[key] = value
                self.config[k][key] = value

        try:
            CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
            CONFIG_PATH.touch(exist_ok=True)
            with open(CONFIG_PATH, 'w') as configfile:
                self.config.write(configfile)
        except:
            error.cannot_create_config_file()

    def __contains__(self, key):
        return key in self.flat

    def load(self):
        default_config = configparser.ConfigParser()
        default_config['server'] = {
            'SERVER_DOMAIN': 'server.poly.puppet.com',
            'SERVER_CERTNAME': 'server.poly.puppet.com',
            'SERVER_PORT': 8668}
        default_config['agent'] = {
            'CONTROL_PORT': 8668,
            'CERT_WAITTIME': 90,
            'ENABLE': False}
        default_config['profile'] = {
            'AUDIENCE': '',
            'STUDENT_FLOW': '',
            'STUDENT_GROUP': ''}
        default_config['cache'] = {
            'SSLDIR': '/etc/puppetlabs/puppet/ssl'}

        if not CONFIG_PATH.exists():
            self.config = default_config
        else:
            self.config = configparser.ConfigParser()
            self.config.read(CONFIG_PATH)

        self.flat = {}
        for key in self.config:
            self.flat.update(self.config[key])

    def all(self):
        return self.flat

    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.load()
        return cls._instance
