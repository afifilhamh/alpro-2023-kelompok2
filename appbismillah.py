from flask import Flask, render_template, request
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import os

app = Flask(__name__)

base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, 'static', 'csv', 'HREmployee.csv')

# Load the dataset
df = pd.read_csv(data_path)
selected_columns = ['Age', 'Over18', 'Gender', 'MaritalStatus', 'Education',
                    'EducationField', 'NumCompaniesWorked', 'TotalWorkingYears',
                    'Department', 'MonthlyIncome', 'BusinessTravel',
                    'OverTime', 'JobRole']
df = df.loc[:, selected_columns]

label_encoders = {}

label_encoder = LabelEncoder()
for column in df.select_dtypes(include=['object']).columns:
    df[column] = label_encoder.fit_transform(df[column])
    label_encoders[column] = label_encoder

# Separate features and target
X = df.drop(['JobRole'], axis=1)
y = df['JobRole']

# Mendefinisikan nilai tukar mata uang (gunakan nilai yang sesuai dan terkini)
nilai_tukar_usd_to_idr = 15633.25
# Create the model
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

@app.route('/lihatrekomendasi', methods=["GET", "POST"])
def seeResult():
    global label_encoders  # Declare label_encoders as a global variable
    if request.method == 'POST':
        print(request.form)
        # Get data from the form
        form_data = {
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
            'Currency': request.form['currency'],
            'MonthlyIncome': int(request.form['salaryExpectation']),
            'BusinessTravel': request.form['businessTravel'],
            'OverTime': (request.form['overtime']),
        }

        # Convert MonthlyIncome from USD to IDR
        if form_data['Currency'] == 'IDR':
            form_data['MonthlyIncome'] /= nilai_tukar_usd_to_idr

        nama = form_data['Name']

        new_df = pd.DataFrame([form_data])
        new_df = new_df.drop(['Name', 'Currency'], axis=1)


        label_encoder = LabelEncoder()
        for column in new_df.select_dtypes(include=['object']).columns:
            print(column)
            label_encoders[column] = label_encoder  
            new_df[column] = label_encoders[column].fit_transform(new_df[column])


        overtime = form_data["OverTime"]
        totalYears = form_data['TotalWorkingYears']
        businessTravel = form_data['BusinessTravel']
        educationField = form_data['EducationField']

        # Predict the job position
        predicted_job_role = model.predict(new_df)

        # Decode the predicted label back to its original value
        prediction_real = label_encoders['JobRole'].inverse_transform(predicted_job_role)
        prediction = prediction_real[0]


        return render_template('lihatrekomendasi2.html', nama=nama, prediction=prediction, overtime=overtime, totalYears=totalYears, businessTravel=businessTravel, educationField=educationField)

@app.route('/')
def index():
    return render_template('halamanutama.html')

@app.route('/temukanpekerjaan')
def findJob():
    return render_template('formulir.html')

@app.route('/tentangkami')
def aboutUs():
    return render_template('tentangkami.html')

if __name__ == '__main__':
    app.run(debug=True)
