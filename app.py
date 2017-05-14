from flask import Flask
from flask import render_template, request
from werkzeug import secure_filename
from flask import json
import os
from os.path import isfile, join
import sys
import zipfile
import subprocess
import re
import pickle
from flask_pymongo import PyMongo
import datetime
from pymongo import MongoClient
from random import randint
import traceback


app = Flask(__name__)
parent_path = os.path.dirname(os.getcwd())
UPLOAD_FOLDER = 'static/detection-component/alert_image'
RETRAIN_FOLDER = 'tensorflow/tensorflow/retrain_image'
app.config['RETRAIN_FOLDER'] = RETRAIN_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['current_path'] = os.getcwd()

#connect mongodb
client = MongoClient()
mongodb = client.illegaldumpingdb

#web services API
@app.route("/")
def hello():
    return "Welcome to illegal dumping dashboard! Please visit index page."

@app.route("/index")
def index():
	return render_template('index.html')

@app.route("/retrain-model", methods=['POST'])
def retrainmodel():
    """
        This API is to retrain the model
    """
    result, count = [], 0
    confirmation_lists = mongodb.confirmation_lists
    retrain_lists = mongodb.retrain_lists
    labelIndex = {'1' : 'mattress', '2' : 'couch', '3' : 'tv-monitor', '4' : 'refrigerator' , '5' :'chair', '6' : 'shopping-cart', '7' : 'clean-street'}
    number_of_images = 0
    try:
        for confirmation_list in confirmation_lists.find({}, {'_id': 0}):
            category = confirmation_list['category']
            imagePath = confirmation_list['image_path']

            #copy file to certain category
            command_line = "cp " + imagePath + " " + "../images/training_images/" + category + "/"
            output = subprocess.call(command_line, shell=True)

            #retrain command
            os.system('python3 ../tensorflow/tensorflow/examples/image_retraining/retrain.py --image_dir ../images/training_images --output_graph ../results/output_graph.pb --output_labels ../results/output_labels.txt --bottleneck_dir ../results/bottleneck --summaries_dir ../results/retrain_logs')

        #insert retrain data
        retrain_info = get_retrain_info()
        retrain_lists.insert({'retrain_info': retrain_info, 'datetime': datetime.datetime.utcnow()})

        #get the latest retrain data
        for retrain_list in retrain_lists.find({}).limit(1).sort('datetime', -1):
            result.append(retrain_list)

        json_str = json.dumps(result)
        return json_str

    except Exception:
        return 'cannot retrain'

@app.route("/upload-files", methods=['GET', 'POST'])
def uploadfile(): #299 * 299, jpg
    """
        This api is for uploading the file
    """
    if request.method == 'POST':
        imgFile = request.files['file']
        if imgFile:
            filename = secure_filename(imgFile.filename)
            imgFile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            #for mongodb insert operation
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            isAlerted = False
            upload_list = mongodb.upload_lists
            upload_list.insert({'image_path': image_path, 'isAlerted': isAlerted, 'datetime': datetime.datetime.utcnow()})

            typename = filename.split('.')[0]
            folderPath = os.path.join(app.config['UPLOAD_FOLDER'])

        return 'sucessfully upload'
    return 'not successfully upload'

#########################   Image Confirmation  #########################
@app.route("/imgConfirmation", methods=['POST'])
def imgConfirmation():
    """
    Function to move the images from tempory folder to the new dataset folder
    """

    try:
        data = request.get_json()
        index_to_label = {'0' : 'couch', '1' : 'mattress', '2' : 'tv-monitor', '3' : 'chair' , '4' :'tv-monitor', '5' : 'shopping-cart', '6' : 'clean-street'}

        #mongod db insertion
        confirmation_lists = mongodb.confirmation_lists
        confirmation_lists.insert({'image_path': data['img_path'], 'category':index_to_label[str(data['labels'][0])], 'datetime': datetime.datetime.utcnow()})

        update_list = []
        upload_lists = mongodb.upload_lists

        #get monogodb data
        for upload_list in upload_lists.find({"image_path": data['img_path']}):
            update_list.append(upload_list['_id'])

        # update mongodb
        for elem in update_list:
            upload_lists.update_one({"_id": elem},{"$set":{"isAlerted": True}})

        return json.dumps({'msg' : 'successfully transfered'})

    except Exception:
        print(traceback.format_exc())
        return json.dumps({'msg' : 'failed transfered'})
