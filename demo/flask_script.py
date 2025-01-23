from flask import Flask, render_template, jsonify, send_file
from gtts import gTTS
import os
import playsound
import asyncio
from ultralytics import YOLO
import cv2

app = Flask(__name__)

# 신호 시간 최소/최대 값 설정
MIN_TRAFFIC_TIME = 4
MAX_TRAFFIC_TIME = 10
DEFAULT_STOP_TIME = 10
DEFAULT_TRAFFIC = 20
CROSSING_TIME = 4

# 신호등 상태 저장
traffic_signal = "green"
pedestrian_signal = "red"

scenario_num = 1

async def speak(text):
    """ 구글 tts """
    tts = gTTS(text=text, lang='ko')
    filename = 'gtts_voice.mp3'
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

async def capture_frame(model, image_path="images/low_traffic.png"):
    """ YOLO 모델을 사용하여 객체 탐지 수행 """
    global scenario_num

    results = model(image_path)

    img = results[0].plot()
    cv2.imwrite("images/current_image.png", img)
    
    return results

async def detect_emergency_vehicle(model, image_path="images/low_traffic.png"):
    """ 응급차량 감지 함수 """
    global scenario_num

    results = await capture_frame(model, image_path)
    EMERGENCY_VEHICLE_ID = 0  # 응급차량 id (임의로 설정)

    img = results[0].plot()
    cv2.imwrite("images/current_image.png", img)

    return EMERGENCY_VEHICLE_ID in results[0].boxes.cls.tolist()

async def change_traffic_sign(model, yolo_model):
    """ 차량 통행량 기반 보행자 신호 조정 및 응급차량 감지 """
    global traffic_signal, pedestrian_signal, scenario_num

    if scenario_num == 1:
        image_path1 = image_path2 = "images/low_traffic.png"
    elif scenario_num == 2:
        image_path1 = image_path2 = "images/high_traffic.png"
    elif scenario_num == 3:
        image_path1 = image_path2 = "images/emergency.png"
    else:
        image_path1 = "images/low_traffic.png"
        image_path2 = "images/emergency.png"

    #save_image(image_path)

    # 응급차량 감지
    emergency_detected = await detect_emergency_vehicle(model, image_path1)
    if emergency_detected:
        traffic_time = MAX_TRAFFIC_TIME
        app.config['is_emergency'] = " 응급 차량 접근 중"
        app.config['num_vehicles'] = 0
        await speak(f"응급차량이 접근중. {traffic_time}초 뒤에 신호가 바뀝니다.")
    else:
        results = await capture_frame(yolo_model, image_path1)
        vehicle_classes = [2, 3, 5, 6, 7]  # 차량 클래스 ID (car, motorcycle, bus, train, truck)

        # 차량 수 계산
        num_vehicles = sum(results[0].boxes.cls.tolist().count(class_id) for class_id in vehicle_classes)
        # 차량 수 정보를 클라이언트에 전달
        app.config['is_emergency'] = " 응급 차량 없음"
        app.config['num_vehicles'] = num_vehicles

        # 신호 시간 조정
        traffic_time = max(MIN_TRAFFIC_TIME, min(MAX_TRAFFIC_TIME, int(num_vehicles / DEFAULT_TRAFFIC * DEFAULT_STOP_TIME)))
        await speak(f"신호가 {traffic_time}초 뒤에 바뀝니다.")

    # 신호 변경
    await asyncio.sleep(traffic_time - 2)
    traffic_signal = "yellow"
    pedestrian_signal = "red"
    print("차량 황색신호")

    await asyncio.sleep(2)
    traffic_signal = "red"
    pedestrian_signal = "green"
    print("차량 적색신호, 보행자 녹색신호")
    await speak("신호가 바뀌었습니다.")

    # 보행자 신호가 녹색으로 바뀐 시점에서 응급차량 체크
    if await detect_emergency_vehicle(model, image_path2):
        app.config['is_emergency'] = " 응급 차량 접근중"
        await speak("응급 차량 접근 중. 주의하여 도로를 건너가십시오.")

    # 보행자 신호 종료
    await asyncio.sleep(CROSSING_TIME)
    traffic_signal = "green"
    pedestrian_signal = "red"
    print("보행자 적색신호, 차량 녹색신호")
    await speak("신호가 종료되었습니다.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_signals')
def get_signals():
    """ 신호등 상태를 클라이언트에 전달 """
    return jsonify({
        'traffic_signal': traffic_signal,
        'pedestrian_signal': pedestrian_signal, 
        "num_vehicles": app.config.get('num_vehicles', 0), 
        "is_emergency": app.config.get('is_emergency', "신호 없음")
    })

@app.route('/start_signal_change')
def start_signal_change():
    model = YOLO("yolo11n.pt")
    emergency_model = YOLO("best.pt")
    # 신호 변경 시작
    asyncio.run(change_traffic_sign(emergency_model, model))
    return jsonify({"message": "신호 변경이 시작되었습니다."})

@app.route('/change_scenario/<int:scenario>')
def change_scenario(scenario):
    """ 시나리오 변경 요청 처리 """
    global scenario_num
    scenario_num = scenario
    return jsonify({"message": f"Scenario {scenario}."}), 404

@app.route('/get_image')
def get_image():
    """ 현재 이미지를 클라이언트에 전달 """
    image_path = "images/current_image.png"
    if not os.path.exists(image_path):
        image_path = "images/low_traffic.png"  # 기본 이미지 경로
    return send_file(image_path, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
