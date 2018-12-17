from flask import Flask, render_template, request, send_from_directory
from flask_cors import CORS
from controller import EZWController
 
app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
   return render_template('index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/browserconfig.xml')
def send_browserconfig():
    return send_from_directory('static', 'browserconfig.xml')
 
@app.route('/ezw', methods=['POST', 'GET'])
def ezw():
    if request.method == 'POST': 
       data = request.json
       input_location = data['location']
 
       ezw = EZWController()
 
       geo_location = ezw.getLocation(input_location)
       if geo_location == None:
           ezw_address = "Unknown location"
           report_template = render_template('report.html', weather_address=ezw_address)
           return report_template 
 
       ezw_address = geo_location.address       
       ezw_reports = ezw.getWeatherReports(data, geo_location)
 
       report_template = render_template('report.html', weather_address=ezw_address, weather_reports=ezw_reports)
 
    return report_template  
 
if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')