#########################   Image Confirmation  #########################

#########################   C3 Chart AJAX   #############################

@app.route("/getRetrainData", methods=['POST'])
def getImgStorage():
    """
    Function to get the image retrained data from the database
    """
    try:
        retrain_lists = mongodb.retrain_lists
        count_tv, count_couch, count_mattress, count_chair, count_refrigerator, count_cart, count_clean, count = \
        0, 0, 0, 0, 0, 0, 0, 0
        result =[]

        #get the latest retrain
        for retrain_list in retrain_lists.find({}, {"_id": 0}).limit(1).sort('datetime', -1):
            for category_list in retrain_list['retrain_info']:
                category, category_count = category_list, retrain_list['retrain_info'][category_list]

                if category == 'tv monitor':
                    count_tv += category_count

                if category == 'couch':
                    count_couch += category_count

                if category == 'mattress':
                    count_mattress += category_count

                if category == 'chair':
                    count_chair += category_count

                if category == 'refrigerator':
                    count_refrigerator += category_count

                if category == 'shopping-cart':
                    count_cart += category_count

                if category == 'clean':
                    count_clean += category_count

        result_count = [['tv monitor', count_tv],
                                   ['mattress', count_mattress],
                                   ['couch', count_couch],
                                   ['chair', count_chair],
                                   ['refrigerator', count_refrigerator],
                                   ['shopping-cart', count_cart],
                                   ['clean-street', count_clean]]

        return json.dumps(result_count)

    except Exception:
        return 'error'


@app.route("/getLowAccuracyData", methods=['POST'])
def getLowAccuracyData():
    """
    Function to get the image storage status from the database
    """
    try:
        low_accuracy_lists = mongodb.low_accuracy_lists
        result, total_threshold = [], 0
        count_tv, count_couch, count_mattress, count_chair, count_refrigerator, count_cart, count_clean, count = \
        0, 0, 0, 0, 0, 0, 0, 0

        for low_accuracy_list in low_accuracy_lists.find({}, {"_id": 0}):
            result_category, result_threshold = label_transform(low_accuracy_list['category']), low_accuracy_list['threshold']
            result.append([result_category, result_threshold])

            if result_category == 'tv monitor':
                count_tv += 1
            if result_category == 'couch':
                count_couch += 1
            if result_category == 'mattress':
                count_mattress += 1
            if result_category == 'chair':
                count_chair += 1
            if result_category == 'refrigerator':
                count_refrigerator += 1
            if result_category == 'shopping-cart':
                count_cart += 1
            if result_category == 'clean-street':
                count_clean += 1

            total_threshold += result_threshold
            count += 1

        total_threshold /= count

        result_count = [['tv monitor', count_tv],
                                   ['mattress', count_mattress],
                                   ['couch', count_couch],
                                   ['chair', count_chair],
                                   ['refrigerator', count_refrigerator],
                                   ['shopping-cart', count_cart],
                                   ['clean-street', count_clean]]

        return json.dumps([result_count, total_threshold])

    except Exception:
        return 'error'

