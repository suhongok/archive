# jetson orin nano llm사용시도.

> **생성일:** 2025-12-05T09:26:00.000Z
> **수정일:** 2025-12-19T03:06:00.000Z

- gpu를 써서 llm돌리는게 목표
- 그냥 이것저것 시도하다 그냥 ollama로 동작시키게됨.
- qwen3:4b 돌리니 gpu로 잘 돌아가는데, 쓸데없이 말을 길게 해서 못쓰겠음.
- gemma3b:1b돌아가나, 잘 못알아 들음.
- ministral-3를 써보려고함. → 아예 안돌아감.
- gemma3:4b잘 동작하고 꽤나 정확하게 알아들음. 그런데 반응이 늦음 한 5초정도? 

```mermaid
import speech_recognition as sr
from gtts import gTTS
import os
import ollama
import json
import re
import time

# -------------------------
#  설정
# -------------------------
MODEL_NAME = "gemma3:4b"
TEMP_SOUND_FILE = "robot_voice.mp3"

SYSTEM_PROMPT = """
너는 ROS2 기반 메카넘휠 로봇을 제어하는 LLM이다.
사용자의 자연어 명령을 해석하여 아래 JSON 형식으로만 출력한다.

형식:
{
  "response": "로봇이 사용자에게 말할 짧은 응답",
  "action": "move | rotate | stop",
  "vx": -2.0 ~ 2.0,
  "vy": -2.0 ~ 2.0,
  "omega": -2.0 ~ 2.0,
  "distance": 미터 단위 숫자 (없으면 0.0),
  "duration": 초 단위 숫자 (없으면 0.0)
}

규칙:
- JSON 외의 텍스트는 절대 출력하지 않는다.
- response는 한국어 한두 문장으로 간단히 설명한다.
- 속도값 vx, vy, omega는 항상 -2.0~2.0 범위 내.
- stop동작 시 속도값은 0.0.
"""

# -------------------------
#  유틸 함수
# -------------------------

def cleanup_files():
    """임시 mp3 파일 삭제"""
    if os.path.exists(TEMP_SOUND_FILE):
        try:
            os.remove(TEMP_SOUND_FILE)
        except:
            pass

def speak(text):
    """TTS 출력 + 파일 자동 삭제"""
    print(f"[🔊 로봇]: {text}")

    cleanup_files()
    try:
        tts = gTTS(text=text, lang='ko')
        tts.save(TEMP_SOUND_FILE)
        os.system(f"mpg321 -g 150 {TEMP_SOUND_FILE} > /dev/null 2>&1")
    except Exception as e:
        print(f"TTS 오류: {e}")
    finally:
        cleanup_files()

def extract_json(text):
    """문장 중 JSON만 추출"""
    try:
        match = re.search(r'\{.*?\}', text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except:
        pass
    return None

def ask_llm(user_text):
    """Ollama를 통해 JSON 명령 생성"""
    print(f"[🧠 LLM 분석 중...] ({MODEL_NAME})")

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"사용자: {user_text}\nJSON 출력:"}
    ]

    try:
        response = ollama.chat(model=MODEL_NAME, messages=messages)
        return extract_json(response["message"]["content"])
    except Exception as e:
        print("LLM 오류:", e)
        return None

# -------------------------
#  메인 실행 루프
# -------------------------

r = sr.Recognizer()
r.dynamic_energy_threshold = True   # 자동으로 노이즈 레벨 적응

cleanup_files()
print(f"\n✨ 로봇 제어 시스템 시작 ({MODEL_NAME})")

try:
    while True:
        # 매 번 새 마이크 세션 열기 → 이전 입력 영향 최소화
        with sr.Microphone() as source:
            try:
                print("\n🎙 마이크 초기화 중...")
                r.adjust_for_ambient_noise(source, duration=0.5)
                print(f"   현재 에너지 임계값: {r.energy_threshold:.1f}")

                # 1. 안내 멘트
                speak("명령을 내려주세요.")

                # 2. 메아리 방지
                print("⏳ 1초간 대기... (지금 말해도 안 들어요)")
                time.sleep(1.0)

                # 3. 녹음 (최대 3초, 시작 대기 최대 4초)
                print("\n🔴 [REC] 녹음 시작! 3초 동안 말씀하세요!")
                try:
                    audio = r.listen(source, timeout=4, phrase_time_limit=3)
                except sr.WaitTimeoutError:
                    print("⏹️ 시간 초과: 아무 말도 감지되지 않았습니다.")
                    speak("아무 말도 들리지 않았어요. 다시 말씀해 주세요.")
                    continue

                print("⏹️ 녹음 끝. 인식 중...")

                # 4. 음성 인식
                try:
                    user_cmd = r.recognize_google(audio, language="ko-KR")
                    user_cmd = user_cmd.strip()
                    print(f"[👤 사용자]: {user_cmd}")
                except sr.UnknownValueError:
                    print("❌ 음성을 인식하지 못했습니다.")
                    speak("무슨 말인지 이해하지 못했어요. 다시 말씀해 주세요.")
                    continue
                except sr.RequestError as e:
                    print(f"❌ STT 요청 오류: {e}")
                    speak("음성 인식 서버에 문제가 있습니다.")
                    continue

                if not user_cmd:
                    speak("다시 말씀해 주세요.")
                    continue

                # 종료 명령 처리
                if "종료" in user_cmd or "꺼" in user_cmd or "끄" in user_cmd:
                    speak("시스템을 종료합니다.")
                    raise KeyboardInterrupt

                # 5. LLM 분석(JSON 생성)
                result = ask_llm(user_cmd)

                if result is None:
                    speak("명령을 해석할 수 없어요. 다시 말씀해주세요.")
                    continue

                # 6. 로봇 응답 + JSON 출력
                speak(result.get("response", "알겠습니다."))

                print("-" * 30)
                print("🚀 [로봇 제어 명령]")
                print(json.dumps(result, ensure_ascii=False, indent=2))
                print("-" * 30)

                # TODO: 여기서 ROS2/ESP32로 실제 명령 보내기
                # publish_robot_command(result)

                time.sleep(0.5)

            except Exception as e:
                print(f"⚠️ 루프 내부 예외: {e}")
                cleanup_files()
                time.sleep(1.0)

except KeyboardInterrupt:
    print("\n🛑 프로그램 종료 요청됨.")

speak("프로그램을 종료합니다.")
cleanup_files()
print("🧹 정리 완료.")
```


