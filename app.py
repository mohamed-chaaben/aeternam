from flask import Flask, render_template, request , redirect, url_for
import base64
import tensorflow as tf
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import io


app = Flask(__name__)
app.config['UPLOAD_PATH']='static'
model = tf.keras.models.load_model("model.h5")

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/colorize')
def colorize():
    return render_template("colorize.html")

@app.route('/colorize', methods=['POST'])
def upload_file():
    f = request.files['file']
    image1_b64 = base64.b64encode(f.read()).decode('utf-8')
    rgb_image = Image.open(f).resize( ( 120 , 120) )
        # Normalize the RGB image array
    gray_image = rgb_image.convert( 'L' )
    # Normalize the grayscale image array
    gray_img_array = ( np.asarray( gray_image ).reshape( ( 120 , 120 , 1 ) ) ) / 255
    x1=[]
    x1.append( gray_img_array )
    x2=np.array(x1)

    y = model( x2[ 0: ]  ).numpy()

    image = Image.fromarray( ( y[0] * 255 ).astype( 'uint8' ) ).resize( ( 1024 , 1024 ) )
    rawBytes = io.BytesIO()	
    image.save(rawBytes, "PNG")	
    rawBytes.seek(0)	
    image3_b64 = base64.b64encode(rawBytes.read()).decode('utf-8')


    return render_template("colorize.html", file1=image1_b64, file2=image3_b64)


if __name__ == '__main__':
    app.run(debug= True)