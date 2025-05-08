from flask import Flask, render_template, request
import google.generativeai as genai
import requests

app = Flask(__name__)

genai.configure(api_key="AIzaSyBEgp4Z0nZEe5soW-gTQe-WxqyvO6LE6i0")

regions = {
    'North': ['Chandigarh', 'Delhi', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir',
              'Ladakh', 'Punjab', 'Rajasthan', 'Uttarakhand', 'Uttar Pradesh'],
    'South': ['Andaman and Nicobar Islands', 'Andhra Pradesh', 'Karnataka', 'Kerala',
              'Lakshadweep', 'Puducherry', 'Tamil Nadu', 'Telangana'],
    'East': ['Bihar', 'Jharkhand', 'Odisha', 'West Bengal', 'Arunachal Pradesh',
             'Assam', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Sikkim', 'Tripura'],
    'West': ['Chhattisgarh', 'Dadra and Nagar Haveli and Daman and Diu', 'Goa',
             'Gujarat', 'Maharashtra', 'Madhya Pradesh']
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/region')
def region():
    return render_template('region.html', regions=regions.keys())

@app.route('/state', methods=['POST'])
def state():
    selected_region = request.form['region']
    states = regions[selected_region]
    return render_template('state.html', region=selected_region, states=states)

@app.route('/interest', methods=['POST'])
def interest():
    selected_state = request.form['state']
    return render_template('interest.html', state=selected_state)

@app.route('/result', methods=['POST'])
def result():
    state = request.form['state']
    interest = request.form['interest']

    model = genai.GenerativeModel(model_name="gemini-2.0-flash")
    prompt = f"""
Suggest exactly 10 beautiful travel destinations in {state} suitable for someone who loves {interest}.
For each place, give in this exact format without any extra line:
Place Name: A short 3-4 line beautiful description about that place.
No numbering. No headings. No introduction or conclusion. Just the 10 places and their info.
"""

    response = model.generate_content(prompt)

    if response and response.text:
        places = [line.strip() for line in response.text.split('\n') if line.strip()]
    else:
        places = []

    places = places[:10]
    while len(places) < 10:
        places.append("Coming Soon: Details will be updated soon.")

    return render_template('result.html', places=places)

if __name__ == "__main__":
    app.run(debug=True)