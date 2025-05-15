from flask import Flask, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)

# Load your trained model (ensure the path is correct)
with open('loaded_models/XGB_Model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)
with open('loaded_models/label_encoder.pkl','rb') as model_file:
    label_encoder = pickle.load(model_file)


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
        predictions = model.predict(X)

        # Add predictions to DataFrame
        df['Prediction'] = label_encoder.inverse_transform(predictions)

        # Convert DataFrame to HTML
        result_html = df.to_html(classes='table table-bordered', index=False)
        return render_template('index.html', table=result_html)

    except Exception as e:
        return f"Error during prediction: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
