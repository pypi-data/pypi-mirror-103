# YAML Helper

Helper methods to read and write YAML files.

## Installation
`pip install yaml-helper`

## Usage
```
from yaml_helper import YAML


yaml = YAML('config.yml')
config = yaml.load()

print(config['ip_address'])
print(config['port'])

yaml.add({'driver': 'mysqli'})
yaml.add({'username': 'admin'})
yaml.write()
```
