from flask import Flask
from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import models
from models import Base, ImageCategory, ImageConfirmation, AlertImage
from werkzeug import secure_filename
from flask import json
import os
from sqlalchemy.sql import select

app = Flask(__name__)
UPLOAD_FOLDER = 'tempFolders/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
ALLOWED_FILE_EXTENSIONS = set(['tar', 'zip'])

#connect db
db = SQLAlchemy(app)
engine = create_engine('postgresql://localhost:5433/cmpe295')
Base.metadata.create_all(engine)
#new
conn = engine.connect()

Session = sessionmaker(bind=engine)
session = Session()
#web services API
@app.route("/")
def hello():
    return "Hello cmpe295 group!"

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
			return 'sucessfully upload'
	return 'not successfully upload'


@app.route("/getTrainingImageStats", methods=['POST'])
def getImageStats():
    """
    This is function for API of getting image stats

    Returns: json arr [category_1 count, category_2 count, category_3 count, total count]

    ---
    TODO: can use bar chart to show the result
    """
    if request.method == 'POST':
        imagedata_stats_arr = []
        counter, counter1, counter2, counter3 = 0, 0, 0, 0
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

#########################   Image Confirmation  #########################
@app.route("/imgConfirmation", methods=['POST'])
def imgConfirmation():
    '''
    Function to move the images from tempory folder to the new dataset folder
    '''
    try:
        imgInfo = request.get_json()
        print("Current Image Source is " + imgInfo["imgSrc"])
        print(imgInfo["labels"])
        return json.dumps("POST Successfully")
    except Exception:
        return traceback.format_exc()
#########################   Image Confirmation  #########################

#########################   C3 Chart AJAX   #############################
@app.route("/getCpuUsage", methods=['POST'])
def getCpuUsage():
    """
    Function to get the image storage status from the database
    """
    try:
        return json.dumps([
          ['x', '2013-01-07', '2013-01-08', '2013-01-09', '2013-01-10', '2013-01-11', '2013-01-12'],
          ['CPU Usage', 46, 78, 88, 72, 98, 88]
        ])
    except Exception:
        return traceback.format_exc()

@app.route("/getMemLoad", methods=['POST'])
def getMemLoad():
    """
    Function to get the image storage status from the database
    """
    try:
        return json.dumps([
          ['x', '2013-01-07', '2013-01-08', '2013-01-09', '2013-01-10', '2013-01-11', '2013-01-12'],
          ['Memory Load', 46, 78, 88, 72, 98, 88]
        ])
    except Exception:
        return traceback.format_exc()

@app.route("/getNetTraff", methods=['POST'])
def getNetTraff():
    """
    Function to get the image storage status from the database
    """
    try:
        return json.dumps([
          ['x', '2013-01-07', '2013-01-08', '2013-01-09', '2013-01-10', '2013-01-11', '2013-01-12'],
          ['Network Traffic', 100, 120, 130, 150, 120, 135]
        ])
    except Exception:
        return traceback.format_exc()

@app.route("/getCpuTemp", methods=['POST'])
def getCpuTemp():
    """
    Function to get the image storage status from the database
    """
    try:
        return json.dumps([
          ['x', '2013-01-07', '2013-01-08', '2013-01-09', '2013-01-10', '2013-01-11', '2013-01-12'],
          ['CPU Temperature', 46, 50, 65, 72, 78, 54]
        ])
    except Exception:
        return traceback.format_exc()

@app.route("/getImgStorage", methods=['POST'])
def getImgStorage():
    """
    Function to get the image storage status from the database
    """
    try:
        return json.dumps([
            ['mattress', 376], ['couch', 456], ['tv-monitor', 231]
        ])
    except Exception:
        return traceback.format_exc()

@app.route("/getDBIO", methods=['POST'])
def getDBIO():
    """
    Function to get the image storage status from the database
    """
    try:
        return json.dumps([
            ['x', '2013-01-07', '2013-01-08', '2013-01-09', '2013-01-10', '2013-01-11', '2013-01-12'],
            ['Database I/O Traffic', 20, 30, 88, 72, 98, 88]
        ])
    except Exception:
        return traceback.format_exc()

@app.route("/getDBQuery", methods=['POST'])
def getDBQuery():
    """
    Function to get the image storage status from the database
    """
    try:
        return json.dumps([
            ['x', '2013-01-07', '2013-01-08', '2013-01-09', '2013-01-10', '2013-01-11', '2013-01-12'],
            ['Database Queries', 200, 300, 880, 720, 980, 880]
        ])
    except Exception:
        return traceback.format_exc()

