from flask import Flask
from flask_wtf.csrf import CSRFProtect
from appdir.config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
csrf = CSRFProtect(app)

from appdir import routes, models
from appdir import commands
