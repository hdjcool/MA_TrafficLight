========================================
README: 지능형 교통 신호 시스템 (w/o YOLO)
========================================

1. 요구 환경
------------
- Python 3.9 이상
- 필수 라이브러리 설치:
  pip install streamlit gTTS playsound
- (옵션) beep_sound.mp3 파일을 스크립트와 같은 폴더에 두면
  보행자 신호 시 비프음이 재생됩니다.
- (환경파일) environment.yml 사용 가능
  예) conda env create -f environment.yml

2. 사용 방법
------------
1) (선택) 가상환경 활성화  
   conda activate traffic-env

2) Streamlit 실행  
   streamlit run script.py

3) 브라우저에 표시된 로컬 URL(예: http://localhost:8501) 접속  
   - 초기 화면에서 기본 신호등 상태가 표시됩니다.
   - 차량 수·긴급차량 수를 입력하고 "신호등 시작" 버튼을 누르면
     단계별 시뮬레이션이 진행됩니다.
   - 차량 수·긴급차량 수를 모델에서 받아오도록 수정 필요

4) (4) 신호 주기 로직에 영민님의 신호등 로직 반영필요
