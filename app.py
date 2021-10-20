import uuid
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os
from app_helper import *

# Define a flask app
app = Flask(__name__)
ALLOWED_EXT = set(['jpg','jpeg','png'])
def allowed_file(filename):
    return '.'in filename and \
            filename.rsplit('.',1)[1] in ALLOWED_EXT

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/uploader', methods = ['POST'])
def upload_file():
    error = ""
    basepath = os.path.dirname(__file__)

    if request.method == 'POST':
        if (request.files):
            f = request.files['file']
            if f and allowed_file(f.filename):
                file_path = os.path.join(basepath, 'static', 'uploads', secure_filename(f.filename))
                f.save(file_path)
                file_name = Image.open(file_path)
                pred,img = predict_image(file_name)
            else:
                error = "Please upload images of jpg, jpeg and png extensions only"
            if (len(error) == 0):
                return render_template('upload.html', predictions=pred,display_image=f.filename, similar_images=img)
            else:
                return render_template('index.html', error=error)
        elif (request.form):
            link = request.form.get('link')
            try:
                resource = urllib.request.urlopen(link)
                unique_filename = str(uuid.uuid4())
                file = unique_filename + ".jpg"
                file_path = os.path.join(basepath, 'static', 'uploads', secure_filename(file))
                output = open(file_path , "wb")
                output.write(resource.read())
                output.close()
                file_name = Image.open(file_path)
                pred,img = predict_image(file_name)
            except Exception as e:
                print(str(e))
                error = 'This image from this site is not accessible or inappropriate input'
            if (len(error) == 0):
                return render_template('upload.html', predictions=pred,display_image=file, similar_images=img)
            else:
                return render_template('index.html', error=error)
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
