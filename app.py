import os
from flask import Flask
import fcntl

app = Flask(__name__)

def write(count):
    with open("/data/count", "w") as g:
        fcntl.flock(g, fcntl.LOCK_EX)
        g.write(new_entry)
        fcntl.flock(g, fcntl.LOCK_UN)

def read():
    f = open("/data/count", "r")
    return f.read()

def get_visit_count():
    try:
        visit_count = read()
        if visit_count is None:
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
