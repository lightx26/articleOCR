import yaml
from vietocr.tool.config import Cfg


def load_config_from_file(base, fname):

    with open(base, encoding='utf-8') as f1:
        base_config = yaml.safe_load(f1)
    with open(fname, encoding='utf-8') as f2:
        config = yaml.safe_load(f2)

    base_config.update(config)
    return Cfg(base_config)
