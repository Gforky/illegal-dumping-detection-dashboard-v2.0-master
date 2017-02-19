from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
# from app import Base
Base = declarative_base()
engine = create_engine('postgresql://localhost/cmpe295')

#SQL schema
class ImageCategories(Base):
	"""
	RDMS - table for image categories
	"""
	__tablename__ = 'imagecategory'
	category_id = Column(Integer, primary_key = True, autoincrement=True)
	category_name = Column(String(100), nullable = False)

	def __init__(self, category_name):
		self.category_name = category_name

class ImageData(Base):
	"""
	RDMS - table for image meta data
	"""
	__tablename__ = 'imagedata'
	image_id = Column(Integer, primary_key = True)
	category_id = Column(Integer, ForeignKey("imagecategory.category_id"), nullable=False)
	path = Column(String(100), nullable = False)
	preProcessed = Column(Boolean, nullable = False)
	createDate = Column(DateTime, nullable = False)
	preprocessedDate = Column(DateTime, nullable = True, default = None)
	trainedDate = Column(DateTime, nullable = True, default = None)

	def __init__(self, category_id, path, preProcessed):
		self.category_id = category_id
		self.path = path
		self.preProcessed = preProcessed
		self.createDate = datetime.utcnow()
		if self.preProcessed == True:
			self.preprocessedDate = datetime.utcnow()

class UnIdentifiedImage(Base):
	"""
	RDMS - table for unIdentified image
	"""
	__tablename__ = 'unidentified'
	unidentified_id = Column(Integer, primary_key = True)
	category_id = Column(Integer, ForeignKey("imagecategory.category_id"), nullable=False)
	path = Column(String(100), nullable = False)
	createDate = Column(DateTime, nullable = False)
	def __init__(self, category_id, path):
		self.category_id = category_id
		self.path = path
		self.createDate = datetime.utcnow()


class UserData(Base):
	"""
	RDMS - table for user data
	"""

	__tablename__ = 'userdata'
	user_id = Column(Integer, primary_key = True)
	userName = Column(String(100), nullable = False)
	user_password = Column(String(50), nullable = False)
	workType = Column(String(50), nullable = False)
	createDate = Column(DateTime)

	def __init__(self, userName, user_password, workType):
		self.userName = userName
		self.user_password = user_password
		self.workType = workType
		self.createDate = datetime.utcnow()
