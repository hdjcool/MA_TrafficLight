### Yolo-world model directory

- Yolo-world 모델 사용시 fine-tuning 없이 아래 와 같이 단어 설정 하면 fire truck 탐지 됨
```
model.set_classes(['ambulance', 'fire truck', 'police car', 'person', 'car', 'bicycle', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'van'])
```
![image](https://github.com/user-attachments/assets/a874ce37-1d64-49ca-bc31-66b4054517d9)

- 다만 ambulance 와 police car 는 탐지가 잘 안되고 있음
![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/5de7cef9-20c4-4f63-aef4-82589c82e341/732bb483-771c-47a7-b97f-b2202db2fc8b/image.png)
YOLO-World supports a "prompt-then-detect" strategy, which utilizes an offline vocabulary to enhance efficiency.
![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/5de7cef9-20c4-4f63-aef4-82589c82e341/fdc04c2a-d911-47a7-b907-67d124406d0c/image.png)
- 아래와 같이 class 설정 후 별도의 fine-tuning 없이 detection 이 가능함을 확인 함
- 단 기존 COCO 데이터 셋의 car, van, truck 등과 같이 사용시에는 police car, ambulance van 보다 우선으로 탐지 함을 보여 우리 시스템에 사용하기 위해서는 결국 2 stage 방식으로 사용 해야 함
```python
model.set_classes(['emergency ambulance van', 'medical van', 'fire truck', 'police car', 'police cruiser']) 
```
![image](https://github.com/user-attachments/assets/579f63a4-8147-4cb4-8169-be9dcf19e5c6)
![image](https://github.com/user-attachments/assets/54da43be-2677-40f6-941d-a0a4ec8351bb)

