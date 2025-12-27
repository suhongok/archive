# 이미지 모델을 사용한 검출2 - trained model

> **생성일:** 2024-09-30T03:03:00.000Z
> **수정일:** 2025-09-13T15:38:00.000Z

이미지 모델을 사용한 검출(raspberry pi 5), mediapipe, tflite 
## 훈련 된 환경을 이용한 이미지 검출

- 기 훈련된 tensorflow lite 모델을 python3.9기준 코드에서 동작 아래와 같은 에러발생
```python
detector = _CppObjectDetector.create_from_options(
ValueError: Mobile SSD models are expected to have exactly 4 outputs, found 2
```

- 원인 분석 
- 결과