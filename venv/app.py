from flask import Flask,render_template,request
from elasticsearch import Elasticsearch
import json
app = Flask(__name__)
es=Elasticsearch()
@app.route('/',methods=["GET","POST"])
def index():
    #q = request.args.get("q")
    q = request.form.get("q")
    data=[]
    if q is not None:
        resp=es.search(index='flickrphotos',body={"query":{"fuzzy":{"tags":{"value":q,
                                                                            "fuzziness":4}}}})
        result = resp['hits']['hits']
        for i in range(len(resp['hits']['hits'])):
            str = "http://farm" + result[i]['_source']['flickr_farm'] + ".staticflickr.com/" + result[i]['_source']['flickr_server'] + "/" + result[i]['_source']['id'] + "_" + result[i]['_source']['flickr_secret'] + ".jpg";
            data.append(str)


        return render_template("index.html",q=q, response=data)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True,port=8000)