@app.route("/getImgConf", methods=['POST'])
def getImgConf():
    """
        API that can get the image confirmation data
    """
    try:
        detected_lists = mongodb.detected_lists
        result = {}
        result_date = ['x']
        result_mattress, result_couch, result_tvmonitor, result_refri, result_chair, result_shopping, result_clean \
        = ['mattress'], ['couch'], ['tv monitor'], ['refrigerator'], ['chair'], ['shopping-cart'], ['clean-street']
        prevDate, index = None, 0

        #get the detected result from db
        for detected_list in detected_lists.find():
            if index > 6:
                break

            detected_datetime, detected_top3_accuracies, detected_top3_labels = str(detected_list['datetime']).split(',', 1), detected_list['top3_accuracies'], detected_list['top3_labels']
            date = str(detected_datetime)[2:12]

            if prevDate == None:
                prevDate = date
                result_date.append(date)
                result['mattress'], result['couch'], result['tv monitor'], result['refrigerator'], result['chair'], result['shopping-cart'], result['clean-street'] \
                = 0, 0, 0, 0, 0, 0, 0
                index += 1

            if date != prevDate:
                result_mattress.append(result['mattress'])
                result_couch.append(result['couch'])
                result_tvmonitor.append(result['tv monitor'])
                result_refri.append(result['refrigerator'])
                result_chair.append(result['chair'])
                result_shopping.append(result['shopping-cart'])
                result_clean.append(result['clean-street'])
                result['mattress'], result['couch'], result['tv monitor'], result['refrigerator'], result['chair'], result['shopping-cart'], result['clean-street'] \
                = 0, 0, 0, 0, 0, 0, 0
                prevDate = date
                result_date.append(date)
                index += 1

            label = label_transform(detected_top3_labels[0])
            if label == 'mattress':
                result['mattress'] += 1
            if label == 'couch':
                result['couch'] += 1
            if label == 'tv monitor':
                result['tv monitor'] += 1
            if label == 'refrigerator':
                result['refrigerator'] += 1
            if label == 'chair':
                result['chair'] += 1
            if label == 'shopping cart':
                result['shopping-cart'] += 1
            if label == 'clean':
                result['clean-street'] += 1

        result_mattress.append(result['mattress'])
        result_couch.append(result['couch'])
        result_tvmonitor.append(result['tv monitor'])
        result_refri.append(result['refrigerator'])
        result_chair.append(result['chair'])
        result_shopping.append(result['shopping-cart'])
        result_clean.append(result['clean-street'])

        return json.dumps([
            result_date,
            result_mattress,
            result_couch,
            result_tvmonitor,
            result_refri,
            result_chair,
            result_shopping,
            result_clean
        ])

    except Exception:
        return 'error'

@app.route("/getUpImg", methods=['POST'])
def getUpImg():
    """
    Function to get the upload images from db
    """
    try:

        upload_lists = mongodb.upload_lists
        result_time, result_count = ['x'], ['upload_object']
        prevTime, count, index = None, 0, 0

        #find the data from database
        for upload_list in upload_lists.find({}, {"_id": 0}):
            if index > 6:
                break

            time = time_transform(upload_list['datetime'])
            if prevTime == None:
                prevTime = time
                result_time.append(time)
                count = 1
                index += 1

            if time == prevTime:
                count += 1

            else:
                prevTime = time
                result_count.append(count)
                result_time.append(time)
                count = 1
                index += 1

        if count != 0:
            result_count.append(count)

        return json.dumps([ result_time, result_count])

    except Exception:
        return traceback.format_exc()

@app.route("/getDetectedObj", methods=['POST'])
def getDetectedObj():
    """
        Function to get the detected object data
    """
    try:

        detected_lists = mongodb.detected_lists
        result, index = {}, 0
        result_date = ['x']
        result_mattress, result_couch, result_tvmonitor, result_refri, result_chair, result_shopping, result_clean \
        = ['mattress'], ['couch'], ['tv monitor'], ['refrigerator'], ['chair'], ['shopping-cart'], ['clean-street']
        prevDate = None

        for detected_list in detected_lists.find({}, {'_id': 0}):
            if index > 6:
                break

            detected_top3_accuracies, detected_top3_labels =  detected_list['top3_accuracies'], detected_list['top3_labels']
            detected_datetime = time_transform(detected_list['datetime'])
            if prevDate == None:
                prevDate = detected_datetime
                result_date.append(detected_datetime)
                result['mattress'], result['couch'], result['tv monitor'], result['refrigerator'], result['chair'], result['shopping-cart'], result['clean-street'] \
                = 0, 0, 0, 0, 0, 0, 0
                index += 1

            if detected_datetime != prevDate:
                result_mattress.append(result['mattress'])
                result_couch.append(result['couch'])
                result_tvmonitor.append(result['tv monitor'])
                result_refri.append(result['refrigerator'])
                result_chair.append(result['chair'])
                result_shopping.append(result['shopping-cart'])
                result_clean.append(result['clean-street'])
                result['mattress'], result['couch'], result['tv-monitor'], result['refrigerator'], result['chair'], result['shopping-cart'], result['clean-street'] \
                = 0, 0, 0, 0, 0, 0, 0
                prevDate = detected_datetime
                result_date.append(detected_datetime)
                index += 1

            else:
                label = label_transform(detected_top3_labels[0])
                if label == 'mattress':
                    result['mattress'] += 1
                if label == 'couch':
                    result['couch'] += 1
                if label == 'tv-monitor':
                    result['tv-monitor'] += 1
                if label == 'refrigerator':
                    result['refrigerator'] += 1
                if label == 'chair':
                    result['chair'] += 1
                if label == 'shopping-cart':
                    result['shopping-cart'] += 1
                if label == 'clean-street':
                    result['clean-street'] += 1

        result_mattress.append(result['mattress'])
        result_couch.append(result['couch'])
        result_tvmonitor.append(result['tv monitor'])
        result_refri.append(result['refrigerator'])
        result_chair.append(result['chair'])
        result_shopping.append(result['shopping-cart'])
        result_clean.append(result['clean-street'])

        json_str = json.dumps([result_date, result_mattress, result_couch, \
            result_tvmonitor, result_refri, result_chair, result_shopping, \
            result_clean
            ])

        return json_str

    except Exception:
        return 'error'

