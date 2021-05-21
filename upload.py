import os      
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from threading import Thread 
import requests
app=Flask(__name__)
app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 * 1024

# Get current path
path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'images')

# Make directory if uploads is not exists
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['images/'] = UPLOAD_FOLDER

# Allowed extension you can set your own
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','mp4','3g2','3gp','asf','asx','avi','flv','mkv','mov','mp4','mpg','ogv','rm','swf','vob','wmv','webm'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/dialogflow')
def render_dialogflow():
    return render_template('dialogflow.html')

@app.route('/uploader', methods=['POST','GET'])
def upload_file():
    if request.method == 'POST':

        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['images/'], filename))

        flash('File(s) successfully uploaded')
        return redirect('/')

@app.route('/webhook', methods=['POST'])
def webhook():
  req = request.get_json(silent=True, force=True)
  #print(req)
  fulfillmentText = ''
  sum = 0
  query_result = req.get('queryResult')

  if query_result.get('action') == 'input.unknown':
    print(fulfillmentText)
  elif query_result.get('intent').get('displayName') == 'add.numbers':
    num1 = int(query_result.get('parameters').get('number'))
    num2 = int(query_result.get('parameters').get('number1'))
    sum = str(num1 + num2)
    fulfillmentText = 'Cela fais '+sum

  elif query_result.get('intent').get('displayName') == 'weather':
    if len(query_result.get('parameters').get('date-time')) == 0 :
      city = str(query_result.get('parameters').get('address').get('city'))
      weather_request = requests.get('http://api.weatherstack.com/current?access_key=776371bf2940f65f32dc34dfc74795ea&query='+city)
      weather_final = weather_request.json()
      temp = str(weather_final.get('current').get('temperature'))
      fulfillmentText = 'La Temperature actuel à '+ city +' est de '+temp+'℃'
      print(fulfillmentText)
    else:
      fulfillmentText = 'Je ne peut malheureusement pas encore de dire la météo de demain' 
      print(fulfillmentText)
  elif query_result.get('intent').get('displayName') == 'multiply.numbers':
    num1 = int(query_result.get('parameters').get('number'))
    num2 = int(query_result.get('parameters').get('number1'))
    sum = str(num1 * num2)
    fulfillmentText = 'Cela fais '+sum
  return {
        "fulfillmentText": fulfillmentText,
        "source": "webhookdata"
    }

def keep_alive():
  server = Thread(target=run)
  server.start()
def run():
  app.run(host="0.0.0.0", port=8000)
