import os
from flask import Flask
from pathlib import Path
import fcntl

app = Flask(__name__)
Path('/data/count').touch(exist_ok=True)

def write(count):
    with open("/data/count", "w") as g:
        fcntl.flock(g, fcntl.LOCK_EX)
        g.write(str(count))
        fcntl.flock(g, fcntl.LOCK_UN)

def read():
    f = open("/data/count", "r")
    return f.read()

def get_visit_count():
    try:
        visit_count = read()
        if visit_count == "":
            visit_count = 0
        visit_count = int(visit_count) + 1
        write(visit_count)
        return visit_count
    except Exception as e:
        raise e

@app.route('/')
def index():
    visit_count = str(get_visit_count())
    return 'Host name: {}, Visit count: {}.\n'.format(os.uname()[1], visit_count)