jetson clock 을 켜고, 컨텍스트 사이즈를 조정해서 model을 실행했더니 엄청 빨라짐.


Jetson Orin Nano 8GB의 메모리 견적서]

- gemma3:4b가 적절
- 아래처럼 modelfile수정 - gpu사용량 극대화 하고 컨텍스트 수정
```python
sm@allturnbot:~/ollama-models/gemma3-mecanum$ cat Modelfile
FROM gemma3:4b

PARAMETER num_gpu 999

PARAMETER num_ctx 1024
PARAMETER temperature 0.7
PARAMETER num_predict 128
PARAMETER top_p 0.9
PARAMETER top_k 40

SYSTEM """
너는 ROS2 기반 메카넘휠 로봇을 제어하는 LLM이다.
사용자의 자연어 명령을 해석하여 항상 아래 JSON 형식으로만 답변한다.

형식:
{
  "response": "로봇이 사용자에게 말할 짧은 응답",
  "action": "move | rotate | stop",
  "vx": -2.0 ~ 2.0,   // 전/후 병진 속도 비율
  "vy": -2.0 ~ 2.0,   // 좌/우 병진 속도 비율
  "omega": -2.0 ~ 2.0, // 회전 속도 비율 (rad/s 스케일)
  "distance": 0.0 이상, // 미터 단위 거리, 없으면 0.0
  "duration": 0.0 이상  // 초 단위 시간, 없으면 0.0
}

규칙:
- JSON 외의 텍스트는 절대 출력하지 않는다. (설명, 문장, 코드 블록, 주석 모두 금지)
- 항상 하나의 JSON 객체만 출력한다.
- "response"는 한국어 한두 문장으로, 로봇이 지금 수행할 동작을 짧게 설명한다.
- vx, vy, omega는 반드시 -2.0 이상 2.0 이하의 실수 값만 사용한다.

방향 매핑:
- "앞으로", "전진"       → vx > 0, vy = 0
- "뒤로", "후진"         → vx < 0, vy = 0
- "왼쪽으로 이동"        → vx = 0, vy > 0
- "오른쪽으로 이동"      → vx = 0, vy < 0
- "왼쪽으로 회전"        → vx = 0, vy = 0, omega > 0
- "오른쪽으로 회전"      → vx = 0, vy = 0, omega < 0
- 대각선 이동(예: "앞으로 오른쪽") → vx > 0, vy < 0 같이 조합 가능

속도 표현 매핑:
- "아주 천천히", "살살"    → 속도 크기 ≈ 0.1 ~ 0.2
- "천천히"                 → 속도 크기 ≈ 0.2 ~ 0.4
- "보통 속도"              → 속도 크기 ≈ 0.5 ~ 0.8
- "빠르게", "전력 질주"    → 속도 크기 ≈ 1.0 ~ 1.5 (단, 2.0은 넘기지 않는다)

거리 / 시간:
- 거리 기반 명령:
  - 예: "앞으로 1.5미터 가" → distance = 1.5, duration = 0.0
- 시간 기반 명령:
  - 예: "3초 동안 제자리에서 오른쪽으로 돌아" → duration = 3.0, distance = 0.0
- 둘 다 언급되면 둘 다 채우되, 모호하면 하나만 선택해 일관되게 사용한다.

정지 명령:
- "멈춰", "정지", "스톱" 등 → action = "stop", vx = 0.0, vy = 0.0, omega = 0.0, distance = 0.0, duration = 0.0

에러 / 이해 불가:
- 사용자의 명령을 이해하지 못하거나 위험해 보일 경우:
  - action = "stop"
  - vx = vy = omega = 0.0
  - distance = 0.0, duration = 0.0
  - response에 "명령을 이해하지 못했습니다. 다시 말씀해 주세요." 와 같이 안내 문장을 넣는다.

중요:
- 어떤 상황에서도 JSON 형식을 반드시 지킨다.
- 키 이름은 항상 소문자 + 정확한 철자를 사용한다. (response, action, vx, vy, omega, distance, duration)
- 불필요한 필드는 추가하지 않는다.
"""

```

- 대화가 실사용 가능할정도로 빨라짐.