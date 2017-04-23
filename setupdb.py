from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import models
from models import Base, TrainingImageData, UserData, ImageCategories, ClassificationResult, InputImageData

#testing postgresql with sqlalchemy - test ok
app = Flask(__name__)
db = SQLAlchemy(app)
engine = create_engine('postgresql:///illegaldumpingdb')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# #create category instance in the db
category1 = ImageCategories(category_name='couch')
category2 = ImageCategories(category_name='mattress')
category3 = ImageCategories(category_name='tv-monitor')
category_unknown = ImageCategories(category_name='unknown')
session.add(category1)
session.add(category2)
session.add(category3)

# create image instance
image1 = TrainingImageData(category_id='1', path='abc/ccc')
image2 = TrainingImageData(category_id='2', path='abc/bbb')
session.add(image1)
session.add(image2)

#create employee instance
employee1 = UserData(userName='Andrew', user_password = 'a',workType='admin')
employee2 = UserData(userName='Eric', user_password = 'b', workType='operator')
session.add(employee1)
session.add(employee2)

#create image input
imageinput1 = InputImageData(session_id='1', path='abc/a')
imageinput2 = InputImageData(session_id='2', path='abc/a')
session.add(imageinput1)
session.add(imageinput2)

#create classification result
classification1 = ClassificationResult(inputimage_id = '1', category_id='1', batch_id='1')
classification2 = ClassificationResult(inputimage_id = '2', category_id='2', batch_id='1')
session.add(classification1)
session.add(classification2)


try:
    session.commit()
except SQLAlchemyError as ex:
    print(str(ex))


engine.dispose()


# for image in session.query(ImageData).all():
#   print("id", image.image_id)
#   print("path", image.path)
#   print("preprocessed", image.preProcessed)
#   print("add date", image.createDate)
#   print("preprcessed date", image.preprocessedDate)
#   print("trained date", image.trainedDate)

# for employee in session.query(UserData).all():
#   print("id", employee.user_id)
#   print("name", employee.userName)
#   print("preprocessed", employee.workType)
#   print("add date", employee.createDate)

# for imagecategory in session.query(ImageCategories).all():
#   print("id", imagecategory.category_id)
#   print("category name", imagecategory.category_name)

# for unidentified in session.query(UnIdentifiedImage).all():
#   print("id", unidentified.unidentified_id)
#   print("unidentified category id", unidentified.category_id)
#   print("unidentified path", unidentified.path)
#   print("unidentified create date", unidentified.createDate)

engine.dispose()