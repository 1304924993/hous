
from flask import Flask
from flask_script import Manager

from app.hous_views import hous
from app.models import db
from app.order_viewa import order
from app.user_views import user
from utils.setting import STATIC_PATH, TEMPLATE_PATH


app = Flask(__name__,static_folder=STATIC_PATH, template_folder=TEMPLATE_PATH)

app.register_blueprint(blueprint=user, url_prefix='/user')
app.register_blueprint(blueprint=hous, url_prefix='/hous')
app.register_blueprint(blueprint=order, url_prefix='/order')

app.secret_key = 'mashdihalsjaks'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/hous8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


manage = Manager(app)


if __name__ == '__main__':
    manage.run()






