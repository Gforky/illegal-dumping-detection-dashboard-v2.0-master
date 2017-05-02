from flask import Flask
from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import models
from werkzeug import secure_filename
from flask import json
import os
from os.path import isfile, join
from sqlalchemy.sql import select
import zipfile
import subprocess
import re
import pickle
from models import Base, ImageCategory, ImageConfirmation
from flask_pymongo import PyMongo
import datetime
from pymongo import MongoClient
from random import randint


app = Flask(__name__)
UPLOAD_FOLDER = 'static/detection-component/alert_image'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['current_path'] = os.getcwd()
ALLOWED_FILE_EXTENSIONS = set(['png', 'jpg'])

#connect mongodb
client = MongoClient()
mongodb = client.illegaldumpingdb

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
        if imgFile:
            filename = secure_filename(imgFile.filename)
            imgFile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #for mongodb
            waiting_id = randint(0, 100000)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            isAlerted = False
            upload_list = mongodb.upload_lists
            upload_list.insert({'waiting_id': waiting_id, 'image_path': image_path, 'isAlerted': isAlerted, 'datetime': datetime.datetime.utcnow()})

            typename = filename.split('.')[0]
            folderPath = os.path.join(app.config['UPLOAD_FOLDER'])

            # if filename.endswith('.zip'):
            #     zip_file = zipfile.ZipFile(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r')
            #     zip_file.extractall(folderPath)
            #     zip_file.close()
        return 'sucessfully upload'
    return 'not successfully upload'

#########################   Image Confirmation  #########################
@app.route("/imgConfirmation", methods=['POST'])
def imgConfirmation():
    '''
    Function to move the images from tempory folder to the new dataset folder
    '''
    #['mattress','sofa','tvmonitor',fridge,'chair','shoppingcart', 'cleanstreet']
    engine = create_engine('postgresql://localhost:5433/cmpe295')
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        data = request.get_json()
        print(data['img_path'])
        print(data['labels'])
        confirmation1 = ImageConfirmation(category_id= int(data['labels'][0] + 1), image_path= str(data['img_path']))
        session.add(confirmation1)
        session.commit()

        update_list = []
        upload_lists = mongodb.upload_lists
        # #get monogodb data
        for upload_list in upload_lists.find({"image_path": 'static' + data['img_path']}):
            update_list.append(upload_list['waiting_id'])
        # # update mongodb
        for elem in update_list:
            upload_lists.update_one({"waiting_id": int(elem)},{"$set":{"isAlerted": True}})

        return json.dumps([{'msg' : 'successfully transfered'}])
        # return json.dumps([data])
        #return json.dumps([{'msg' : 'successfully transfered'}])
    except Exception:
        return 'no new image'
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
            ['mattress', 376], ['couch', 456], ['tv-monitor', 231], ['clean-street', 231]
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
            ['clean-street', 55, 67, 73, 85, 89, 97]
        ])
    except Exception:
        return traceback.format_exc()

@app.route("/getDetectedObj", methods=['POST'])
def getDetectedObj():
    """
    Function to get the image storage status from the database

    update:
          get potential dupming image status based on uplaod image or remote send pictures
    """
    try:
        upload_lists = mongodb.upload_lists
        result_potential = ['potential_dumping']
        result_date = ['x']
        count = 0
        prevDate = None
        index = 0
        for upload_list in upload_lists.find({"isAlerted": False}, {"_id":0}):
            if index > 6:
                break

            datetime = str(upload_list['datetime']).split(',', 1)
            date = str(datetime)[2:12]

            if date == prevDate:
                count += 1

            else:
                if count != 0:
                    result_potential.append(count)
                prevDate = date
                result_date.append(date)
                index += 1
                count = 1

        if count != 0:
            result_potential.append(count)

        json_str = json.dumps([result_date, result_potential])
        return json_str
        # return json.dumps([
        #     ['x', '2013-01-07', '2013-01-08', '2013-01-09', '2013-01-10', '2013-01-11', '2013-01-12'],
        #     ['mattress', 26, 20, 18, 19, 19, 16],
        #     ['couch', 15, 16, 26, 26, 39, 36],
        #     ['tv-monitor', 55, 17, 13, 25, 39, 19],
        #     ['clean-street', 55, 67, 73, 85, 89, 97]
        # ])
    except Exception:
        return 'error'

