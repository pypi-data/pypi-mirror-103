import json
import base64 as b64

def listfiles(aseobj):
    with open(aseobj) as f:
        ra = json.load(f)
    outlist = []
    for s in ra['rawfiles']:
        outlist.append(s)
    return outlist
def readfiledata(aseobj, filename):
    with open(aseobj) as f:
        ra = json.load(f)
    return ra['files'][filename]

def expandplaintext(aseobj, dirpath):
    with open(aseobj) as f:
        ra = json.load(f)
    for key in ra['files']:
        open(f'{dirpath}{key}', 'w').write(ra['files'][key])
        
def expandbase64(aseobj, dirpath):
    with open(aseobj) as f:
        ra = json.load(f)
    for key in ra['files']:
        open(f'{dirpath}{key}', 'w').write(b64.b64decode(ra['files'][key].encode()).decode())
    
def load(filename):
    return filename

def readmode(aseobj, dirpath):
    with open(aseobj) as f:
        ra = json.load(f)
    return ra['contentmode']

class ASEWriter:
    def __init__(self, asename):
        self.name = asename
        self.obj = {}
        self.obj['files'] = {}
        self.obj['rawfiles'] = []
        
    def setmode(self, mode):
        self.obj['contentmode'] = mode

    def addfile(self, filename):
        self.obj['rawfiles'].append(filename)

    def readstate(self):
        return self.obj

    def setfiledata(self, filename, data):
        self.obj['files'][filename] = data

    def readfile(self, filename):
        try:
            if self.obj['contentmode'] == 'base64':
                trk = open(filename)
                b64o = b64.b64encode(trk.read().encode()).decode()
                return b64o
            elif self.obj['contentmode'] == 'plaintext':
                trk = open(filename).read()
                return trk
        except:
            print('Please set a content mode first with instance.setmode()')
            return False

    def write(self):
        open(self.name, 'w').write(json.dumps(self.obj))
        

    
        

