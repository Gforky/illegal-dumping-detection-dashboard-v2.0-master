from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


#SQL schema
class ImageCategory(Base):
    """
    RDMS - table for image categories
    """
    __tablename__ = 'imagecategory'
    category_id = Column(Integer, primary_key = True, autoincrement=True)
    category_name = Column(String(100), nullable = False)

    def __init__(self, category_name):
        self.category_name = category_name


class AlertImage(Base):
    """
    RDMS - table for input image data
    """
    __tablename__ = 'alertimage'
    alert_id = Column(Integer, primary_key = True, autoincrement=True)
    image_name = Column(String(100), nullable=False)
    alert_datetime = Column(DateTime, nullable = False)

    def __init__(self, image_name):
        self.image_name = image_name
        self.alert_datetime = datetime.utcnow()

class ImageConfirmation(Base):
    """
    RDMS - table for classification result
    """

    __tablename__ = 'imageconfirmation'
    confirmation_id = Column(Integer, primary_key = True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("imagecategory.category_id"), nullable=False)
    alert_id = Column(Integer, ForeignKey("alertimage.alert_id"), nullable=False)
    classification_datetime = Column(DateTime, nullable = False)

    def __init__(self, category_id, alert_id):
        self.category_id = category_id
        self.classification_datetime = datetime.utcnow()
        self.alert_id = alert_id


