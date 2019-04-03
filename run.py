#!/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import Flask
import time
app = Flask(__name__)

@app.route('/cast/<n>')
def cast(n):
    time.sleep(int(n))
    print('cast', time.ctime())
    return 'ok'

@app.route('/other_cast/<n>')
def other_cast(n):
    time.sleep(int(n))
    print('cast', time.ctime())
    return 'other_ok'

if __name__ == '__main__':
    app.run()
