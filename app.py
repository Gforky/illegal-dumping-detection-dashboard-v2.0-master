from flask import Flask
from flask import render_template, request
import models
from werkzeug import secure_filename
from flask import json
import os
from os.path import isfile, join
import zipfile
import subprocess
import re
import pickle
from flask_pymongo import PyMongo
import datetime
from pymongo import MongoClient
from random import randint
import shutil


app = Flask(__name__)
parent_path = os.path.dirname(os.getcwd())
UPLOAD_FOLDER = 'static/detection-component/alert_image'
RETRAIN_FOLDER = parent_path + '/tensorflow/tensorflow/retrain_image'
print(RETRAIN_FOLDER)
app.config['RETRAIN_FOLDER'] = RETRAIN_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['current_path'] = os.getcwd()
ALLOWED_FILE_EXTENSIONS = set(['jpg'])

#connect mongodb
client = MongoClient()
mongodb = client.illegaldumpingdb

#web services API
@app.route("/")
def hello():
    return "Hello cmpe295 group!"

@app.route("/index")
def index():
	return render_template('index.html')

@app.route("/retrain-model", methods=['POST'])
def retrainmodel():
    """
        Still working on this part...
    """
    result, count = [], 0
    confirmation_lists = mongodb.confirmation_lists
    retrain_lists = mongodb.retrain_lists
    number_of_images = 0
    try:
        # for confirmation_list in confirmation_lists.find({}, {'_id': 0}):
        #     category = confirmation_list['category']
        #     imagePath = confirmation_list['image_path']
        #     datetime = transform_time(confirmation_list['datetime'])
        #
        #     result.append([category, imagePath, date])

            #retrain command
            # result = subprocess.check_output('bazel build tensorflow/examples/image_retraining:retrain', shell=True)

            #db insertion
        retrain_id = randint(0, 100000)
        retrain_info =  get_retrain_info()
        retrain_lists.insert({'retrain_id': retrain_id, 'retrain_info': retrain_info , 'datetime': datetime.datetime.utcnow()})
            #move folder
            # destination = shutil.move('static/detection-component/alert_image/' + imagePath, 'tensorflow/tensorflow/retrain_image/' + category +'/' + imagePath)
        json_str = json.dumps(retrain_info)
        return json_str

    except Exception:
        return 'cannot retrain'

@app.route("/upload-files", methods=['GET', 'POST'])
def uploadfile(): #299 * 299, jpg
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

    try:
        data = request.get_json()
        index_to_label = {'1': 'mattress', '2':'couch', '3': 'tv monitor', '4': 'refrigerator', '5': 'chair', '6':  'shopping-cart', '7': 'clean-street'}
        # print(data['img_path'])
        # print(data['labels'])

        #mongod db insertion
        confirmation_id = randint(0, 100000)
        confirmation_lists = mongodb.confirmation_lists
        confirmation_lists.insert({'confirmation_id':confirmation_id, 'image_path': data['img_path'], 'category':index_to_label[str(data['labels'][0])], 'datetime': datetime.datetime.utcnow()})

        update_list = []
        upload_lists = mongodb.upload_lists
        # #get monogodb data
        for upload_list in upload_lists.find({"image_path": data['img_path']}):
            #print("confima image : " + data['img_path'])
            update_list.append(upload_list['waiting_id'])
        # # update mongodb
        for elem in update_list:
            upload_lists.update_one({"waiting_id": int(elem)},{"$set":{"isAlerted": True}})

        return json.dumps([{'msg' : 'successfully transfered'}])

    except Exception:
        return 'no new image'
#########################   Image Confirmation  #########################

#########################   C3 Chart AJAX   #############################

@app.route("/getRetrainData", methods=['POST'])
def getImgStorage():
    """
    Function to get the image storage status from the database
    """
    try:
        retrain_lists = mongodb.retrain_lists
        count_tv, count_couch, count_mattress, count_chair, count_refrigerator, count_cart, count_clean, count = \
        0, 0, 0, 0, 0, 0, 0, 0
        result =[]

        for retrain_list in retrain_lists.find({}, {"_id": 0}):
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
        return traceback.format_exc()