@app.route("/getAP", methods=['POST'])
def getAP():
    """
    Function to get the image storage status from the database

    mean accuracy
    """
    try:
        detected_lists = mongodb.detected_lists
        result_accuracy, result_time, index = ['average_accuracy'], ['x'], 0
        prevTime = None
        total_accuracy = 0
        count = 0
        for detected_list in detected_lists.find({},{'_id':0}):
            if index > 6:
                break

            detected_datetime, detected_top3_accuracies, detected_top3_labels = str(detected_list['datetime']).split(',', 1), detected_list['top3_accuracies'], detected_list['top3_labels']
            date = str(detected_datetime)[2:12]
            print(date)
            if prevTime == None:
                result_time.append(date)
                prevTime = date
                index += 1

            if date == prevTime:
                total_accuracy += detected_top3_accuracies[0]
                count += 1
                prevTime = date
            else:
                result_time.append(date)
                total_accuracy /= count
                result_accuracy.append(total_accuracy)
                count = 1
                total_accuracy = detected_top3_accuracies[0]
                index += 1


        if total_accuracy:
            result_accuracy.append(total_accuracy/count)

        return json.dumps([result_time, result_accuracy
            # ['x', '2013-01-07', '2013-01-08', '2013-01-09', '2013-01-10', '2013-01-11', '2013-01-12'],
            # ['mattress', 76, 80, 88, 90, 92, 96],
            # ['couch', 56, 66, 76, 86, 90, 96],
            # ['tv-monitor', 55, 67, 73, 85, 89, 97],
            # ['clean-street', 55, 67, 73, 85, 89, 97]
        ])
    except Exception:
        return 'error'
#########################   C3 Chart AJAX   #############################

@app.route("/getConfirmationStats", methods=['POST'])
def getConfirmationStats():
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
        count, count_tv, count_mattress, count_couch, count_chair, count_refrigerator, count_cart, count_clean = 0, 0, 0, 0, 0, 0, 0, 0
        s = select([ImageCategory, ImageConfirmation]).\
            where(ImageCategory.category_id == ImageConfirmation.category_id).\
            order_by(ImageConfirmation.classification_datetime.desc())
        result = conn.execute(s)

        for row in result:
            print(row)
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
            if row[1] == 'clean-street':
                count_clean += 1
            count += 1

        classfication_stats_arr = [['tv-monitor', count_tv],
                                   ['mattress', count_mattress],
                                   ['couch', count_couch],
                                   ['chair', count_chair],
                                   ['refrigerator', count_refrigerator],
                                   ['shopping-cart', count_cart],
                                   ['clean-street', count_clean]]

        json_str = json.dumps(classfication_stats_arr)
        return json_str

@app.route("/check_temp_folder_classify", methods=['POST'])
def check_temp_folder_classify():
    folderPath = os.path.join(app.config['UPLOAD_FOLDER'])
    folder_file, folder_arr = [], []
    for file in os.listdir(folderPath):
        if not isfile(join(folderPath, file)) and str(file) == 'car':
            folder_arr.append(file)

    for folder in folder_arr:
        folder_file.append(folder)

    image_inFolder = []
    for filename in folder_file:
        for file in os.listdir(os.path.join(folderPath, filename)):
            image_inFolder.append(os.path.abspath(os.path.join(folderPath, file)))

    json_str = json.dumps([folder_arr, image_inFolder])
    return json_str

@app.route("/trigger_detect", methods=['POST'])
def trigger_detect():
    engine = create_engine('postgresql://localhost:5433/cmpe295')
    Session = sessionmaker(bind=engine)
    session = Session()

    upload_lists = mongodb.upload_lists
    detected_list = mongodb.detected_lists
    result = []
    wait_list = []
    problem_list = []

    for upload_list in upload_lists.find({"isAlerted": False}, {"_id":0}):
        wait_list.append(upload_list)

    for elem in wait_list:
        elem_path = elem['image_path']
        print(elem_path)
        #static/detection-component/alert_image/mattress3.jpg
        result = subprocess.check_output('python3 static/detection-component/classify.py --image_dir '+ elem_path +' --model_dir static/detection-component/output_graph.pb --label_dir static/detection-component/output_labels.txt', shell=True)
        with open('result.pickle', 'rb') as f:
            unpickled_result = pickle.load(f)

        result_pickle = (unpickled_result)
        result_imagepath = unpickled_result['imagepath']
        result_top3labels = unpickled_result['top3labels']
        result_top3accuracies = unpickled_result['top3accuracies']

        detected_id = randint(0, 100000)

        #save detection result
        if result_imagepath not in detected_list.find({'image_path': result_imagepath}, {"_id":0}):
            detected_list.insert({'detected_id': detected_id,
                                'image_path': result_imagepath,
                                'top3_labels': result_top3labels,
                                'top3_accuracies': result_top3accuracies,
                                'datetime':datetime.datetime.utcnow()})

        #if over than threshold add into db directly
        if result_top3accuracies[0] < 0.7:
            # confirmation_image = ImageConfirmation(category_id='2', alert_id='1')
            # session.add(confirmation_image)
            # session.commit()
            print('test')
        else:
            problem_list.append([result_imagepath, result_top3labels, result_top3accuracies])

            # alert_image1 = AlertImage(image_name=result_imagepath)
            # session.add(alert_image1)
            # session.commit()
        os.remove("result.pickle")


    engine.dispose()
    # json_str = json.dumps([result_imagepath, result_top3labels, result_top3accuracies])
    print(problem_list)
    json_str = json.dumps(problem_list)
    return json_str


#helper function
def allowed_file_type(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_FILE_EXTENSIONS


if __name__ == "__main__":
    app.run(debug=True)
