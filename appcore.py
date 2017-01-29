from flask import Flask
from modules.neutron import neutron

app = Flask(__name__)


app.register_blueprint(neutron, url_prefix='/neutron')


if __name__ == '__main__':
    app.run()
