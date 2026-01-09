# CMake 캐시 메커니즘 이해

## 🎯 개요

CMake는 **빌드 설정 정보를 캐시에 저장**하여 다음 빌드를 빠르게 처리합니다. 하지만 소스 경로가 변경되면 캐시가 문제가 될 수 있습니다.

---

## 💾 CMake 캐시란?

### 정의
CMake가 처음 빌드할 때 설정한 정보를 `build/CMakeCache.txt` 파일에 저장하는 것입니다.

### 저장되는 정보

```
# build/CMakeCache.txt 예시

CMAKE_BUILD_TYPE:STRING=Release
CMAKE_SOURCE_DIR:STATIC=/home/sm/ros2_ws/src/custom_interfaces/src
CMAKE_BINARY_DIR:STATIC=/home/sm/ros2_ws/build/custom_interfaces
CMAKE_CXX_COMPILER:FILEPATH=/usr/bin/c++
...
```

### 목적

| 목적 | 설명 |
|------|------|
| **빠른 빌드** | 이전 설정을 재사용하여 시간 절약 |
| **설정 유지** | 같은 설정으로 계속 빌드 |
| **점진적 빌드** | 변경된 부분만 다시 컴파일 |

---

## ⚠️ 캐시가 문제가 되는 이유

### 경로 불일치 에러

다음 빌드 때, CMake는 **캐시된 소스 경로**와 **현재 소스 경로**를 비교합니다:

```
캐시에 저장된 경로: /home/sm/ros2_ws/src/custom_interfaces/src/CMakeLists.txt
현재 실제 경로:    /home/sm/ros2_ws/src/custom_interfaces/CMakeLists.txt

비교 결과: ❌ 경로가 다르다 
↓
CMake Error: The source "..." does not match the source "..." used to generate cache.
```

### 캐시가 문제가 되는 상황들

| 상황 | 원인 |
|------|------|
| **소스 폴더 이동** | 경로 변경 |
| **파일 구조 변경** | 예상 경로와 실제 경로 불일치 |
| **CMakeLists.txt 경로 변경** | 캐시가 이전 경로 기억 |
| **패키지 이름 변경** | 캐시 무효화 |

---

## 🔄 이번 경우의 구체적인 상황

### 1️⃣ 처음 빌드 (잘못된 구조)

```
프로젝트 구조:
src/custom_interfaces/
└── src/  ← 잘못된 중첩 구조
    ├── CMakeLists.txt
    ├── MoveRobot.srv
    └── ...

첫 번째 빌드:
$ colcon build --packages-select custom_interfaces

CMake가 감지한 소스 경로:
/home/sm/ros2_ws/src/custom_interfaces/src/CMakeLists.txt
                                        ^^^

이 정보를 캐시에 저장:
build/CMakeCache.txt → CMAKE_SOURCE_DIR=/home/sm/ros2_ws/src/custom_interfaces/src
```

### 2️⃣ 파일 이동 (올바른 구조로 수정)

```
새로운 프로젝트 구조:
src/custom_interfaces/
├── CMakeLists.txt  ← 올바른 위치 (src/ 제거)
├── package.xml
├── msg/
│   └── RobotStatus.msg
└── srv/
    └── MoveRobot.srv

파일 재배치 완료!
```

### 3️⃣ 두 번째 빌드 (에러 발생)

```
두 번째 빌드 시도:
$ colcon build --packages-select custom_interfaces

CMake가 캐시 확인:
  캐시에 저장된 경로: /home/sm/ros2_ws/src/custom_interfaces/src/CMakeLists.txt
  현재 실제 경로:    /home/sm/ros2_ws/src/custom_interfaces/CMakeLists.txt

비교 결과: 
  ❌ /src/custom_interfaces/src/ ≠ /src/custom_interfaces/
  
에러 메시지:
CMake Error: The source "/home/sm/ros2_ws/src/custom_interfaces/CMakeLists.txt" 
does not match the source "/home/sm/ros2_ws/src/custom_interfaces/src/CMakeLists.txt" 
used to generate cache.  Re-run cmake with a different source directory.
```

