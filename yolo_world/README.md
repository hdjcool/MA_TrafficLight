### Yolo-world model directory

- Yolo-world 모델 사용시 fine-tuning 없이 아래 와 같이 단어 설정 하면 fire truck 탐지 됨
```
model.set_classes(['ambulance', 'fire truck', 'police car', 'person', 'car', 'bicycle', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'van'])
```
![image](https://github.com/user-attachments/assets/a874ce37-1d64-49ca-bc31-66b4054517d9)

- 다만 ambulance 와 police car 는 탐지가 잘 안되고 있음
