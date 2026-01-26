#!/bin/bash
#
# Orbbec Astro Pro + ORB-SLAM3 실행 스크립트
#
# 사용법:
#   chmod +x launch_orbslam3.sh
#   ./launch_orbslam3.sh
#

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Orbbec Astro Pro + ORB-SLAM3 실행${NC}"
echo -e "${BLUE}========================================${NC}"

# 경로 설정 (필요시 수정)
ORB_SLAM3_PATH="${HOME}/ORB_SLAM3"
ROS2_WS="${HOME}/ros2_ws"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 환경 변수 확인
check_env() {
    echo -e "\n${YELLOW}[1/4] 환경 확인 중...${NC}"

    # ROS2 설치 확인
    if [ -z "$ROS_DISTRO" ]; then
        echo -e "${RED}  ❌ ROS2가 설정되지 않았습니다.${NC}"
        echo -e "     source /opt/ros/humble/setup.bash 실행 필요"
        return 1
    fi
    echo -e "${GREEN}  ✓ ROS2 Distro: $ROS_DISTRO${NC}"

    # ORB-SLAM3 경로 확인
    if [ ! -d "$ORB_SLAM3_PATH" ]; then
        echo -e "${RED}  ❌ ORB-SLAM3를 찾을 수 없습니다: $ORB_SLAM3_PATH${NC}"
        echo -e "     ORB_SLAM3_PATH 변수를 수정하세요"
        return 1
    fi
    echo -e "${GREEN}  ✓ ORB-SLAM3 경로: $ORB_SLAM3_PATH${NC}"

    # Vocabulary 파일 확인
    VOCAB_FILE="$ORB_SLAM3_PATH/Vocabulary/ORBvoc.txt"
    if [ ! -f "$VOCAB_FILE" ]; then
        echo -e "${RED}  ❌ Vocabulary 파일이 없습니다: $VOCAB_FILE${NC}"
        echo -e "     tar -xf ORBvoc.txt.tar.gz 실행 필요"
        return 1
    fi
    echo -e "${GREEN}  ✓ Vocabulary 파일 확인됨${NC}"

    # 카메라 설정 파일 확인
    CONFIG_FILE="$SCRIPT_DIR/orbbec_astro.yaml"
    if [ ! -f "$CONFIG_FILE" ]; then
        echo -e "${RED}  ❌ 설정 파일이 없습니다: $CONFIG_FILE${NC}"
        return 1
    fi
    echo -e "${GREEN}  ✓ 설정 파일: $CONFIG_FILE${NC}"

    return 0
}

# 카메라 연결 확인
check_camera() {
    echo -e "\n${YELLOW}[2/4] 카메라 연결 확인 중...${NC}"

    # Orbbec USB 장치 확인
    if lsusb | grep -qi "orbbec\|2bc5"; then
        echo -e "${GREEN}  ✓ Orbbec 카메라 감지됨${NC}"
        lsusb | grep -i "orbbec\|2bc5"
        return 0
    else
        echo -e "${RED}  ❌ Orbbec 카메라가 연결되지 않았습니다.${NC}"
        echo -e "     카메라를 USB에 연결하고 다시 시도하세요."
        return 1
    fi
}

# 실행 모드 선택
select_mode() {
    echo -e "\n${YELLOW}[3/4] 실행 모드 선택${NC}"
    echo ""
    echo "  1) 카메라 테스트만 (ROS 없이)"
    echo "  2) ROS2 orbbec_camera 패키지 실행"
    echo "  3) 커스텀 노드 + ORB-SLAM3 실행"
    echo "  4) 종료"
    echo ""
    read -p "  선택 (1-4): " choice

    case $choice in
        1)
            run_camera_test
            ;;
        2)
            run_ros2_orbbec
            ;;
        3)
            run_orbslam3
            ;;
        4)
            echo -e "${GREEN}종료합니다.${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}잘못된 선택입니다.${NC}"
            select_mode
            ;;
    esac
}

# 1) 카메라 테스트
run_camera_test() {
    echo -e "\n${YELLOW}[실행] 카메라 테스트...${NC}"

    TEST_SCRIPT="$SCRIPT_DIR/test_orbbec_camera.py"
    if [ -f "$TEST_SCRIPT" ]; then
        python3 "$TEST_SCRIPT"
    else
        echo -e "${RED}테스트 스크립트를 찾을 수 없습니다: $TEST_SCRIPT${NC}"
    fi
}

# 2) ROS2 orbbec_camera 실행
run_ros2_orbbec() {
    echo -e "\n${YELLOW}[실행] ROS2 orbbec_camera...${NC}"

    # 워크스페이스 소싱
    if [ -f "$ROS2_WS/install/setup.bash" ]; then
        source "$ROS2_WS/install/setup.bash"
    fi

    echo -e "${BLUE}  터미널 1: ros2 launch orbbec_camera astra.launch.py${NC}"
    echo -e "${BLUE}  터미널 2: rviz2 (토픽 구독)${NC}"
    echo ""
    echo "  실행하시겠습니까? (y/n)"
    read -p "  > " confirm

    if [ "$confirm" = "y" ]; then
        ros2 launch orbbec_camera astra.launch.py
    fi
}

# 3) ORB-SLAM3 실행
run_orbslam3() {
    echo -e "\n${YELLOW}[4/4] ORB-SLAM3 실행...${NC}"

    # 워크스페이스 소싱
    if [ -f "$ROS2_WS/install/setup.bash" ]; then
        source "$ROS2_WS/install/setup.bash"
    fi

    export ORB_SLAM3_ROOT_DIR="$ORB_SLAM3_PATH"

    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  터미널을 2개 열어서 다음을 실행하세요:${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "${GREEN}[터미널 1] Orbbec 카메라 노드:${NC}"
    echo "  python3 $SCRIPT_DIR/orbbec_orbslam3_node.py"
    echo ""
    echo -e "${GREEN}[터미널 2] ORB-SLAM3 RGB-D:${NC}"
    echo "  ros2 run orbslam3_ros2 rgbd \\"
    echo "      $ORB_SLAM3_PATH/Vocabulary/ORBvoc.txt \\"
    echo "      $SCRIPT_DIR/orbbec_astro.yaml"
    echo ""
    echo -e "${YELLOW}주의: orbbec_astro.yaml의 카메라 파라미터를${NC}"
    echo -e "${YELLOW}      test_orbbec_camera.py 결과로 업데이트하세요!${NC}"
    echo ""

    # 사용자 선택
    echo "  직접 실행하시겠습니까?"
    echo "    1) 카메라 노드만 실행"
    echo "    2) 명령어만 표시 (수동 실행)"
    read -p "  선택: " exec_choice

    if [ "$exec_choice" = "1" ]; then
        echo -e "\n${GREEN}카메라 노드 실행 중...${NC}"
        echo -e "${YELLOW}다른 터미널에서 ORB-SLAM3를 실행하세요.${NC}"
        python3 "$SCRIPT_DIR/orbbec_orbslam3_node.py"
    fi
}

# 메인 실행
main() {
    check_env || exit 1
    check_camera || exit 1
    select_mode
}

main
