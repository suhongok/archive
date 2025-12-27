# ros2 humble + gazebo setup on mac

> **생성일:** 2025-05-12T02:53:00.000Z
> **수정일:** 2025-09-15T00:54:00.000Z

물론입니다! 아래는 Mac에서 ROS2 Humble과 Gazebo를 설치하고, 두 개의 터미널을 사용하여 서버와 클라이언트를 실행하는 과정에서 겪은 문제와 해결 방법을 정리한 마크다운 문서입니다. 기본적인 설치 과정은 PinkWink 블로그의 가이드를 참고하였으며, 이후 발생한 문제는 직접 해결하였습니다.
---

# 🛠 Mac에서 ROS2 Humble 및 Gazebo 설치 및 실행 요약

## 📌 설치 및 설정 개요

- 참고 자료: PinkWink 블로그의 가이드
- 시스템 환경: Mac M1/M2/M3
- 주요 도구:
## 🧱 설치 및 설정 단계

1. Homebrew 설치:
```plain text
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

1. 
1. Miniforge 설치:
```plain text
# Miniforge 설치 스크립트 실행
curl -L -O https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh
bash Miniforge3-MacOSX-arm64.sh
```

1. 
1. Mamba 설치:
```plain text
conda install mamba -c conda-forge
```

1. 
1. 가상환경 생성 및 활성화:
```plain text
conda create -n ros2
conda activate ros2
```

1. 
1. 채널 설정:
```plain text
conda config --env --add channels conda-forge
conda config --env --add channels robostack-staging
conda config --env --remove channels defaults
```

1. 
1. ROS2 Humble 설치:
```plain text
mamba install ros-humble-desktop
```

1. 
1. 환경 재활성화:
```plain text
conda deactivate
conda activate ros2
```

## 🧪 실행 및 테스트

- rviz2 실행 테스트:
```plain text
  rviz2
```

정상적으로 실행되면 설치가 완료된 것입니다.
## 🧩 문제 해결: Gazebo 실행 시 서버와 GUI 분리 실행

### 문제 상황

Mac에서 gz sim 명령어를 실행할 때, -s (서버)와 -g (GUI)를 동시에 실행하려고 하면 다음과 같은 오류가 발생합니다:
```plain text
On macOS `gz sim` currently only works with either the -s argument
or the -g argument, you cannot run both server and gui in one terminal.
See https://github.com/gazebosim/gz-sim/issues/44 for more info.
```

### 해결 방법

서버와 GUI를 별도의 터미널에서 각각 실행합니다:
1. 터미널 1: 서버 실행
```plain text
gz sim -s
```

1. 
1. 터미널 2: GUI 실행
```plain text
gz sim -g
```

이렇게 하면 서버와 GUI가 정상적으로 실행되며, 시뮬레이션을 사용할 수 있습니다.
## ✅ 최종 결과

- ROS2 Humble 및 Gazebo가 Mac에서 정상적으로 설치되고 실행되었습니다.
- gz sim의 서버와 GUI를 별도의 터미널에서 실행하여 문제를 해결하였습니다.
---