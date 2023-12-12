from flask import Flask, render_template, request
import pandas as pd
import random


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('halamanutama.html')

@app.route('/temukanpekerjaan')
def findJob():
    return render_template('formulir.html')

@app.route('/lihatrekomendasi', methods=["GET", "POST"])
def seeResult():
    if request.method == 'POST':
        data = {
            'Name': request.form['name'].title(),
            'Age': int(request.form['age']),
            'Over18': request.form['isAdult'],
            'Gender': request.form['gender'],
            'MaritalStatus': request.form['maritalStatus'],
            'Education': request.form['educationBackground'],
            'EducationField': request.form['educationField'],
            'NumCompaniesWorked': int(request.form['howManyCompanies']),
            'TotalWorkingYears': float(request.form['totalYears']),
            'Department': request.form['department'],
            'MonthlyIncome': int(request.form['salaryExpectation']),
            'BusinessTravel': request.form['businessTravel'],
            'OverTime': request.form['overtime'],
        }

        hasil_data = {key: [value] for key, value in data.items() if key != 'Name'}
        hasil_df = pd.DataFrame(hasil_data)

        nama = data['Name'];
        overtime = data["OverTime"];
        totalYears = ['TotalWorkingYears'];
        businessTravel = ['BusinessTravel'];
        educationBackground = ['Education']

        job_positions = [
            "Sales Executive",
            "Research Scientist",
            "Laboratory Technician",
            "Manufacturing Director",
            "Healthcare Representative",
            "Manager",
            "Sales Representative",
            "Research Director",
            "Human Resources"
        ]

        prediction = random.choice(job_positions) #untuk testing html maka ini dirandom dulu, tapi nanti tologn diganti dengan modelnya

        return render_template('lihatrekomendasi.html', nama=nama, prediction=prediction, overtime=overtime, totalYears=totalYears, businessTravel=businessTravel, educationBackground=educationBackground)

@app.route('/tentangkami')
def aboutUs():
    return render_template('tentangkami.html')

if __name__ == '__main__':
    app.run(debug=True)