@app.route("/getAP", methods=['POST'])
def getAP():
    """
    API to get the average accuracy recognition data
    """
    try:
        detected_lists = mongodb.detected_lists
        result_accuracy, result_time, index = ['average_accuracy'], ['x'], 0
        prevTime, total_accuracy, count = None, 0, 0

        for detected_list in detected_lists.find({},{'_id':0}):
            if index > 6:
                break

            detected_datetime, detected_top3_accuracies, detected_top3_labels = time_transform(detected_list['datetime']), detected_list['top3_accuracies'], detected_list['top3_labels']

            if prevTime == None:
                result_time.append(detected_datetime)
                prevTime = detected_datetime
                index += 1

            if detected_datetime == prevTime:
                total_accuracy += detected_top3_accuracies[0]
                count += 1
                prevTime = detected_datetime

            else:
                result_time.append(detected_datetime)
                total_accuracy /= count
                result_accuracy.append(total_accuracy)
                count = 1
                index += 1

        if total_accuracy:
            result_accuracy.append(total_accuracy/count)

        return json.dumps([result_time, result_accuracy])

    except Exception:
        return 'error'
#########################   C3 Chart AJAX   #############################

@app.route("/getConfirmationStats", methods=['POST'])
def getConfirmationStats():
    """
    This is function for API of getting confirmation data from db
    """

    if request.method == 'POST':
        confirmation_arr, time_stamp = [], []
        count, count_tv, count_mattress, count_couch, count_chair, count_refrigerator, count_cart, count_clean = 0, 0, 0, 0, 0, 0, 0, 0
        confirmation_lists = mongodb.confirmation_lists
        result = []

        for confirmation_list in confirmation_lists.find({},{'_id':0}):
            print(confirmation_list)
            result.append(confirmation_list)
            if confirmation_list['category'] == 'tv-monitor':
                count_tv += 1
            if confirmation_list['category'] == 'couch':
                count_couch += 1
            if confirmation_list['category'] == 'mattress':
                count_mattress += 1
            if confirmation_list['category'] == 'chair':
                count_chair += 1
            if confirmation_list['category'] == 'refrigerator':
                count_refrigerator += 1
            if confirmation_list['category'] == 'shopping-cart':
                count_cart += 1
            if confirmation_list['category'] == 'clean-street':
                count_clean += 1
            count += 1

        confirmation_stats_arr = [['tv monitor', count_tv],
                                   ['mattress', count_mattress],
                                   ['couch', count_couch],
                                   ['chair', count_chair],
                                   ['refrigerator', count_refrigerator],
                                   ['shopping-cart', count_cart],
                                   ['clean-street', count_clean]]

        json_str = json.dumps(confirmation_stats_arr)
        return json_str

