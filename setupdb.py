from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import models
from models import Base, TrainingImageData, UserData, ImageCategories, ClassificationResult, InputImageData

#create category instance in the db
category1 = ImageCategory(category_name='couch')
category2 = ImageCategory(category_name='mattress')
category3 = ImageCategory(category_name='tv-monitor')
category_unknown = ImageCategory(category_name='unknown')
session.add(category1)
session.add(category2)
session.add(category3)


#create employee instance
alert_image1 = AlertImage(userName='Andrew', user_password = 'a',workType='admin')
alert_image2 = AlertImage(userName='Eric', user_password = 'b', workType='operator')
session.add(employee1)
session.add(employee2)

#create confirmation instance
confirmation1 = ImageConfirmation(category_id='1', alert_id='1')
confirmation1 = ImageConfirmation(category_id='2', alert_id='1')
confirmation1 = ImageConfirmation(category_id='3', alert_id='2')

try:
    session.commit()
except SQLAlchemyError as ex:
    print(str(ex))


#   print("add date", employee.createDate)

# for imagecategory in session.query(ImageCategories).all():
#   print("id", imagecategory.category_id)
#   print("category name", imagecategory.category_name)


engine.dispose()