@app.route("/getLowAccuracyData", methods=['POST'])
def getLowAccuracyData():
    """
    Function to get the image storage status from the database
    ### rename API
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

        return json.dumps([result_count, total_threshold
            # ['x', '2013-01-07', '2013-01-08', '2013-01-09', '2013-01-10', '2013-01-11', '2013-01-12'],
            # ['mattress', 176, 180, 188, 190, 192, 196],
            # ['couch', 156, 166, 276, 286, 390, 396],
            # ['tv monitor', 55, 167, 173, 285, 389, 197]
        ])
    except Exception:
        return 'error'

@app.route("/getImgConf", methods=['POST'])
def getImgConf():
    """
    Function to get the image storage status from the database
    get total detected object
    #ask
    """
    try:
        detected_lists = mongodb.detected_lists
        result = {}
        result_date = ['x']
        result_mattress, result_couch, result_tvmonitor, result_refri, result_chair, result_shopping, result_clean \
        = ['mattress'], ['couch'], ['tv monitor'], ['refrigerator'], ['chair'], ['shopping-cart'], ['clean-street']
        prevDate = None
        for detected_list in detected_lists.find():
            detected_datetime, detected_top3_accuracies, detected_top3_labels = str(detected_list['datetime']).split(',', 1), detected_list['top3_accuracies'], detected_list['top3_labels']
            date = str(detected_datetime)[2:12]

            if prevDate == None:
                prevDate = date
                result_date.append(date)
                result['mattress'], result['couch'], result['tv monitor'], result['refrigerator'], result['chair'], result['shopping-cart'], result['clean-street'] \
                = 0, 0, 0, 0, 0, 0, 0

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
        # result['mattress'], result['couch'], result['tv monitor'], result['refrigerator'], result['chair'], result['shopping-cart'], result['clean-street'] \
        # = 0, 0, 0, 0, 0, 0, 0

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
    Function to get the image storage status from the database
    """
    try:

        upload_lists = mongodb.upload_lists
        result_time, result_count = ['x'], ['upload_object']
        prevTime, count = None, 0
        for upload_list in upload_lists.find({}, {"_id": 0}):
            time = time_transform(upload_list['datetime'])
            if prevTime == None:
                prevTime = time
                result_time.append(time)
                count = 1

            if time == prevTime:
                count += 1

            else:
                prevTime = time
                result_count.append(count)
                result_time.append(time)
                count = 1

        if count != 0:
            result_count.append(count)

        return json.dumps([ result_time, result_count
            # ['x', '2013-01-07', '2013-01-08', '2013-01-09', '2013-01-10', '2013-01-11', '2013-01-12'],
            # ['mattress', 176, 180, 188, 190, 192, 196],
            # ['couch', 156, 166, 276, 286, 390, 396],
            # ['tv monitor', 55, 167, 173, 285, 389, 197]
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
                result['mattress'], result['couch'], result['tv monitor'], result['refrigerator'], result['chair'], result['shopping-cart'], result['clean-street'] \
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
    Function to get the image storage status from the database

    mean accuracy
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
                # total_accuracy = detected_top3_accuracies[0]
                index += 1


        if total_accuracy:
            result_accuracy.append(total_accuracy/count)

        return json.dumps([result_time, result_accuracy
            # ['x', '2013-01-07', '2013-01-08', '2013-01-09', '2013-01-10', '2013-01-11', '2013-01-12'],
            # ['mattress', 76, 80, 88, 90, 92, 96],
            # ['couch', 56, 66, 76, 86, 90, 96],
            # ['tv monitor', 55, 67, 73, 85, 89, 97],
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
        count, count_tv, count_mattress, count_couch, count_chair, count_refrigerator, count_cart, count_clean = 0, 0, 0, 0, 0, 0, 0, 0
        confirmation_lists = mongodb.confirmation_lists
        result = []
        for confirmation_list in confirmation_lists.find({},{'_id':0}):
            print(confirmation_list)
            result.append(confirmation_list)
            if confirmation_list['category'] == 'tv monitor':
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
    upload_lists = mongodb.upload_lists
    detected_lists = mongodb.detected_lists
    low_accuracy_lists = mongodb.low_accuracy_lists
    result, wait_list, problem_list = [], [], []
    data = request.get_json()
    threshold = data['threshold']
    labelIndex = {'mattress' : 1, 'couch' : 2, 'tv monitor' : 3, 'refrigerator' : 4, 'chair' : 5, 'shopping-cart' : 6, 'clean-street' : 7}

    try:
        for upload_list in upload_lists.find({"isAlerted": False}, {"_id":0}):
            wait_list.append(upload_list)

        for elem in wait_list:
            elem_path = elem['image_path']
            #static/detection-component/alert_image/mattress3.jpg
            result = subprocess.check_output('python3 static/detection-component/classify.py --image_dir '+ elem_path +' --model_dir static/detection-component/output_graph.pb --label_dir static/detection-component/output_labels.txt', shell=True)
            with open('result.pickle', 'rb') as f:
                unpickled_result = pickle.load(f)

            result_pickle = (unpickled_result)
            result_imagepath = unpickled_result['imagepath']
            result_top3labels = unpickled_result['top3labels']
            result_top3accuracies = unpickled_result['top3accuracies']
            detected_id, low_accuracy_id = randint(0, 100000), randint(0, 100000)

            #save detection result if not in the detected_lists
            detected_object = detected_lists.find_one({'image_path': result_imagepath}, {"_id":0})
            if not detected_object:
                detected_lists.insert({'detected_id': detected_id,
                                    'image_path': result_imagepath,
                                    'top3_labels': result_top3labels,
                                    'top3_accuracies': result_top3accuracies,
                                    'datetime':datetime.datetime.utcnow()})

            #add into probelm list waiting for return
            problem_list.append([result_imagepath, result_top3labels, result_top3accuracies])

            #if accuracy more than threshold set isAlerted true directly
            if result_top3accuracies[0] >= threshold:
                update_list = []
                #get monogodb data
                for upload_list in upload_lists.find({"image_path": result_imagepath}, {'_id': 0}):
                    update_list.append(upload_list['waiting_id'])

                # update mongodb
                for elem in update_list:
                    upload_lists.update_one({"waiting_id": int(elem)},{"$set":{"isAlerted": True}})

            #if low accuracy, write into db, waiting for future examination
            else:
                #TO-DO: still working on this part
                #get monogodb data
                # detected_object = detected_lists.find_one({"image_path": result_imagepath}, {'_id': 0})
                low_accuracy_object = low_accuracy_lists.find_one({"image_path": result_imagepath}, {'_id': 0})
                #prevent duplicate
                if low_accuracy_object:
                    continue

                else:
                    low_accuracy_lists.insert({'low_accuracy_id': low_accuracy_id, 'category': result_top3labels[0], 'threshold': threshold, 'image_path': result_imagepath, 'datetime': datetime.datetime.utcnow()})

            os.remove("result.pickle")

        # json_str = json.dumps([result_imagepath, result_top3labels, result_top3accuracies])
        json_str = json.dumps(problem_list)
        return json_str

    except Exception:
        return 'Error'


#helper function
def allowed_file_type(filename):
	return '.' in filename and filename.rsplit('.', 1)[-1] in ALLOWED_FILE_EXTENSIONS

def time_transform(transform_time):
    list_datetime = str(transform_time).split(',', 1)
    date = str(list_datetime)[2:12]
    return date

def label_transform(transform_label):
    label = str(transform_label)[2:-3]
    return label

def get_retrain_info():
    folderPath = os.path.join(RETRAIN_FOLDER)
    result = {'mattress': 0, 'tv monitor': 0, 'shopping cart': 0, 'couch': 0, 'clean': 0, 'chair': 0, 'refrigerator': 0}
    folder_file, folder_arr, count = [], [], 0
    for folder in os.listdir(folderPath):
        if not isfile(join(folderPath, folder)):
            folder_arr.append(folder)

    for folder in folder_arr:
        for file in os.listdir(os.path.join(folderPath, folder)):
            if folder == 'tv monitor':
                result['tv monitor'] += 1

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

            if folder == 'clean':
                result['clean'] += 1

            # folder_file.append(file)

    # json_str = json.dumps([count])
    return result


if __name__ == "__main__":
    app.run(debug=True)