@app.route("/getDatasetSize", methods=['POST'])
def getDatasetSize():
    """
    Function to get the image storage status from the database
    """
    try:
        return json.dumps([
            ['x', '2013-01-07', '2013-01-08', '2013-01-09', '2013-01-10', '2013-01-11', '2013-01-12'],
            ['mattress', 176, 180, 188, 190, 192, 196],
            ['couch', 156, 166, 276, 286, 390, 396],
            ['tv-monitor', 55, 167, 173, 285, 389, 197]
        ])
    except Exception:
        return traceback.format_exc()

@app.route("/getImgConf", methods=['POST'])
def getImgConf():
    """
    Function to get the image storage status from the database
    """
    try:
        return json.dumps([
            ['x', '2013-01-07', '2013-01-08', '2013-01-09', '2013-01-10', '2013-01-11', '2013-01-12'],
            ['mattress', 176, 180, 188, 190, 192, 196],
            ['couch', 156, 166, 276, 286, 390, 396],
            ['tv-monitor', 55, 167, 173, 285, 389, 197]
        ])
    except Exception:
        return traceback.format_exc()

@app.route("/getUpImg", methods=['POST'])
def getUpImg():
    """
    Function to get the image storage status from the database
    """
    try:
        return json.dumps([
            ['x', '2013-01-07', '2013-01-08', '2013-01-09', '2013-01-10', '2013-01-11', '2013-01-12'],
            ['mattress', 176, 180, 188, 190, 192, 196],
            ['couch', 156, 166, 276, 286, 390, 396],
            ['tv-monitor', 55, 167, 173, 285, 389, 197]
        ])
    except Exception:
        return traceback.format_exc()

@app.route("/getDetectedObj", methods=['POST'])
def getDetectedObj():
    """
    Function to get the image storage status from the database
    """
    try:
        return json.dumps([
            ['x', '2013-01-07', '2013-01-08', '2013-01-09', '2013-01-10', '2013-01-11', '2013-01-12'],
            ['mattress', 26, 20, 18, 19, 19, 16],
            ['couch', 15, 16, 26, 26, 39, 36],
            ['tv-monitor', 55, 17, 13, 25, 39, 19]
        ])
    except Exception:
        return traceback.format_exc()

@app.route("/getAP", methods=['POST'])
def getAP():
    """
    Function to get the image storage status from the database
    """
    try:
        return json.dumps([
            ['x', '2013-01-07', '2013-01-08', '2013-01-09', '2013-01-10', '2013-01-11', '2013-01-12'],
            ['mattress', 76, 80, 88, 90, 92, 96],
            ['couch', 56, 66, 76, 86, 90, 96],
            ['tv-monitor', 55, 67, 73, 85, 89, 97]
        ])
    except Exception:
        return traceback.format_exc()
#########################   C3 Chart AJAX   #############################

@app.route("/getConfirmationStats", methods=['POST'])
def getClassifiactionStats():
    """
    This is function for API of getting classification stats

    Returns:
        json String: [count for category 1, count for category 2,
         count for category 3, count for unkonwn, total image count]

    ---
    TODO: use piechart to show the result
    """
    if request.method == 'POST':
        confirmation_arr, time_stamp = [], []
        # counterUnknown, counter1, counter2, counter3, denominator = 0, 0, 0, 0, 0
        count, count_tv, count_mattress, count_couch, count_chair, count_refrigerator, count_cart, count_clean, count_unidentified = 0, 0, 0, 0, 0, 0, 0, 0, 0
        s = select([ImageCategory, ImageConfirmation, AlertImage]).where(ImageConfirmation.alert_id == AlertImage.alert_id ).\
            where(ImageCategory.category_id == ImageConfirmation.confirmation_id).\
            order_by(ImageConfirmation.classification_datetime.desc())
        result = conn.execute(s)
        for row in result:
            print(row[1])
            if row[1]== 'tv-monitor':
                count_tv += 1
            if row[1] == 'couch':
                count_couch += 1
            if row[1] == 'mattress':
                count_mattress += 1
            if row[1] == 'chair':
                count_chair += 1
            if row[1] == 'refrigerator':
                count_refrigerator += 1
            if row[1] == 'shopping-cart':
                count_cart += 1
            if row[1] == 'clean':
                count_clean += 1
            if row[1] == 'unidentified':
                count_unidentified += 1
            count += 1
            print(row)

        classfication_stats_arr = [count_tv, count_mattress, count_couch, count_chair, count_refrigerator, count_cart, count_clean, count_unidentified, count]

        json_str = json.dumps(classfication_stats_arr)
        return json_str

#helper function
def allowed_file_type(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_FILE_EXTENSIONS


if __name__ == "__main__":
	app.run(debug=True)
