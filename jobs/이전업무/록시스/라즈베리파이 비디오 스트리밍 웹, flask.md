# 라즈베리파이 비디오 스트리밍 웹, flask

> **생성일:** 2024-10-29T06:24:00.000Z
> **수정일:** 2025-09-13T15:38:00.000Z


## 웹 이미지 스트리밍 코드

```python
from flask import Flask, Response
from picamera2 import Picamera2
import cv2
import threading
import time

app = Flask(__name__)

def generate_frames(camera):
    while True:
        frame = camera.capture_array()
        # JPEG로 인코딩
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        # 멀티파트 응답 형식으로 프레임 전송
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    # 간단한 HTML 페이지 반환
    return """
    <html>
    <body>
        <h1>라즈베리파이 카메라 스트리밍</h1>
        <img src="/video_feed">
    </body>
    </html>
    """

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(picam2),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # 카메라 초기화
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={"size": (640, 480)})
    picam2.configure(config)
    picam2.start()
    
    # 서버 시작 (외부 접속 허용을 위해 host='0.0.0.0' 설정)
    app.run(host='0.0.0.0', port=5000, debug=False)
```

## tensorflow lite 모델 활용 picamera2, flask활용 이미지 검출


```python
import argparse
import sys
import time
from flask import Flask, Response, render_template
import cv2
import mediapipe as mp
from picamera2 import Picamera2
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from utils import visualize
import threading

app = Flask(__name__)

# Global variables
COUNTER, FPS = 0, 0
START_TIME = time.time()
output_frame = None
lock = threading.Lock()
frame_rate = 0.1  # 약 10 FPS

def detect_objects(model: str, max_results: int, score_threshold: float, 
                  width: int, height: int):
    global output_frame, COUNTER, FPS, START_TIME

    try:
        # Picamera2 초기화
        picam2 = Picamera2()
        preview_config = picam2.create_preview_configuration(
            main={"size": (width, height),
                  "format": "RGB888"})
        picam2.configure(preview_config)
        picam2.start()
        print("카메라 초기화 완료")  # 디버깅용 메시지

        # Visualization parameters
        row_size = 50
        left_margin = 24
        text_color = (0, 0, 0)
        font_size = 1
        font_thickness = 1
        fps_avg_frame_count = 10

        detection_result_list = []

        def save_result(result: vision.ObjectDetectorResult, unused_output_image: mp.Image, timestamp_ms: int):
            detection_result_list.append(result)

        # Initialize the object detection model
        base_options = python.BaseOptions(model_asset_path=model)
        options = vision.ObjectDetectorOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.LIVE_STREAM,
            max_results=max_results, 
            score_threshold=score_threshold,
            result_callback=save_result)
        detector = vision.ObjectDetector.create_from_options(options)
        print("모델 초기화 완료")  # 디버깅용 메시지

        while True:
            # 새 프레임 캡처
            image = picam2.capture_array()
            if image is None:
                print("이미지 캡처 실패")  # 디버깅용 메시지
                continue

            # MediaPipe 이미지 객체 생성
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)

            # 객체 감지 실행
            detector.detect_async(mp_image, time.time_ns() // 1_000_000)

            # FPS 계산
            current_time = time.time()
            if COUNTER % fps_avg_frame_count == 0:
                FPS = fps_avg_frame_count / (current_time - START_TIME)
                START_TIME = current_time
            COUNTER += 1

            # 현재 프레임 복사
            current_frame = image.copy()

            # FPS 표시
            fps_text = 'FPS = {:.1f}'.format(FPS)
            cv2.putText(current_frame, fps_text, (left_margin, row_size),
                       cv2.FONT_HERSHEY_DUPLEX, font_size, text_color,
                       font_thickness, cv2.LINE_AA)

            # 감지 결과 처리
            if detection_result_list:
                current_frame = visualize(current_frame, detection_result_list[-1])
                detection_result_list.clear()

            # 스레드 안전하게 프레임 업데이트
            with lock:
                output_frame = current_frame.copy()

            # 프레임 레이트 제어
            time.sleep(frame_rate)  # 약 10 FPS

    except Exception as e:
        print(f"카메라 초기화 중 오류 발생: {e}")  # 디버깅용 메시지
    finally:
        print("카메라 및 모델 정리 중...")  # 디버깅용 메시지
        detector.close()
        picam2.stop()

def generate():
    global output_frame
    while True:
        with lock:
            if output_frame is None:
                time.sleep(0.1)  # 잠시 대기 후 다시 시도
                continue
            
            # JPEG로 인코딩
            flag, encoded_image = cv2.imencode(".jpg", output_frame)
            if not flag:
                print("이미지 인코딩 실패")  # 디버깅용 메시지
                continue
            
        # 바이트 스트림 생성
        yield(b'--frame\r\n' 
              b'Content-Type: image/jpeg\r\n\r\n' + 
              bytearray(encoded_image) + b'\r\n')
        
        # 프레임 레이트 제어
        time.sleep(frame_rate)  # 약 10 FPS

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video_feed")
def video_feed():
    return Response(generate(),
                   mimetype = "multipart/x-mixed-replace; boundary=frame")

def run_server(host='0.0.0.0', port=5000):
    app.run(host=host, port=port, debug=False, threaded=True)

def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--model',
        help='Path of the object detection model.',
        required=False,
        default='efficientdet.tflite')
    parser.add_argument(
        '--maxResults',
        help='Max number of detection results.',
        required=False,
        default=5)
    parser.add_argument(
        '--scoreThreshold',
        help='The score threshold of detection results.',
        required=False,
        type=float,
        default=0.25)
    parser.add_argument(
        '--frameWidth',
        help='Width of frame to capture from camera.',
        required=False,
        type=int,
        default=1280)
    parser.add_argument(
        '--frameHeight',
        help='Height of frame to capture from camera.',
        required=False,
        type=int,
        default=720)
    args = parser.parse_args()

    # 객체 감지 스레드 시작
    detection_thread = threading.Thread(target=detect_objects,
                                     args=(args.model, int(args.maxResults),
                                           args.scoreThreshold, args.frameWidth, args.frameHeight))
    detection_thread.daemon = True
    detection_thread.start()

    # Flask 서버 실행
    run_server()

if __name__ == '__main__':
    main()
```

## 📎 연관 문서


- [[엽채류 수확기]] - 3개 공통 주제
- [[7월 24일 cm4확장보드에 cm4연결후 테스트]] - 3개 공통 주제
- [[이미지 모델을 사용한 검출2 - trained model]] - 3개 공통 주제
- [[이미지 데이터 라벨링, 모델훈련, mediapipe, tensorflow]] - 3개 공통 주제
- [[라즈베리파이 http 스트리밍 usb cam, 재부팅시 재실]] - 3개 공통 주제