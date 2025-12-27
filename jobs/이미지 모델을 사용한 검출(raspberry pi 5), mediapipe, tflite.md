# 이미지 모델을 사용한 검출(raspberry pi 5), mediapipe, tflite

> **생성일:** 2024-09-09T00:44:00.000Z
> **수정일:** 2025-09-13T15:38:00.000Z

# 라즈베리파이 이미지 검출 테스트

- 기 생성된 이미지 모델을 활용하여, 라즈베리 파이에서 이미지 검출 모델 동작 테스트 
## 실행 환경

- 참고링크https://www.youtube.com/watch?v=kX6zWqMP9U4&t=73s
- 라즈베리파이 5, 라즈베리파이 os 실행환경 설정
- miniconda3로 가상환경 생성 python3.9기반.
## 테스트 진행

- code 수정 gui기반이 아닌 원격 기반으로 실행하기 때문에 코드 수정
```python
#detect.py

# 기존 코드
 if cv2.waitKey(1) == 27:
 break

# 수정된 코드
 import time
 if time.time() - start_time > 0.1:  # 100ms마다 체크
     if input() == 'q':
         break
     start_time = time.time()
       
       
# ... 기존 코드 ...

def run(model: str, camera_id: int, width: int, height: int, num_threads: int,
        enable_edgetpu: bool) -> None:
    # ... 기존 코드 ...
    
    # cv2.imshow('object_detector', image) 대신:
    cv2.imwrite('detected_objects.jpg', image)
    print("이미지가 'detected_objects.jpg'로 저장되었습니다.")

# ... 기존 코드 ...
```

- git으로 설치 성공 실행은 
```bash
python3 detect.py \
  --model efficientdet_lite0.tflite
```

- 실행화면