from flask import Flask, request, render_template
from tkinter import Tk, messagebox, Button, Label
import threading
import requests
import os

app = Flask(__name__)
signatureType = ''
server_started = False
server_should_stop = False
own_pid = os.getpid()


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


@app.route('/stopServer', methods=['POST'])
def stop_server():
    global server_should_stop
    global own_pid
    server_should_stop = True
    os.kill(own_pid, 9)
    return 'Server stopped'


def start_server():
    global server_started
    server_started = True
    app.run(host="0.0.0.0", port=80, threaded=True)


def check_server_started():
    global server_started
    if server_started:
        messagebox.showinfo('Server Started', 'The server has started.')
    else:
        root.after(100, check_server_started)


def on_stopping():
    response = requests.post('http://localhost/stopServer')
    if response.status_code == 200:
        messagebox.showinfo('Server Stopped', 'The server has been stopped.')
    root.destroy()


if __name__ == '__main__':
    root = Tk()

    messagebox.showinfo('Server Starting', 'The server is starting...')

    threading.Thread(target=start_server).start()
    root.after(100, check_server_started)

    serverLabel = Label(root, text="The server has started. You can update Signature Type by opening http://IPaddr"
                                   "in a browser. \n Then you can use http://IPaddr/returnList to get a response")
    serverLabel.pack()
    stop_button = Button(root, text="Stop Server", command=on_stopping)
    stop_button.pack()

    infoLabel = Label(root, text="Note that the file with students should be in the same directory as your "
                                 "script/exe and should be named studentsList.csv", fg='red')
    infoLabel.pack()

    root.protocol("WM_DELETE_WINDOW", on_stopping)
    root.mainloop()
