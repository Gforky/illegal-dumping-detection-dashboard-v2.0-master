from flask import Flask
from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import models
from models import Base, ImageData, UserData, ImageCategories, UnIdentifiedImage
from werkzeug import secure_filename
from flask import json
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'imgFolders/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_FILE_EXTENSIONS = set(['tar', 'zip'])

#web services API
@app.route("/")
def hello():
    return "Hello World!"

@app.route("/index")
def index():
	return render_template('index.html')

@app.route("/upload-files", methods=['GET', 'POST'])
def uploadfile():
	if request.method == 'POST':
		imgFile = request.files['file']
		if imgFile and allowed_file_type(imgFile.filename):
			filename = secure_filename(imgFile.filename)
			imgFile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return ''
	return 'not successfully upload'

"""
This is an API for getting image stats
Usage: return json arr [category_1 count, category_2 count, category_3 count, total count]
"""
@app.route("/getImageStats", methods=['POST'])
def getImageStats():
    if request.method == 'POST':
        imagedata_stats_arr = []
        counter, counter1, counter2, counter3 = 0, 0, 0, 0
        getTotalSQL = engine.execute("select * from imagedata;")
        for data in session.query(ImageData.category_id == 1).all():
            counter1 += 1
        imagedata_stats_arr.append(counter1)
        for data in session.query(ImageData.category_id == 2).all():
            counter2 += 1
        imagedata_stats_arr.append(counter2)
        for data in session.query(ImageData.category_id == 3).all():
            counter3 += 1

        imagedata_stats_arr.append(counter3)
        counter = counter1 + counter2 + counter3
        imagedata_stats_arr.append(counter)

        json_str = json.dumps(imagedata_stats_arr)
        return json_str

#helper function
def allowed_file_type(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_FILE_EXTENSIONS

#testing postgresql with sqlalchemy - test ok
db = SQLAlchemy(app)
engine = create_engine('postgresql://localhost/cmpe295')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

#create category instance in the db
category1 = ImageCategories(category_name='couch')
category2 = ImageCategories(category_name='mattress')
category3 = ImageCategories(category_name='tv-monitor')
session.add(category1)
session.add(category2)
session.add(category3)

# create image instance
image1 = ImageData(category_id='1', path='abc/ccc', preProcessed = True)
image2 = ImageData(category_id='2', path='abc/bbb', preProcessed = False)
session.add(image1)
session.add(image2)

#create employee instance
employee1 = UserData(userName='Andrew', user_password = 'a',workType='admin')
employee2 = UserData(userName='Eric', user_password = 'b', workType='operator')
session.add(employee1)
session.add(employee2)

#creaet unidentified image
unidentified1 = UnIdentifiedImage(category_id='1', path='aaa/ccc')
unidentified2 = UnIdentifiedImage(category_id='2', path='bbb/aaa')
session.add(unidentified1)
session.add(unidentified2)

# try:
# 	session.commit()
# except SQLAlchemyError as ex:
# 	session.rollback()
# 	print(str(ex))


# for image in session.query(ImageData).all():
# 	print("id", image.image_id)
# 	print("path", image.path)
# 	print("preprocessed", image.preProcessed)
# 	print("add date", image.createDate)
# 	print("preprcessed date", image.preprocessedDate)
# 	print("trained date", image.trainedDate)
#
# for employee in session.query(UserData).all():
# 	print("id", employee.user_id)
# 	print("name", employee.userName)
# 	print("preprocessed", employee.workType)
# 	print("add date", employee.createDate)
#
# for imagecategory in session.query(ImageCategories).all():
# 	print("id", imagecategory.category_id)
# 	print("category name", imagecategory.category_name)
#
# for unidentified in session.query(UnIdentifiedImage).all():
# 	print("id", unidentified.unidentified_id)
# 	print("unidentified category id", unidentified.category_id)
# 	print("unidentified path", unidentified.path)
# 	print("unidentified create date", unidentified.createDate)
#
# engine.dispose()

if __name__ == "__main__":
	app.run(debug=True)
