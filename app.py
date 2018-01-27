import os

from flask import Flask

import settings

app = Flask(__name__)
app.config.from_object(settings)

db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=settings.PORT, debug=settings.DEBUG)
