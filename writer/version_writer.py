import json
import platform
from pprint import pprint

package_json = {}
targets = []
with open("../package.json") as jsonfile:
    package_json = json.load(jsonfile)

build_info = package_json['build']

if platform.system() == 'Windows':
    targets.extend(build_info['win']['target'])
    
elif platform.system() == 'Linux':
    targets.extend(build_info['linux']['target'])

print('targets', targets)
