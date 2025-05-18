from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import pickle

app = Flask(__name__)

def CNNModel(df):
    with open('loaded_models/cnn_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    with open('loaded_models/cnn_scaler.pkl', 'rb') as model_file:
        scaler = pickle.load(model_file)
    normalized_df = scaler.transform(df)
    prediction = model.predict(normalized_df)
    predicted_index = np.argmax(prediction,axis=1)
    label = ['Attack', 'Benign', 'C&C', 'C&C-FileDownload', 'C&C-HeartBeat', 'C&C-HeartBeat-FileDownload', 'C&C-Mirai', 'C&C-Torii', 'DDoS', 'FileDownload', 'Okiru', 'PartOfAHorizontalPortScan']
    predicted_label = label[predicted_index[0]]
    return predicted_label

def NaiveBayes(df):
    with open('loaded_models/naive_bayes_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    return model.predict(df)

def DecisionTree(df):
    with open('loaded_models/XGB_Model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    with open('loaded_models/label_encoder.pkl', 'rb') as model_file:
        label_encoder = pickle.load(model_file)
    return label_encoder.inverse_transform(model.predict(df))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'csv_file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['csv_file']
    if file.filename == '':
        return 'No selected file', 400

    try:
        df = pd.read_csv(file)

        # Ensure the column order and names match what the model expects
        feature_columns = ['duration', 'orig_bytes', 'resp_bytes', 'missed_bytes',
                           'orig_pkts', 'orig_ip_bytes', 'resp_pkts', 'resp_ip_bytes',
                           'proto_icmp', 'proto_tcp', 'proto_udp',
                           'conn_state_OTH', 'conn_state_REJ', 'conn_state_RSTO',
                           'conn_state_RSTOS0', 'conn_state_RSTR', 'conn_state_RSTRH',
                           'conn_state_S0', 'conn_state_S1', 'conn_state_S2', 'conn_state_S3',
                           'conn_state_SF', 'conn_state_SH', 'conn_state_SHR']

        # Filter the required features
        X = df[feature_columns]

        # Predict using the loaded model
        predictions = DecisionTree(X)

        # Add predictions to DataFrame
        df['Prediction'] = predictions

        # Convert DataFrame to HTML
        result_html = df.to_html(classes='table table-bordered', index=False)
        return render_template('index.html', table=result_html)

    except Exception as e:
        return f"Error during prediction: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
