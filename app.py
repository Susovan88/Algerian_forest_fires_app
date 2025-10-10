from flask import Flask,render_template,request,jsonify,redirect,url_for
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

application=Flask(__name__)
app=application

## import models 
lasso_model=pickle.load(open('models/lasso.pkl','rb'))   ## predict output
std_scaler=pickle.load(open('models/scaler.pkl','rb'))   ## feature scaling 
efs_model=pickle.load(open('models/efs.pkl','rb'))  ## for feature selection

@app.route('/')
def index():
    return redirect(url_for('predict'))


@app.route('/predict',methods=['GET','POST'])
def predict():
    if request.method=='POST':
        Temperature=float(request.form.get('Temperature'))
        RH=float(request.form.get('RH'))
        Ws=float(request.form.get('Ws'))
        Rain=float(request.form.get('Rain'))
        FFMC=float(request.form.get('FFMC'))
        DMC=float(request.form.get('DMC'))
        ISI=float(request.form.get('ISI'))
        Classes=float(request.form.get('Classes'))
        Region=float(request.form.get('Region'))

        ## feature scaling
        features=std_scaler.transform([[Temperature,RH,Ws,Rain,FFMC,DMC,ISI,Classes,Region]])
        ## feature selection using efs
        filter_features=efs_model.transform(features)
        ##predict
        output=lasso_model.predict(filter_features)
        return render_template('home.html',results=output[0])

    else:
        return render_template('home.html')
    
if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True)

    
