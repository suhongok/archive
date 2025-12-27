# mac m2max에서 llama2-7b테스트

> **생성일:** 2025-12-08T15:38:00.000Z
> **수정일:** 2025-12-19T03:06:00.000Z

1. llama2 -7b모델을 다운받아 metal버전으로 빌드하고 4int로 양자화 한 후 json 테스트
---

# 📌 Llama-2 7B 모델 다운로드 → Metal 빌드 → GGUF 변환 → 양자화(Q4_K_M) 전체 과정 정리

## 1. 🏁 Python 환경 준비

- macOS(M2 Max)에서 전용 가상환경 생성
```plain text
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

- 필요한 패키지 설치
```plain text
pip install transformers huggingface_hub torch sentencepiece
```

---

## 2. 🔑 Hugging Face 모델 다운로드 (Llama-2-7B-chat-hf)

- snapshot_download()를 이용해 직접 다운로드:
```plain text
from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="meta-llama/Llama-2-7b-chat-hf",
    local_dir="llama2-7b-chat-hf",
    local_dir_use_symlinks=False,
    token="hf_xxx..."
)
```

- 다운로드 결과:
---

## 3. ⚙️ llama.cpp 빌드 (Metal 가속 ON)

- 최신 llama.cpp clone:
```plain text
cd ~/llama2
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
```

- Metal 백엔드 활성화하여 빌드:
```plain text
mkdir build && cd build
cmake -DLLAMA_METAL=ON ..
cmake --build . --config Release -j$(sysctl -n hw.ncpu)
```

- 빌드 후 생성된 binary 확인:
---

## 4. 📦 HF 모델 → GGUF 변환 (FP16)

- llama.cpp 변환 스크립트 실행:
```plain text
python3 convert_hf_to_gguf.py \
  --outfile ./models/llama-2-7b-fp16.gguf \
  ~/llama2/llama2-7b-chat-hf
```

- 변환 결과:
---

## 5. 🔍 (중간 이슈) quantize 실행 파일 위치 문제

- 처음에는 ./bin/quantize가 없었음.
- 정답은 llama-quantize (로 새 이름 변경됨)
- 올바른 실행 파일은:
```plain text
./build/bin/llama-quantize
```

---

## 6. ⚡ FP16 → Q4_K_M 양자화

```plain text
./build/bin/llama-quantize \
  ./models/llama-2-7b-fp16.gguf \
  ./models/llama-2-7b-Q4_K_M.gguf \
  Q4_K_M
```

- 결과:
---

## 7. 🧪 테스트 실행 (llama-cli)

```plain text
./build/bin/llama-cli \
  -m ./models/llama-2-7b-Q4_K_M.gguf \
  -p "전진해"
```

- 정상적으로 모델 응답 출력됨.
---

# 🎯 오늘 과정의 핵심 요약


---

# ✨ 결론

- M2 Max + Metal 환경에서 llama.cpp 빌드 → 변환 → 양자화까지 전체 파이프라인 정착.
- 이제 Jetson Orin 용 TensorRT-LLM 변환도 병행 가능.
- Gemma-3 4B와 비교했을 때, Llama-2는 구조적 LLM 제어에 조금 약함도 확인.
---

원하면 Notion 스타일 블록(토글/하이라이트/번호 목록) 버전으로도 만들어줄게!