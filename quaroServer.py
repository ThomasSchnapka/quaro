__version__ = '1'
__author__ = 'Thomas Schnapka'

from flask import Flask, render_template, request
import quaroMain as main

#only log errors:
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
  
  
def quit():
    #Flask has no quit() method, that's why we have to send a request to our own server
    import requests
    requests.post('http://localhost:5000/shutdown')


@app.route('/')
def template():
    return render_template('basic.html')


@app.route('/get_up')
def get_up():
    main.control_thread("get_up")
    return "Bla"


@app.route('/get_down')
def get_down():
    main.control_thread("get_down")
    return "Bla"

@app.route('/toggle_phase')
def toggle_phase():
    main.change_value("phase")
    return "Bla"


@app.route('/start_demo')
def start_demo():
    main.control_thread("demo")
    return "Bla"


@app.route('/toggle_gait')
def toggle_gait():
    main.control_thread("toggle_gait")
    return "Bla"


@app.route('/dx/<amount>')
def dx(amount):
    main.change_value("rotation",amount)
    return "Bla"


@app.route('/dy/<amount>')
def dy(amount):
    main.change_value("stride_x",int(amount)/(-2))
    return "Bla"


@app.route('/shutdown', methods=['GET', 'POST'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    func()
    return "Shutting down..."
