
import os
import sys
import json

from datetime import datetime

from . import __version__, __inkscape__

filters = ['.pyc', '.swp', '~', 'package.json']

if '-v' in sys.argv:
    print(__version__)
elif '-p' in sys.argv and sys.argv[-1].endswith('.json'):
    with open('inkman/data/package.json', 'r') as fhl:
        pkg = json.loads(fhl.read())

    pkg["dates"]["edited"] = str(datetime.now())
    pkg["version"] = __version__
    pkg["Inkscape Version"] = __inkscape__

    pkg["files"] = [
        'manage_extensions.inx',
        'manage_extensions.py',
    ]
    for (base, dirs, files) in os.walk('inkman'):
        for filename in files:
            if not any([flt for flt in filters if filename.endswith(flt)]):
                pkg["files"].append(os.path.join(base, filename))

    print(sys.argv[-1])
    for item in pkg["files"]:
        print(item)

    with open(sys.argv[-1], 'w') as fhl:
        fhl.write(json.dumps(pkg, indent=2))
