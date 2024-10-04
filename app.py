from flask import Flask, render_template, url_for, request
import os,joblib,sqlite3
from tensorflow.keras.models import load_model #type: ignore

model = load_model('./models/loan_approval.h5')
std_scaler = joblib.load('./models/std_scaler.lb')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict',methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        dependents = int(request.form['dependents'])
        income = float(request.form['income'])
        loan_amount = float(request.form['loan_amount'])
        loan_term = int(request.form['loan_term'])
        cibil_score = float(request.form['cibil_score'])
        residential_assets_value = float(request.form['residential_assets_value'])
        commercial_assets_value = float(request.form['commercial_assets_value'])
        luxury_assets_value = float(request.form['luxury_assets_value'])
        bank_asset_value = float(request.form['bank_asset_value'])
        education = int(request.form['education'])
        self_employed = int(request.form['self_employed'])

        UNSEEN_DATA = [[dependents,income,loan_amount,loan_term,cibil_score,\
                        residential_assets_value,commercial_assets_value,\
                        luxury_assets_value,bank_asset_value,education,\
                        self_employed]]
        
        x_transformed = std_scaler.transform(UNSEEN_DATA)
        prediction = model.predict(x_transformed)[0][0]
        # ANN model will give prediction in probability
        pred = (prediction > 0.5).astype(int)

        pred_dict = {1:'Rejected',0:'Approved'}
        result = pred_dict[pred]

        # Insert data into database
        conn = sqlite3.connect('loan_approval.db')
        cur = conn.cursor()

        query_to_execute = """
            insert into client_details values(?,?,?,?,?,?,?,?,?,?,?,?)
        """

        education_dict = {1:'Not Graduate',0:'Graduate'}
        self_employed_dict = {1:'Yes',0:'No'}

        data = [dependents,income,loan_amount,loan_term,cibil_score,\
                residential_assets_value,commercial_assets_value,\
                luxury_assets_value,bank_asset_value,education_dict[education],\
                self_employed_dict[self_employed],result]

        cur.execute(query_to_execute,data)
        conn.commit()
        print('YOUR RECORD HAVE BEEN STORED IN OUR DATABASE')
        cur.close()
        conn.close()


        return render_template('output.html',output = result)


if __name__ == '__main__':
    app.run(debug=True)