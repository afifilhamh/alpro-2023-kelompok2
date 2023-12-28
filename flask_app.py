from flask import Flask, render_template, request
import pandas as pd
from joblib import load
import os
app = Flask(__name__)
script_directory = os.path.dirname(os.path.realpath(__file__))
print(script_directory)

model_filename = os.path.join(script_directory, 'model3.joblib')

with app.app_context():
    model_filename = os.path.join(app.root_path, 'model3.joblib')

model = load(model_filename)


nilai_tukar_usd_to_idr = 15633.25


@app.route('/lihatrekomendasi', methods=["GET", "POST"])
def seeResult():
    if request.method == 'POST':
        label_encoders_filename = os.path.join(script_directory, 'encoders3.joblib')

        with app.app_context():
            label_encoders_filename = os.path.join(app.root_path, 'encoders3.joblib')

        # Load label encoders from the joblib file
        label_encoders = load(label_encoders_filename)
        # dapatkan input user dari form
        form_data = {
            'Name': request.form['name'].title(),
            'Age': int(request.form['age']),
            'Gender': request.form['gender'],
            'MaritalStatus': request.form['maritalStatus'],
            'Education': request.form['educationBackground'],
            'EducationField': request.form['educationField'],
            'NumCompaniesWorked': int(request.form['howManyCompanies']), #yang bisa dipakai buat machine learning
            'TotalWorkingYears': float(request.form['totalYears']), #yang bisa dipakai buat machine learning
            'Department': request.form['department'],
            'Currency': request.form['currency'],
            'MonthlyIncome': int(request.form['salaryExpectation']), #yang bisa dipakai buat machine learning
            'BusinessTravel': request.form['businessTravel'],
            'OverTime': (request.form['overtime']),
        }

        # Konvert MonthlyIncome dari USD to IDR
        if form_data['Currency'] == 'IDR':
            form_data['MonthlyIncome'] /= nilai_tukar_usd_to_idr
        # buat dataframe untuk data pengguna
        new_df = pd.DataFrame([form_data])
        nama = form_data['Name']

        #Menambahkan variabel baru sesuai usia, karena kalau kita tetap ambil dari form, nanti bermasalah saat ada yang pilih No krn di data train ga ada
        new_df['Over18'] = ''
        new_df.loc[new_df['Age'] > 18, 'Over18'] = 'Y'
        new_df.insert(new_df.columns.get_loc('Gender'), 'Over18', new_df.pop('Over18'))


        #encoding the input
        for column in new_df.select_dtypes(include=['object']).columns:
            if column in label_encoders:
                new_df[column] = label_encoders[column].transform(new_df[column])

        #untuk keperluan rasionalisasi
        overtime = form_data["OverTime"]
        totalYears = form_data['TotalWorkingYears']
        businessTravel = form_data['BusinessTravel']
        educationField = form_data['EducationField']

        #hapus variabel tidak perlu
        new_df = new_df.drop(['Name', 'Currency'], axis=1)
        print(new_df)


        # memprediksi (BISA DILIHAT MULAI DARI SINI AJA)
        predicted_job_role = model.predict(new_df)

        prediction = predicted_job_role[0]

        return render_template('lihatrekomendasi2responsive.html', nama=nama, prediction=prediction,
                               overtime=overtime, totalYears=totalYears, businessTravel=businessTravel,
                               educationField=educationField)



@app.route('/')
def index():
    return render_template('halamanutamaresponsive.html')

@app.route('/temukanpekerjaan')
def findJob():
    return render_template('formfix2.html')

@app.route('/tentangkami')
def aboutUs():
    return render_template('tentangkamiresponsive.html')

#if __name__ == '__main__':
    #app.run(debug=True)
