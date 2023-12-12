from flask import Flask, render_template, request
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import os

app = Flask(__name__)

base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, 'static', 'csv', 'HREmployee.csv')

# Load the dataset
df = pd.read_csv(data_path, names=['Age', 'Over18', 'Gender', 'MaritalStatus', 'Education', 
                                   'EducationField', 'NumCompaniesWorked','TotalWorkingYears', 
                                   'Department', 'MonthlyIncome','BusinessTravel', 
                                   'OverTime', 'JobRole'])

# Label encoding for categorical features
label_encoder = LabelEncoder()
for column in df.select_dtypes(include=['object']).columns:
    label_encoder = LabelEncoder()
    df[column] = label_encoder.fit_transform(df[column])

# One-hot encode categorical columns
categorical_columns = ['MaritalStatus', 'EducationField', 'Department', 'BusinessTravel']
df = pd.get_dummies(df, columns=categorical_columns)

# Ganti nilai 'Yes' menjadi 1 dan 'No' menjadi 0 pada kolom-kolom kategorik
df['Over18'] = df['Over18'].apply(lambda x: 1 if x == 'yes' else 0)
df['OverTime'] = df['OverTime'].apply(lambda x : 1 if x == 'yes' else 0)
df['Gender'] = df['Gender'].apply(lambda x : 1 if x == 'male' else 0)

# Separate features and target
X = df.drop(['JobRole'], axis=1)
y = df['JobRole'].values

# Create the model
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

@app.route('/lihatrekomendasi', methods=["GET", "POST"])
def seeResult():
    try:
        if request.method == 'POST':
            # Get data from the form
            form_data = {
                'Name': request.form['name'].title(),
                'Age': int(request.form['age']),
                'Over18': float(request.form['isAdult']),
                'Gender': float(request.form['gender']),
                'MaritalStatus': request.form['maritalStatus'],
                'Education': request.form['educationBackground'],
                'EducationField': request.form['educationField'],
                'NumCompaniesWorked': int(request.form['howManyCompanies']),
                'TotalWorkingYears': float(request.form['totalYears']),
                'Department': request.form['department'],
                'MonthlyIncome': int(request.form['salaryExpectation']),
                'BusinessTravel': request.form['businessTravel'],
                'OverTime': (request.form['overtime']),
            }

            # One-hot encode categorical columns
            form_data_encoded = pd.get_dummies(pd.DataFrame([form_data]))

            # Ensure the encoded form data has the same columns as training data
            form_data_encoded = form_data_encoded.reindex(columns=X.columns, fill_value=0)

            nama = form_data['Name'];
            overtime = form_data["OverTime"];
            totalYears = form_data['TotalWorkingYears'];
            businessTravel = form_data['BusinessTravel'];
            educationField= form_data['EducationField']

            # Predict the job position
            prediction = model.predict(form_data_encoded)[0]

            return render_template('lihatrekomendasi2.html', nama=nama, prediction=prediction, overtime=overtime, totalYears=totalYears, businessTravel=businessTravel, educationField=educationField)

    except Exception as e:
        return render_template('error.html', error=str(e))

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
