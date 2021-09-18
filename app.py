from flask import Flask, request, render_template
from flask_cors import cross_origin
import pickle

app = Flask(__name__)
model = pickle.load(open("heart_risk.pkl", "rb"))


@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")


@app.route("/predict", methods=["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":

        # age
        age = int(request.form['age'])

        # sex
        sex = request.form['Sex']
        if sex == 'male':
            Sex = 1
        else:
            Sex = 0

        # Chest pain type
        chestpaintype = request.form['chestpaintype']
        if chestpaintype == 'asymptomatic':
            cpt = 0
        elif chestpaintype == 'non-anginal_pain':
            cpt = 1
        elif chestpaintype == 'atypical_angina':
            cpt = 2
        else:
            cpt = 3

        # bp
        BP = int(request.form['bp'])

        # cholesterol
        Cholesterol = int(request.form['cholesterol'])

        # blood_sugar
        sugar = int(request.form['sugar'])
        if sugar > 120:
            Sugar = 1
        else:
            Sugar = 0

        # ECG
        ecg = request.form['ecg']
        if ecg == 'normal':
            ECG = 0
        elif ecg == 'lvh':
            ECG = 1
        else:
            ECG = 2

        # heart_rate
        heart_rate = int(request.form['heartrate'])

        # exercise angima
        ex_angima = request.form['pain']
        if ex_angima == 'yes':
            angima = 1
        else:
            angima = 0

        # st segment
        st_segment = request.form['st']
        if st_segment == 'up':
            st = 1
        elif st_segment == 'flat':
            st = 0
        else:
            st = 2

        prediction = model.predict([[
            age,
            Sex,
            cpt,
            BP,
            Cholesterol,
            Sugar,
            ECG,
            heart_rate,
            angima,
            st
        ]])

        output = prediction[0]
        if output == 0:
            return render_template('home.html', prediction_text="Heart disease possibility is less")
        else:
            return render_template('home.html', prediction_text="Heart disease possibility is more")

    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True, port=9999)
