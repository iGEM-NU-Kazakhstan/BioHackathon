from flask import Flask,render_template
from flask import request
from flask import jsonify
import string
import random
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/request', methods = ['POST'])
def request_query():
    if request.method == 'POST':
        data = request.form # a multidict containing POST data
        letters = string.ascii_lowercase
        random_str = ''.join(random.choice(letters) for i in range(10))
        dna_file = random_str + "dna.txt"
        restrictions_file = random_str + "restrictions.txt"
        output_file = random_str + "output.txt"
        f = open(dna_file, "w")
        f.write(data.get('dna'))
        f.close()
        f = open(restrictions_file, "w")
        f.write(data.get('restrictions').replace('\r', ''))
        f.close()
        stream = os.popen('./a.out ' + " ".join([dna_file, output_file, restrictions_file]))
        output = stream.read()
        print(output)
        f = open(output_file, "r")
        data = jsonify({"data": f.read().split("\n")})
        os.remove(output_file)
        os.remove(dna_file)
        os.remove(restrictions_file)
        return data

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
