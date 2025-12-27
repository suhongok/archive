# ROS setup on Mac

> **생성일:** 2024-10-07T04:55:00.000Z
> **수정일:** 2025-09-13T15:38:00.000Z

## ROS2 kinetic 설치관련

- 관련 링크 : https://snowdeer.github.io/ros2/2020/09/15/how-to-install-ros2-foxy-on-macos/
- Python 3.8버전 설치 및 명령어 경로 등록
 
```bash
%brew install python@3.8 
%brew unlink python
%brew link --force python@3.8
%brew install asio tinyxml2
# OpenCV는 필수는 아닙니다. 설치시 시간이 엄청 오래 걸리니 고민해보세요.
%brew install opencv

%brew install openssl
%echo "export OPENSSL_ROOT_DIR=$(brew --prefix openssl)" >> ~/.zshrc

%brew install qt freetype assimp
%brew install sip pyqt5

%brew install console_bridge
%brew install log4cxx spdlog
%brew install cunit
%brew install graphviz
%export CFLAGS="-I$(brew --prefix graphviz)/include"
%export LDFLAGS="-L$(brew --prefix graphviz)/lib"

#conda환경 설정 및 활성화

%conda create --name py308 python=3.8
%conda activte py308

(py308)python3 -m pip install pygraphviz pydot
(py308)python3 -m pip install lxml
(py308)python3 -m pip install catkin_pkg empy ifcfg lark-parser lxml netifaces numpy pyparsing pyyaml setuptools argcomplete

(py308)pip3 install -U colcon-common-extensions

```

- 위 환경을 conda 가상환경을 활용하여, 적용시켰음.
- 그후 바이너리 파일을 다운받아서 설치후 실행. 파이썬 명령어 경로를 찾지 못하여 /Users/a/miniconda3/envs/py308/bin/python3 로 지정함(가상환경 파이썬 명령어 경로)
- 그후 ros2명령어 실행을 통해 실행

- 아래와 같은 보안 에러 발생