# JONano에서  text-generation-webui 설치 시도 

> **생성일:** 2025-12-19T01:04:00.000Z
> **수정일:** 2025-12-19T03:04:00.000Z

# Jetson Orin Nano(8GB) – jetson-containers / text-generation-webui 설치 시도 기록

## ✅ 목표

- Jetson Orin Nano 8GB (SSD 256GB, swap 32GB)에서 jetson-containers로
---

## 🔎 진행 로그 요약 (핵심 타임라인)

- cuda-toolkit-12-6 설치 및 이미지 생성 성공
- 태그: text-generation-webui:r36.4.tegra-aarch64-cu126-22.04-cuda_12.6
- 컨테이너에서 nvcc 확인됨
✅ 결론: CUDA 기본 베이스 이미지는 정상
### 증상

- jetson-containers build 테스트 중 아래 오류로 중단됨:
### 원인

- Jetson(tegra/L4T) 환경에서 --gpus=all이 “훅 직접 호출”로 처리되어 막히는 케이스
- NVIDIA runtime 명시가 필수
### 해결

- sudo docker run --runtime=nvidia ...로 테스트 실행 → 정상 동작 확인
✅ 결론: GPU 런타임 방식 문제였고 해결됨
- /etc/docker/daemon.json 설정:
- systemctl restart docker
- docker info에서 Default Runtime이 nvidia로 바뀐 것 확인
- usermod -aG docker $USER + newgrp docker로 권한도 해결
✅ 결론: 이후부터는 sudo 없이도 docker 사용 가능 + 기본 nvidia runtime 적용
---

## 💣 실패 원인 분석 (결론)

### 증상

- PyTorch 빌드 단계에서 장시간 컴파일 진행 후:
### 결정적 증거

- dmesg에 OOM killer 기록이 명확히 남음:
### 왜 swap 32GB인데도?

- CUDA 컴파일(cicc, flash-attention 계열)은 순간 메모리 피크가 큼
- swap은 “용량”은 늘려주지만 피크 순간 성능/지연 때문에 결국 OOM이 날 수 있음
- gnome-shell 같은 GUI 프로세스도 OOM 로그에 함께 등장 → 헤드리스가 유리
✅ 결론: 실패 원인은 디스크가 아니라 “메모리 OOM”이 거의 확정
- 로그에서 fatal: Remote branch v2.10.0 not found... 같은 메시지가 있었음
- 다만 “최종 중단 트리거”는 Killed + dmesg OOM이 확실해서
---

## 🧹 마무리 정리(정상 복구/정리 작업)

- docker system prune -f 실행
- 약 3.236GB 회수
- 큰 이미지(17GB급)들이 남아있어도 “unused” 중간 레이어 일부 정리됨
- ~/jetson-containers/data/models/huggingface 쪽 캐시/모델이 가장 큼(최대 16GB급)
- 정리 후:
✅ 결론: 빌드 실패 후 시스템 공간은 충분히 회복됨
---

## ✅ 현재 상태 체크

- Docker 실행 정상
- Default runtime = nvidia 확인 완료
- 컨테이너 내부에서 /dev/nvhost*, /dev/nvidia*, /etc/nv_tegra_release 확인 → GPU 패스스루 OK
- text-generation-webui 최종 빌드는 PyTorch 소스 빌드 OOM 때문에 실패
---

## 🎯 다음 액션(재도전 전략)

- GUI 끄고(또는 멈추고) 빌드/런 수행
- 빌드 병렬 수 제한(예: -j1 수준)
- 가능하면 “소스 빌드 없는” 경로 선택:
---

원하면, 다음 단계로 **“헤드리스 전환 커맨드 + 빌드 병렬 제한 + OOM 줄이는 설정”**을 내가 너 환경(Orin Nano 8GB, Ubuntu 22.04, SSD, swap 32GB) 기준으로 바로 실행 순서대로 체크리스트로 만들어줄게.