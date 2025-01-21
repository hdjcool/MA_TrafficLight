"""
API 기능 설명:
1. speak(text): Google TTS를 통해 한국어 텍스트를 mp3로 변환 후 재생 (TTS 안내)
2. play_beep(): 보행자 신호 시 보조 음향(낮은 볼륨의 Beep) 재생
3. render_traffic_lights(car_state, ped_state):
   - 차량 신호등(빨강·노랑·초록), 보행자 신호등(빨강·초록)을 검은색 박스 안에 표시
4. run_traffic_cycle(num_vehicles, num_emergency):
   - 차량 수(num_vehicles), 긴급차량 수(num_emergency)에 따라 신호를 제어
   - 긴급차량만 있는 경우(only emergency) 즉시 차량 녹색
   - 긴급차량이 하나 이상이면 보행자에 음성 안내
   - 보행자 신호 시 Beep 사운드 재생
   - 보행자 신호에서 0.5초 간격으로 '띠' 재생
   - 보행자 신호가 끝나면 "차량 신호로 바뀌었습니다." 안내
5. main():
   - (가정) 모델을 통해 이미 num_vehicles, num_emergency 추론되었다고 보고,
     신호등 시뮬레이션 실행
"""

import streamlit as st
import time
import os
from gtts import gTTS
import playsound

# ---------------------
# 전역 상수
# ---------------------
DEFAULT_STOP_TIME = 30   # 차량 기본 신호 시간(초)
DEFAULT_TRAFFIC = 20     # 기준 트래픽(차량 수)
CROSSING_TIME = 5        # 보행자 횡단 시간(초)
EMERGENCY_CLASS_ID = 8   # 긴급차량(Class ID=8 예시)

# ---------------------
# (1) 음성 안내 함수
# ---------------------
def speak(text: str):
    """
    Google TTS로 text를 mp3로 변환 후 재생합니다.
    파일명/경로는 ASCII 권장.
    """
    filename = 'temp_voice.mp3'
    tts = gTTS(text=text, lang='ko')
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

# ---------------------
# (2) Beep 사운드 함수
# ---------------------
def play_beep():
    """
    보행자 신호 시 낮은 볼륨의 Beep 사운드를 재생합니다.
    Beep 사운드 파일(beep_sound.mp3)은 미리 준비했다고 가정합니다.
    """
    beep_file = 'beep_sound.mp3'
    if os.path.exists(beep_file):
        playsound.playsound(beep_file)
    else:
        print("[WARN] beep_sound.mp3 파일이 존재하지 않아 Beep를 재생할 수 없습니다.")

# ---------------------
# (3) 신호등 시각화 함수
# ---------------------
def render_traffic_lights(car_state: str, ped_state: str):
    """
    차량 신호등(빨강·노랑·초록), 보행자 신호등(빨강·초록) 시각화
    """
    # 차량 신호등 색상 설정
    car_red    = '#FF0000' if car_state == 'red' else '#333333'
    car_yellow = '#FFFF00' if car_state == 'yellow' else '#333333'
    car_green  = '#00FF00' if car_state == 'green' else '#333333'

    # 보행자 신호등 색상 설정
    ped_red   = '#FF0000' if ped_state == 'red' else '#333333'
    ped_green = '#00FF00' if ped_state == 'green' else '#333333'

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 차량 신호등")
        st.markdown(f"""
        <div style="
            width: 80px; 
            height: 240px; 
            background-color: black;
            border-radius: 10px;
            padding: 5px;
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            justify-content: space-around;
        ">
            <!-- 빨강 -->
            <div style="
                width: 60px; 
                height: 60px; 
                border-radius: 50%; 
                background-color: {car_red};
            "></div>
            <!-- 노랑 -->
            <div style="
                width: 60px; 
                height: 60px; 
                border-radius: 50%; 
                background-color: {car_yellow};
            "></div>
            <!-- 초록 -->
            <div style="
                width: 60px; 
                height: 60px; 
                border-radius: 50%; 
                background-color: {car_green};
            "></div>
        </div>
        """, unsafe_allow_html=True)
        st.write(f"**상태:** {car_state.upper()}")

    with col2:
        st.markdown("### 보행자 신호등")
        st.markdown(f"""
        <div style="
            width: 80px; 
            height: 160px; 
            background-color: black;
            border-radius: 10px;
            padding: 5px;
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            justify-content: space-around;
        ">
            <!-- 빨강 -->
            <div style="
                width: 60px; 
                height: 60px; 
                border-radius: 50%; 
                background-color: {ped_red};
            "></div>
            <!-- 초록 -->
            <div style="
                width: 60px; 
                height: 60px; 
                border-radius: 50%; 
                background-color: {ped_green};
            "></div>
        </div>
        """, unsafe_allow_html=True)
        st.write(f"**상태:** {ped_state.upper()}")

