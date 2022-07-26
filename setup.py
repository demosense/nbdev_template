from pkg_resources import parse_version
from configparser import ConfigParser
import setuptools
assert parse_version(setuptools.__version__) >= parse_version('36.2')

# note: all settings are in settings.ini; edit there, not here
config = ConfigParser(delimiters=['='])
config.read('settings.ini')
cfg = config['DEFAULT']

cfg_keys = 'version'.split()
expected = cfg_keys + "lib_name min_python".split()
for o in expected:
    assert o in cfg, "missing expected setting: {}".format(o)
setup_cfg = {o: cfg[o] for o in cfg_keys}

requirements = cfg.get('requirements', '')
with open(requirements) as f:
    requirements = f.readlines()

min_python = cfg['min_python']

setuptools.setup(
    name=cfg['lib_name'],
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=requirements,
    dependency_links=cfg.get('dep_links', '').split(),
    python_requires='>=' + cfg['min_python'],
    zip_safe=False,
    entry_points={'console_scripts': cfg.get('console_scripts', '').split()},
    **setup_cfg)
