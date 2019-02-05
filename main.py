import os
import tempfile
from xml.dom import minidom

REPO = "https://github.com/EFForg/https-everywhere.git"

current_path = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(current_path, 'https-everywhere')

if os.path.exists(path):
    os.system('git -C ' + path + ' pull ' + REPO)
else:
    os.system('git clone ' + REPO + ' ' + path)

path = os.path.join(path, "src/chrome/content/rules")

files = os.listdir(path)

files.remove('00README')
files.remove('make-trivial-rule')

hosts = set()

for file in files:
    # if not file.endswith('.xml'):
    #     continue
    file = os.path.join(path, file)
    document = minidom.parse(file)
    targets = document.getElementsByTagName('target')

    for target in targets:
        host = target.attributes['host'].value

        if '*' in host:
            continue

        hosts.add(host)

domain_path = os.path.join(current_path, 'domains.txt')
with open(domain_path, 'w') as file:
    file.write('\n'.join(hosts))

print("Output written to", domain_path)
print("Length:", len(hosts))