---

## ✅ 해결 방법

### 1️⃣ 캐시 삭제

```bash
cd ~/ros2_ws
rm -rf build/
```

**삭제되는 파일:**
```
build/
├── CMakeCache.txt  ← 삭제됨
├── custom_interfaces/
│   ├── CMakeFiles/  ← 삭제됨
│   ├── cmake_args.last  ← 삭제됨
│   └── ...
└── ...
```

### 2️⃣ 재빌드

```bash
colcon build --symlink-install --packages-select custom_interfaces
```

**새로운 캐시 생성:**
```
CMake가 올바른 경로 감지:
/home/sm/ros2_ws/src/custom_interfaces/CMakeLists.txt
                                        (src/ 없음)

새로운 캐시 생성:
build/CMakeCache.txt → CMAKE_SOURCE_DIR=/home/sm/ros2_ws/src/custom_interfaces
                                         (올바른 경로)
```

---

## 📊 캐시 동작 흐름

### 정상 상황 (캐시 재사용)

```
첫 번째 빌드          두 번째 빌드          세 번째 빌드
    ↓                    ↓                    ↓
CMake 실행          캐시 읽음             캐시 읽음
    ↓                    ↓                    ↓
캐시 생성           설정 확인 OK          설정 확인 OK
    ↓                    ↓                    ↓
빌드 완료           빌드 진행            빌드 진행
                    (빠름!)              (빠름!)
```

### 문제 상황 (경로 변경)

```
첫 번째 빌드          파일 이동              두 번째 빌드
    ↓                    ↓                    ↓
CMake 실행           폴더 구조 변경        캐시 읽음
    ↓                    ↓                    ↓
캐시 생성:          경로 불일치           경로 확인
src/.../src/                                 ↓
    ↓                                    ❌ 불일치!
빌드 완료                                    ↓
                                         에러 발생!
```

---

## 💡 실제 사례

### Before (캐시 존재 - 에러)

```
$ colcon build --packages-select custom_interfaces

Starting >>> custom_interfaces
--- stderr: custom_interfaces
CMake Error: The source "/home/sm/ros2_ws/src/custom_interfaces/CMakeLists.txt" 
does not match the source "/home/sm/ros2_ws/src/custom_interfaces/src/CMakeLists.txt" 
used to generate cache.

Failed   <<< custom_interfaces [0.03s, exited with code 1]
```

### Solution (캐시 삭제)

```
$ rm -rf build/
```

### After (캐시 초기화 - 성공)

```
$ colcon build --symlink-install --packages-select custom_interfaces

Starting >>> custom_interfaces
Finished <<< custom_interfaces [5.23s]

Summary: 1 package finished [5.54s]
```

---

## 🔑 핵심 정리

| 개념 | 설명 |
|------|------|
| **캐시 목적** | 빌드 설정 저장 및 빠른 재빌드 |
| **캐시 위치** | `build/CMakeCache.txt` |
| **문제 원인** | 경로 변경 시 캐시가 이전 경로 기억 |
| **해결 방법** | `rm -rf build/` 후 재빌드 |
| **언제 삭제?** | 소스 경로, 구조, 이름 변경 시 |

---

## ⏱️ 캐시 삭제의 시간 영향

### 캐시 활용 (정상)
```
두 번째 빌드: 1-2초 (빠름)
```

### 캐시 없음 (초기화)
```
첫 번째 빌드: 5-10초 (느림)
```

**결론**: 소스 변경이 없으면 캐시는 매우 유용하지만, 구조 변경 시에는 캐시를 초기화해야 합니다.


## 📎 연관 문서


- [[식물재배 -ph센서 테스트]] - 2개 공통 주제
- [[상추수확기 제작기(프레임 조립)]] - 2개 공통 주제
- [[Led 와트 식물등 필요량 ]] - 2개 공통 주제
- [[7월 28일 라즈베리파이 초음파센서 제어]] - 2개 공통 주제
- [[03_비동기_서비스_완료_확인]] - 2개 공통 주제