@app.route("/trigger_detect", methods=['POST'])
def trigger_detect():
    """
    This API is for detecting object which is triggered by admin
    """

    upload_lists = mongodb.upload_lists
    detected_lists = mongodb.detected_lists
    low_accuracy_lists = mongodb.low_accuracy_lists
    result, wait_list, problem_list = [], [], []
    data = request.get_json()
    threshold = data['threshold']
    labelIndex = {'mattress' : 1, 'couch' : 2, 'tv-monitor' : 3, 'refrigerator' : 4, 'chair' : 5, 'shopping-cart' : 6, 'clean-street' : 7}

    try:
        for upload_list in upload_lists.find({"isAlerted": False}, {"_id":0}):
            wait_list.append(upload_list)

        for elem in wait_list:
            elem_path = elem['image_path']
            result = subprocess.check_output('python3 ../results/classify.py --image_dir '+ elem_path +' --model_dir ../results/output_graph.pb --label_dir ../results/output_labels.txt', shell=True)
            with open('result.pickle', 'rb') as f:
                unpickled_result = pickle.load(f)

            result_pickle = (unpickled_result)
            result_imagepath = unpickled_result['imagepath']
            result_top3labels = unpickled_result['top3labels']
            result_top3accuracies = unpickled_result['top3accuracies']

            #save detection result if not in the detected_lists
            detected_object = detected_lists.find_one({'image_path': result_imagepath}, {"_id":0})
            if not detected_object:
                detected_lists.insert({'image_path': result_imagepath,
                                    'top3_labels': result_top3labels,
                                    'top3_accuracies': result_top3accuracies,
                                    'datetime':datetime.datetime.utcnow()})


            isAboveThreshold = False
            #if accuracy more than threshold set isAlerted true directly
            if result_top3accuracies[0] >= threshold:
                isAboveThreshold = True
                update_list = []

                #get monogodb data
                for upload_list in upload_lists.find({"image_path": result_imagepath}):
                    update_list.append(upload_list['_id'])

                # update mongodb
                for elem in update_list:
                    upload_lists.update_one({"_id": elem},{"$set":{"isAlerted": True}})

            #if low accuracy, write into db, waiting for future examination
            else:

                low_accuracy_object = low_accuracy_lists.find_one({"image_path": result_imagepath})
                problem_list.append([result_imagepath, result_top3labels, result_top3accuracies])

                #prevent duplicate
                if low_accuracy_object:
                    continue

                else:
                    low_accuracy_lists.insert({'category': result_top3labels[0], 'threshold': threshold, 'image_path': result_imagepath, 'datetime': datetime.datetime.utcnow()})

            os.remove("result.pickle")

        if not isAboveThreshold:
            json_str = json.dumps(problem_list)

        else:
            json_str = json.dumps(problem_list)

        return json_str

    except Exception:
        return 'Error'


#helper function
def time_transform(transform_time):
    """
    Function to transform time to the desired format
    """
    list_datetime = str(transform_time).split(',', 1)
    date = str(list_datetime)[2:12]
    return date

def label_transform(transform_label):
    """
    Function to transform label to desired format
    """
    label = str(transform_label)[2:-3]
    return label

def get_retrain_info():
    """
    Get the data that need to be retrained
    """
    folderPath = os.path.join(RETRAIN_FOLDER)
    result = {'mattress': 0, 'tv-monitor': 0, 'shopping-cart': 0, 'couch': 0, 'clean-street': 0, 'chair': 0, 'refrigerator': 0}
    folder_file, folder_arr, count = [], [], 0
    for folder in os.listdir(folderPath):
        if not isfile(join(folderPath, folder)):
            folder_arr.append(folder)

    for folder in folder_arr:
        for file in os.listdir(os.path.join(folderPath, folder)):
            if folder == 'tv-monitor':
                result['tv-monitor'] += 1

            if folder == 'mattress':
                result['mattress'] += 1

            if folder == 'couch':
                result['couch'] += 1

            if folder == 'chair':
                result['chair'] += 1

            if folder == 'refrigerator':
                result['refrigerator'] += 1

            if folder == 'shopping-cart':
                result['shopping-cart'] += 1

            if folder == 'clean-street':
                result['clean-street'] += 1

    return result

if __name__ == "__main__":
    app.run(debug=True)
