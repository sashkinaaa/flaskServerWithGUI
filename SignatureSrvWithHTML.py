from flask import Flask, request, render_template

app = Flask(__name__)
signatureType = ''


@app.route('/updateSignatureType', methods=['POST'])
def update_signature_type():
    global signatureType
    signatureType = request.form.get('signatureType')  # Get the value of the 'signatureType' parameter
    return 'Signature Type updated successfully to: ' + str(signatureType) + \
        ', now you can use http://IPaddr/returnList in browser to test or you can send the get request from the system'


@app.route('/returnList', methods=['GET'])
def get_numbers():
    numbers = []
    with open('studentsList.csv', 'r') as f:
        for line in f:
            numbers.append(line.strip())

    response = ','.join([signatureType + '[' + number + ']' for number in numbers])
    return response


@app.route("/")
def main():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
