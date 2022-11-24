# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from flask import Flask, request, render_template
import joblib
from sklearn.preprocessing import Normalizer
import datetime
app = Flask(__name__)

model = joblib.load("finalized_model5.sav")

df = pd.DataFrame()

@app.route('/')
def home():
    # print(np.__version__)
    return render_template('form.html')

@app.route('/predict',methods=['POST'])
def predict():
    dictionary = {}
    global df
    # fig, axs = plt.subplots(2, 2, figsize=(15, 6), facecolor='w', edgecolor='k')
    # fig.subplots_adjust(hspace=.5, wspace=.001)
    # axs = axs.ravel()
    input_features = []
    for x in request.form.values():
        # print(x)
        input_features.append(x)
    if len(input_features)==4:
        input_features.append(0)
    # print(input_features)
    minutes_range = list(range(0, 60, 15))
    month_num = (input_features[0][5:7])
    datetime_object = datetime.datetime.strptime(month_num, "%m")
    month_name = datetime_object.strftime("%b")
    print("Short name: ",month_name)
    print(" " * 35, "Month Name is", month_name)

    for n, minute in enumerate(minutes_range):

        output = []

        input = Normalizer().fit_transform([[int(input_features[0][0:4]), int(input_features[0][5:7]), int(input_features[0][8:10]), int(input_features[-2]), int(input_features[1]), minute, 0, input_features[-1]]])
        #         print(input)

        output = model.predict_proba(input)
        starting_time = int(input_features[1])
        #         print()
        #         print(output[0][0])
        #         print(output[0][1])
        data = [round(output[0][0],2), round(output[0][1],2)]
        label = ['No', 'Yes']
        x = n
        # plt.subplot(2, 2,x )
        # axs[x].pie(data, labels=label, autopct='%1.1f%%', shadow=True, startangle=90)
        if n == 0:
            l = ["" * 15, starting_time, ":0", minute + 1, "to", starting_time, ":", minute + 15, "" * 15]
        elif n == 3:
            l = ["" * 15, starting_time, ":", minute + 1, "to", starting_time + 1, ":", "00", "" * 15]

        else:
            l = ["" * 15, starting_time, ":", minute + 1, "to", starting_time, ":", minute + 15, "" * 15]
        # #         axs[n].contourf(np.random.rand(10,10),5,cmap=plt.cm.Oranges)
        print(l)
        print(data[0], data[1])
        values =[]
        values.append(data[0])
        values.append(data[1])
        dictionary[starting_time, ":", minute + 1, "to", starting_time, ":", minute + 15]=values
        # axs[x].set_title(str("  ".join(map(str, l))))
        # plt.title('parking')
        # plt.axis('equal')
        # plt.show()

    # input_features = [int(x) for x in request.form.values() if type(x)==]
    # features_value = np.array(input_features)
    
    #validate input hours
    # if input_features[0] <0 or input_features[0] >24:
    #     return render_template('form.html', prediction_text='Please enter valid hours between 1 to 24 if you live on the Earth')
    #
    #
    # output = model.predict([features_value])[0][0].round(2)

    # input and predicted value store in df then save in csv file
    # df= pd.concat([df,pd.DataFrame({'Study Hours':input_features,'Predicted Output':[output]})],ignore_index=True)
    # print(df)
    # df.to_csv('smp_data_from_app.csv')

    return render_template('index.html',items= dictionary.keys(), Dictionary=dictionary)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
    