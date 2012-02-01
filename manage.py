#!/usr/bin/env python

from flask import Flask
from flaskext.actions import Manager
import settings
from bokbok import app

app.config.from_object(settings)
manager = Manager(app)

if __name__ == '__main__':
    manager.run()
