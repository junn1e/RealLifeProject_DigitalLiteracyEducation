from flask import Flask, jsonify, request  # Flask 임포트
from flask_cors import CORS  # CORS 임포트
import script  # 독립적인 함수 제공 모듈

app = Flask(__name__)
CORS(app)

@app.route('/weather', methods=['GET'])
def weather():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    
    if lat is None or lon is None:
        return jsonify({"error": "좌표가 전달되지 않았습니다."}), 400

    try:
        weather_info = script.get_weather(lat, lon)
        return jsonify(weather_info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
