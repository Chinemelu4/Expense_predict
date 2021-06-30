from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('random_forest_loan_predict_model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        age = int(request.form['age'])
        children=int(request.form['children'])
        bmi=float(request.form['bmi'])
        Zone=request.form['Zone']
        if(Zone=='region_southeast'):
                region_southeast=1
                region_southwest=0
                region_northwest=0
                region_northeast=0
        if(Zone=='region_southwest'):
                region_southeast=0
                region_southwest=1
                region_northwest=0
                region_northeast=0
        if(Zone=='region_northwest'):
                region_southeast=0
                region_southwest=0
                region_northwest=1
                region_northeast=0
        else:
                region_southeast=0
                region_southwest=0
                region_northwest=0
                region_northeast=1 
        sex=request.form['sex']
        if(sex=='male'):
            sex_male=1
            sex_female=0
        else:
            sex_female=1
            sex_male=0
        smoker=request.form['smoker']
        if(smoker=='yes'):
            smoker_yes=1
            smoker_no=0
        else:
            smoker_no=1
            smoker_yes=0
        predictions=model.predict([[age,bmi,children,region_southeast,region_southwest,region_northwest,region_northeast,sex_male,sex_female,smoker_no,smoker_yes]])
        output=round(predictions[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot get a loan")
        else:
            return render_template('index.html',prediction_text="Expenditure is about ${}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)

