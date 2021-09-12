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
        Age = int(request.form['age'])

        # sex
        sex = request.form['Sex']
        if sex == 'Male':
            Sex = 1
        else:
            Sex = 0

        # Chest pain type
        chestpaintype = request.form['chestpaintype']
        if chestpaintype == 'ASY':
            cpt = 0
        elif chestpaintype == 'NAP':
            cpt = 1
        elif chestpaintype == 'ATA':
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
        if ecg == 'Normal':
            ECG = 0
        elif ecg == 'LVH':
            ECG = 1
        else:
            ECG = 2

        # heart_rate
        heart_rate = int(request.form['heartrate'])

        # exercise angima
        ex_angima = request.form['pain']
        if ex_angima == 'Yes':
            angima = 1
        else:
            angima = 0

        # oldpeak
        oldpeak = float(request.form['peak'])

        # st segment
        st_segment = request.form['st']
        if st_segment == 'Up':
            st = 1
        elif st_segment == 'Flat':
            st = 0
        else:
            st = 2

        prediction = model.predict([[
            Age,
            Sex,
            cpt,
            BP,
            Cholesterol,
            Sugar,
            ECG,
            heart_rate,
            angima,
            oldpeak,
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
