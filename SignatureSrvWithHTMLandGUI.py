from flask import Flask, request, render_template
from tkinter import Tk, messagebox, Button
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
    return 'Server stop request received'


def start_server():
    global server_started
    global server_should_stop

    server_started = True
    app.run(host="0.0.0.0", port=80, threaded=True)


def check_server_started():
    global server_started
    if server_started:
        messagebox.showinfo('Server Started', 'The server has started.')
    else:
        root.after(100, check_server_started)


def stop_button_click():
    response = requests.post('http://localhost/stopServer')
    if response.status_code == 200:
        messagebox.showinfo('Server Stopped', 'The server has been stopped.')


def on_closing():
    requests.post('http://localhost/stopServer')
    root.destroy()


if __name__ == '__main__':
    root = Tk()

    messagebox.showinfo('Server Starting', 'The server is starting...')

    threading.Thread(target=start_server).start()
    root.after(100, check_server_started)

    stop_button = Button(root, text="Stop Server", command=stop_button_click)
    stop_button.pack()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
