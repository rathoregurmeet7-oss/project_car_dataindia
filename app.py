import os
import uuid
from flask import Flask, jsonify, render_template, request
from model import predict_car_model
import pandas as pd
import requests
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load car data
df = pd.read_csv('car_data_india.csv')


# Optional: Safety rating via NHTSA API (U.S. only)
def get_safety_rating(model):
  try:
    url = f'https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/{model}?format=json'
    response = requests.get(url, timeout=5)
    data = response.json()
    return 'Available' if data.get('Count', 0) > 0 else 'Not available'
  except Exception:
    return 'Not available'


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
  if 'car_image' not in request.files:
    return jsonify({'error': 'No car image file uploaded.'}), 400

  image = request.files['car_image']
  if image.filename == '':
    return jsonify({'error': 'No selected file.'}), 400

  unique_filename = f'{uuid.uuid4().hex}_{secure_filename(image.filename)}'
  image_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
  image.save(image_path)

  try:
    model_name = predict_car_model(image_path)
  finally:
    # Always clean up uploaded file even if prediction fails
    if os.path.exists(image_path):
      try:
        os.remove(image_path)
      except Exception as e:
        print(f'Error deleting file: {e}')

  if not model_name:
    return jsonify({'error': 'Car model could not be identified.'})

  return get_car_info(model_name)


def get_car_info(model_name):
  car = df[df['Model'].astype(str).str.lower() == model_name.lower()]
  if car.empty:
    return jsonify(
        {'available': False, 'message': f'{model_name} is not sold in India.'}
    )

  car_row = car.iloc[0]

  # Helper functions to handle numerical conversions safely
  def safe_int(val):
    try:
      return int(pd.to_numeric(val, errors='coerce'))
    except (ValueError, TypeError):
      return 0

  def safe_float(val):
    try:
      return float(pd.to_numeric(val, errors='coerce'))
    except (ValueError, TypeError):
      return 0.0

  info = {
      'available': str(car_row.get('IsAvailable', '')).strip().lower() == 'yes',
      'Model': str(car_row.get('Model', '')),
      'Brand': str(car_row.get('Brand', '')),
      'Engine': str(car_row.get('Engine', '')),
      'Mileage': safe_int(car_row.get('Mileage', 0)),
      'Speciality': str(car_row.get('Speciality', '')),
      'Price': safe_int(car_row.get('Price (INR)', 0)),
      'Discount': safe_float(car_row.get('Discount', 0.0)),
      'Headquarter': str(car_row.get('Headquarter', '')),
  }

  return jsonify(info)


if __name__ == '__main__':
  app.run(debug=True)