from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

#from app.models import db
#from dotenv import load_dotenv
#from flask import Flask
#load_dotenv()



app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://barro:BARROBA@localhost/dbproject'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.init_app(app)



def create_app():
    from app.scheduler import start_scheduler
    from app import db
    app = Flask(__name__)
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        start_scheduler()
    
    return app


from app import routes, models