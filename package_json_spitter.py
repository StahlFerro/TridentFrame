import json
from pprint import pprint

with open('package.json', 'r') as file:
    data = json.load(file)
    deps = data['dependencies']
    devdeps = data['devDependencies']
    for key, value in deps.items():
        print(key)
    for key, value in deps.items():
        print(value)
    for key, value in devdeps.items():
        print(key)
    for key, value in devdeps.items():
        print(value)          