# ---------------------
# (4) 신호 주기 로직
# ---------------------
def run_traffic_cycle(num_vehicles: int, num_emergency: int, placeholder):
    """
    차량 수(num_vehicles), 긴급차량 수(num_emergency)를 기반으로
    - 긴급차량만 검출되었으면(only emergency) 즉시 차량 녹색
    - 긴급차량이 하나 이상이면 (보행자에게 TTS 안내)
    - 보행자 신호 시 Beep 사운드
    - 보행자 신호에서 '띠'를 0.2초 간격으로 CROSSING_TIME 동안 반복
    - 보행자 신호 끝나면 "차량 신호로 바뀌었습니다." 안내
    """
  

    def update_signal(car: str, ped: str, desc: str):
        with placeholder:
            st.write(desc)
            render_traffic_lights(car, ped)

    # (A) 긴급차량만 감지된 경우 (only emergency)
    if num_emergency > 0 and num_emergency == num_vehicles:
        st.warning("긴급차량만 감지되어 차량 우선 신호를 즉시 적용합니다.")
        update_signal("green", "red", "**긴급차량 우선 - 차량 녹색**")
        speak("긴급차량이 진입했습니다. 보행자는 대기해주세요.")
        return
    else:
        # (B) 기존의 '차량 수 비례' 로직
        traffic_time = int(num_vehicles / DEFAULT_TRAFFIC * DEFAULT_STOP_TIME)
        if traffic_time < 1:
            traffic_time = 1

        # 긴급차량이 하나 이상 있으면 최소 10초는 확보
        if num_emergency > 0:
            traffic_time = max(traffic_time, 10)
            speak("긴급차량이 감지되었습니다. 보행자는 주의하세요.")

        start_msg = f"신호가 {traffic_time}초 뒤에 바뀝니다."
        end_msg = "신호가 바뀌었습니다."

        # 1) 차량 녹색, 보행자 빨강
        update_signal("green", "red", "**1) 차량: 녹색, 보행자: 빨강**")
        speak(start_msg)
        time.sleep(traffic_time - 1)

        # 2) 차량 황색, 보행자 빨강
        update_signal("yellow", "red", "**2) 차량: 황색, 보행자: 빨강** (1초)")
        time.sleep(1)

        # 3) 차량 적색, 보행자 녹색
        update_signal("red", "green", "**3) 차량: 적색, 보행자: 녹색**")
        # 보행자 신호 시 Beep 사운드
        play_beep()
        speak(end_msg)

        # ───────── 보행자 신호에서 '띠' 반복 ─────────(추후 변경 필요요)
        end_time = time.time() + CROSSING_TIME
        while time.time() < end_time:
            speak("띠")
            time.sleep(0.2)

        # 4) 차량 녹색, 보행자 빨강
        update_signal("green", "red", "**4) 차량: 녹색, 보행자: 빨강**")
        speak("차량 신호로 바뀌었습니다.")
        st.success("신호 주기가 완료되었습니다.")

# ---------------------
# (5) Streamlit 메인
# ---------------------
def main():
    st.title("하나의 신호등을 in-place로 갱신하는 예시")

    # 1) 신호등을 표시할 placeholder를 먼저 선언
    placeholder = st.empty()

    # 2) 초기(대기) 상태를 표시할 때도 이 placeholder를 사용
    with placeholder:
        st.subheader("현재 기본(대기) 상태")
        render_traffic_lights("red", "red")  # 첫 화면에서 '빨강/빨강' 표시

    # 차량·긴급차량 수 입력
    num_vehicles = st.number_input("전체 차량 수", min_value=0, value=3, step=1)
    num_emergency = st.number_input("긴급차량 수", min_value=0, value=0, step=1)

    # 3) 버튼 클릭 시 run_traffic_cycle에 placeholder를 넘겨, 같은 위치에 갱신
    if st.button("신호등 시작"):
        run_traffic_cycle(num_vehicles, num_emergency, placeholder)


if __name__ == "__main__":
    main()
