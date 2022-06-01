from threading import main_thread
from numpy import argmax
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from keras.models import load_model
from pip import main
 
# load and prepare the image
class Digit:
    @staticmethod
    def load_image(filename):
        # load the image
        img = load_img(filename, grayscale=True, target_size=(28, 28))
        # print(img)
        # convert to array
        img = img_to_array(img)
        # reshape into a single sample with 1 channel
        img = img.reshape(1, 28, 28, 1)
        # prepare pixel data
        img = img.astype('float32')
        img = img / 255.0
        return img
    
    # load an image and predict the class
    @staticmethod
    def predict(imag):
        # load the image
    #   imag='/content/gdrive/My Drive/sample_image_red.png'
        img = Digit.load_image(imag)
        # load model
        model = load_model('models\Final_model.h5')
        # predict the class
        predict_value = model.predict(img)
        digit = argmax(predict_value)
        # print(type(imag.split('.')[0]),imag.split('.')[-2])
        acc = 1 if int(digit) == int(imag.split('.')[-2][-1]) else 0
        return digit, acc
    
# if __name__ =="__main__":
#     app = Digit()
#     x,y= app.predict('images\digit\\3.png')
#     print(x,y)
# image = cv2.imread('sample_image_1.png')
# print(image)