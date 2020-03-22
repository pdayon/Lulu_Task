import os
import pdftotext
from flask import Flask, request, render_template, send_from_directory
file = open("master.txt","w+")
app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload():

    target = os.path.join(APP_ROOT,"PDFs")
    if not os.path.isdir(target):
        os.mkdir(target)
    
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        destination = "/".join([target, filename])
        upload.save(destination)
    PDF(destination)
    

    # return send_from_directory("images", filename, as_attachment=True)
    return render_template("complete.html", image_name=filename)

def PDF(filename):
    with open(filename, "rb") as f:
        pdf = pdftotext.PDF(f)
    print("\n\n".join(pdf))
    file.write("\n\n".join(pdf)) 
    file.close()

if __name__ == "__main__":
    app.run(port=4555, debug=True)

