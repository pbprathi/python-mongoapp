from flask import Flask,jsonify,request
from pymongo import MongoClient

app=Flask(__name__)

#client=MongoClient(host="mongodb://127.0.0.1:27017")
#client=MongoClient("localhost","27017")
client = MongoClient('127.0.0.1', 27017)

db=client.testdb


#curl -i http://127.0.0.1:5000/tasks

@app.route('/tasks',methods=['GET'])
def get_tasks():
    task=db.task
    output=[]
    for t in task.find():
        output.append({'id':t['id'],'title':t['title'],'description':t['description'],'done':t['done']})

    return jsonify({'Results' : output}),200

#curl -i http://127.0.0.1:5000/task/1

@app.route('/task/<task_id>',methods=['GET'])
def get_task(task_id):
    task=db.task
    output=[]
    getdoc=task.find_one({'id':task_id})
    output={'id':getdoc['id'],'title':getdoc['title'],'description':getdoc['description'],'done':getdoc['done']}
    return jsonify({'Result':output}),200


#curl -i -X DELETE http://127.0.0.1:5000/task/1

@app.route('/task/<task_id>',methods=['DELETE'])
def del_task(task_id):
    task=db.task
    task.remove({'id':task_id})
    return jsonify({'Result': 'Task deleted'}),200

#curl -i -H "Content-Type: application/json" -X POST -d '{"id":"1","title":"Pay SBI EMI","description":"Pay by 1st of every month","done":"Not paid"}' http://127.0.0.1:5000/task

@app.route('/task',methods=['POST'])
def insert_task():
    task=db.task
    output=[]
    insobjid= task.insert({'id':request.json['id'],
    'title':request.json['title'],
    'description':request.json['description'],
    'done':request.json['done']})
    inserted_doc= task.find_one({'_id':insobjid})
    output={'id':inserted_doc['id'],'title':inserted_doc['title'],
    'description':inserted_doc['description'],'done':inserted_doc['done']}
    return jsonify({'results':output}),200

#curl -i -H "Content-Type: application/json" -X PUT -d '{"id":"1","title":"Pay SBI RJY EMI","description":"Pay by 1st of every month","done":"Not paid"}' http://127.0.0.1:5000/task/1

@app.route('/task/<task_id>',methods=['PUT'])
def update_task(task_id):
    task=db.task
    output=[]
    task_exist=task.find_one({'id':task_id})
    if task_exist:
        task.update({'id':task_id},{'id':task_id,'title':request.json['title'],'description':request.json['description'],'done':request.json['done']})
        updated_task=task.find_one({'id':task_id})
        output={'id':updated_task['id'],'title':updated_task['title'],'description':updated_task['description'],'done':updated_task['done']}
    else:
        task.insert({'id':task_id,'title':request.json['title'],'description':request.json['description'],'done':request.json['done']})
        inserted_task=task.find_one({'id':task_id})
        output={'id':inserted_task['id'],'title':inserted_task['title'],'description':inserted_task['description'],'done':inserted_task['done']}
    return jsonify({'Result':output}),200


if __name__ == '__main__':
    app.run(debug=True)
