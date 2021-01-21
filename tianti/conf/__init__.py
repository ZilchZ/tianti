import os
import sys
import ConfigParser
from oslo_config import cfg as oslo_cfg
from oslo_log import log

PORT_CLI_OPTS = [
    oslo_cfg.IntOpt(
        "port",
        default=8080,
        help = "server port."
    ),
]


def init(args, **kwargs):
    log.register_options(oslo_cfg.CONF)
    oslo_cfg.CONF.register_cli_opts(PORT_CLI_OPTS)
    oslo_cfg.CONF(args=args, **kwargs)


def setup_logging():
    product_name = "server"
    log.setup(oslo_cfg.CONF, product_name)


class Configure(object):
    config_dict = {}
    last_modify_time = None

    def __init__(self):
        if len(oslo_cfg.CONF.config_file) >= 1:
            config_path = oslo_cfg.CONF.config_file[0]
        else:
            config_path = "../../etc/tianti_dev.ini"
            if not os.path.exists(config_path):
                raise Exception("could not find config file")

        config = ConfigParser.RawConfigParser()
        config.readfp(open(config_path, "r"))
        self.config = config
        self.config_path = config_path
        Configure.last_modify_time = os.stat(config_path).st_mtime

    def get_config(self, alias):
        return dict(item for item in self.config.items(alias))

    def reload(self):
        Configure.last_modify_time = os.stat(self.config_path).st_mtime


init(sys.argv[1:])
cfg = Configure()
setup_logging()


if __name__ == '__main__':
    print cfg.get_config("postgres")
    print cfg.get_config("DEFAULT").get("debug")
    from oslo_config import cfg as oslo_cfg
    print oslo_cfg.CONF.port