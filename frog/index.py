import json
import base64
from database import *
from util import *
import mysql.connector
from flask import Flask,request
app = Flask(__name__)

imgs_info = None

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/getImg', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
        tagList = data['desc']
        #data = ['1','2','3']
        #TODO
        tmp = []
        for item in tagList:
            tag = item.split(' ')
            for tag_item in tag:
                tmp.append(tag_item)
        tagList = tmp

        data = main(tagList)

        data = [base64.b64decode(d) for d in data]
        result = []
        for d in data:
            result.append("http://139.198.189.135:5000/static/pictures/"+d)
        return json.dumps(result)
    else:
        pass
    return 'it works'

def main(tagList):
    # initial database
    config = {
        'user': 'root',
        'password': '123456',
        'host': 'localhost',
        'port': 3306,
        'database': 'compose',
    }
    connect = mysql.connector.connect(**config)
    cur = connect.cursor()
    
    if imgs_info==None:
        imgs_info = getAll(cur)

    scores = getScore(imgs_info, tagList)

    thrd = np.max(scores)*0.3
    for i in range(len(imgs_info)):
        imgs_info[i].append(scores[i])

    res_img = sorted(imgs_info,key=lambda x:-x[3])
    for i in range(max(3,len(imgs_info))):
        print(imgs_info[i][2])
    final_res = []
    cnt = 0
    for item in res_img:
        if item[3]>=thrd and cnt<4:
            final_res.append(item[1])
        cnt += 1



    connect.commit() 
    connect.close()

    return final_res

if __name__ == '__main__':
    app.run(host='0.0.0.0')

