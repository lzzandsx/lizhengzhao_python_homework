from flask import Flask,request
from pymongo import MongoClient
from flask import jsonify
from flask import render_template


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def index():
    return 'welcome'

@app.route('/article_list/',methods=['GET','POST'])
def article_list():

    if request.method == 'POST':
        num = int(request.form.get('post'))
        client = MongoClient('mongodb://localhost:27017')
        database = client.xinlang
        collection = database.articles
        id = collection.find().count()-1
        if id<0:
            return '并无收录的文章'
        data = []
        for i in range((num-1)*10,num*10):
            if id-i<0:
                break
            result = collection.find_one({'Id':id-i})
            article = {
                'title':result['title'],
                'date':result['date'],
                'id':result['Id'],
            }
            data.append(article)
        return jsonify({'data':data})
    else:
        return render_template('post.html')


@app.route('/article_detail/',methods=['GET','POST'])
def arricle_detail():

    if request.method == 'POST':
        id = int(request.form.get('id'))


        client = MongoClient('mongodb://localhost:27017')
        database = client.xinlang
        collection = database.articles
        if id>=collection.find().count():
            return jsonify({})

        result = collection.find_one({'Id':id})
        output = {
            'title':result['title'],
            'date':result['date'],
            'content':result['content'],
            'url':result['url'],
        }
        return jsonify(output)
    else:
        return render_template('post_id.html')

if __name__ == '__main__':
    app.run(debug=True)

