from flask import Flask, request, Response
import json
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
import urllib.request

app = Flask(__name__)
idx = None

initialized = False
def initialize():
    global idx
    link = "https://raw.githubusercontent.com/Maoni0/mem-doc/master/doc/.NETMemoryPerformanceAnalysis.md"
    f = urllib.request.urlopen(link)
    myfile = f.read()
    with open("./Input.md", 'wb') as wf:
        wf.write(myfile)
    loader = TextLoader('./Input.md', encoding='utf8')
    idx = VectorstoreIndexCreator().from_loaders([loader])

@app.route('/query', methods = ['POST'])
def index():

    if not initialized:
        initialize()

    rq = json.loads(request.data)
    if 'Query' not in rq:
        return Response("{\"Error\": \"Query must be provided in the payload.\" }", status = 401, mimetype= 'application/json')
    else:
        q = rq['Query'] 
        result = idx.query(q)
        return json.dumps(result)

if __name__ == '__main__':
    app.run(debug=True)