from PIL import Image
from tensorflow.keras.preprocessing.image import load_img , img_to_array
import io

ALLOWED_EXT = set(['jpg' , 'jpeg' , 'png' , 'jfif'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXT



def model_predict(file , model):
    contents = file.file.read()
    img = load_img(io.BytesIO(contents), target_size=(224, 224))
    img = img_to_array(img)
    img = img.reshape(1 , 224 ,224 ,3)

    img = img.astype('float32')
    img = img/255.0
    result = model.predict(img)

    if result[0][0]>=0.5:
        prediction = "Real"
        confidence = round(float(result[0][0]*100),2)
    elif result[0][0]<0.5:
        prediction = "Fake"
        confidence = 100- round(float(result[0][0]*100),2)
    else:
        prediction="unknown"
        confidence = "unknown"

    return prediction, confidence, result