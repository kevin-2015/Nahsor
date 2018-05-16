# -*- coding:utf-8 -*-
__author__ = 'nahsor'
from flask_cors import CORS
from app import create_app
from app.response import products, projects, modules, testcass, reports, index

app = create_app("ProductionConfig")
CORS(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8808, threaded=True)
