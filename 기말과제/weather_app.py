from flask import Flask, jsonify, request
import script3
import openai

app = Flask(__name__)

# /weather 엔드포인트
@app.route('/weather', methods=['GET'])
def weather():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)

    if lat is None or lon is None:
        return jsonify({"error": "좌표가 전달되지 않았습니다."}), 401

    try:
        # 날씨 정보 가져오기
        information_json = script3.get_weather(lat, lon)
        # "answer" 키 제거
        if "answer" in information_json:
            del information_json["answer"]
        return jsonify(information_json)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# /answer 엔드포인트
@app.route('/answer', methods=['GET'])
def answer():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)

    if lat is None or lon is None:
        return jsonify({"error": "좌표가 전달되지 않았습니다."}), 402

    try:
        # 날씨 정보 가져오기
        information_json = script3.get_weather(lat, lon)
        question = information_json.get("question")

        if not question:
            return jsonify({"error": "question이 없습니다."}), 403

        # GPT API를 사용하여 answer 생성
        client = openai.OpenAI(api_key="sk-proj--")
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant who provides weather advice to users, acting as a personal weather assistant. Your responses should be friendly and provide useful recommendations based on the current weather conditions."},
                {"role": "user", "content": question}
            ]
        )
        answer = completion.choices[0].message.content
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
