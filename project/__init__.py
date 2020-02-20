from flask import Flask

app = Flask(__name__)

app.secret_key = 'abc'

import project.com.controller
