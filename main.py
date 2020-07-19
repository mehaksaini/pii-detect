import os
import sys

from flask import Flask, request, jsonify

from piiservice.piidetect import PiiDetect

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

app = Flask(__name__)


@app.route("/get", methods=['GET'])
def getpii():
    inputString = request.args.get('input')
    p = PiiDetect(inputString)
    return jsonify(indices=p.process_data())


if __name__ == '__main__':

    try:
        app.run(host='localhost', port=8090)

    except Exception:
        print('An error occurred')
