from flask import Flask, render_template, request
from threading import Thread
from werkzeug.utils import secure_filename


app = Flask('')


@app.route('/')
def upload_files():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save('images/' + secure_filename(f.filename))
      return 'Fichier importer avec succès'

def keep_alive():
  server = Thread(target=run)
  server.start()

def run():
  app.run(host="0.0.0.0", port=8000)


