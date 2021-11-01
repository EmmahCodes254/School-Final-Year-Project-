import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

#procfile.txt 
#web: gunicorn app:app
#first file that we have to run first : flask server name
app = Flask(__name__)
pkl_file = open('model.pkl','rb')
model = pickle.load(open('model.pkl', 'rb'))
index_dict = pickle.load(pkl_file)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST', "GET"])
def predict():

    if request.method=='POST':
        result = request.form

        index_dict = pickle.load(open('cat','rb'))
        location_cat = pickle.load(open('location_cat','rb'))

        new_vector = np.zeros(151)

        result_location = result['location']

        if result_location not in location_cat:
            new_vector[146] = 1
        else:
            new_vector[index_dict[str(result['location'])]] = 1


        new_vector[index_dict[str(result['area'])]] = 1

        new_vector[0] = result['sqft']
        new_vector[1] = result['bath']
        new_vector[2] = result['balcony']
        new_vector[3] = result['size']

    new = [new_vector]

    prediction = model.predict(new)
    #print(prediction)

    return render_template('index.html', Predict_score ='Your house estimate price is Kenyan Shilling {} millions'.format(prediction))

if __name__ == "__main__":
    app.run(debug=True)
