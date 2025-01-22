# Base model Demo file
---
### 베이스 모델 : YOLO11
https://docs.ultralytics.com/models/yolo11/#overview
![image](https://github.com/user-attachments/assets/c1016204-e001-4440-8a90-3be2af83b3a1)
---
### mac4 pro MPS 환경 설정 
- yolo_tutorial.ipynb
  - Mac4 local conda 환경에서 Test 함
```bash
❯ conda create --name ultralytics-env python=3.11 -y                                                                                       ─╯
Retrieving notices: done
Channels:
 - conda-forge
Platform: osx-arm64
Collecting package metadata (repodata.json): done
Solving environment: done
```

```bash
❯ conda activate ultralytics-env
```

```bash
❯ conda install -c conda-forge ultralytics
```

```bash
❯ conda install pytorch torchvision torchaudio -c pytorch-nightly
```

```bash
# environment.yml 만들기
❯ conda env export > environment.yml 
```

```bash
# 다른 시스템에서 이 환경을 재현하려면 다음 명령어를 실행
conda env create -f environment.yml
```

CLIP 설치 : yolov-world 모델 사용할 시
```bash
pip install git+https://github.com/openai/CLIP.git
```

