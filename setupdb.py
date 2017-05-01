from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import models
from models import Base, ImageCategory, ImageConfirmation

#testing postgresql with sqlalchemy - test ok
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
# <<<<<<< Updated upstream
# engine = create_engine('postgresql://localhost:5432/cmpe295')
# ||||||| merged common ancestors
# engine = create_engine('postgresql:///illegaldumpingdb')
# =======
engine = create_engine('postgresql://localhost:5433/cmpe295')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

#create category instance in the db
category1 = ImageCategory(category_name='couch')
category2 = ImageCategory(category_name='mattress')
category3 = ImageCategory(category_name='tv-monitor')
category_unknown = ImageCategory(category_name='unknown')
session.add(category1)
session.add(category2)
session.add(category3)
session.commit()

# #create alert  instance
# alert_image1 = AlertImage(image_name='car1')
# alert_image2 = AlertImage(image_name='car2')
# session.add(alert_image1)
# session.add(alert_image2)
# session.commit()

#create confirmation instance
confirmation1 = ImageConfirmation(category_id='1', image_path='mattress3.jpg')
confirmation2 = ImageConfirmation(category_id='2', image_path='mattress4.jpg')
confirmation3 = ImageConfirmation(category_id='3', image_path='mattress5.jpg')
session.add(confirmation1)
session.add(confirmation2)
session.add(confirmation3)
session.commit()


engine.dispose()
