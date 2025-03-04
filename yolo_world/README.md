### Yolo-world model directory
YOLO-World supports a "prompt-then-detect" strategy, which utilizes an offline vocabulary to enhance efficiency.  

![image](https://github.com/user-attachments/assets/e1cc8fbe-e56d-4a8f-8d52-168c207a564f)  
![image](https://github.com/user-attachments/assets/3fc92088-97f1-48ba-99d7-0f01b4f10a5f)  
https://docs.ultralytics.com/models/yolo-world/
---

- Yolo-world 모델 사용시 fine-tuning 없이 아래 와 같이 단어 설정 하면 fire truck 탐지 됨
```
model.set_classes(['ambulance', 'fire truck', 'police car', 'person', 'car', 'bicycle', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'van'])
```
![image](https://github.com/user-attachments/assets/a874ce37-1d64-49ca-bc31-66b4054517d9)
- 다만 ambulance 와 police car 는 탐지가 잘 안되고 있음
![image](https://github.com/user-attachments/assets/1b34a0ee-1348-4929-85f3-97e8f17058c5)
![image](https://github.com/user-attachments/assets/f9e2458c-be13-45ec-a02c-2d52e794aaa5)

### class 단어 변경
- 아래와 같이 class 설정 후 별도의 fine-tuning 없이 detection 이 가능함을 확인 함
- 단 기존 COCO 데이터 셋의 car, van, truck 등과 같이 사용시에는 police car, ambulance van 보다 우선으로 탐지 함을 보여 우리 시스템에 사용하기 위해서는 결국 2 stage 방식으로 사용 해야 함
```python
model.set_classes(['emergency ambulance van', 'medical van', 'fire truck', 'police car', 'police cruiser']) 
```
![image](https://github.com/user-attachments/assets/579f63a4-8147-4cb4-8169-be9dcf19e5c6)
![image](https://github.com/user-attachments/assets/54da43be-2677-40f6-941d-a0a4ec8351bb)

