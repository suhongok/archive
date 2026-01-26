// =============================================
// 인휠모터 4바퀴 이동형 로봇
// - 브라켓 높낮이 조절 가능
// - 좌우 바퀴 거리 조절 가능
// - 베이스 크기/위치 조절 가능
// - 브라켓 위치 조절 가능 (베이스 기준)
// =============================================

/* [기둥-베이스중심 거리] */
// 기둥에서 베이스 중심까지 X방향 거리 (mm)
leg_center_x = 200;        // [50:5:200]
// 기둥에서 베이스 중심까지 Y방향 거리 (mm)
leg_center_y = 150;         // [50:5:175]

// === 계산된 바퀴 거리 (참고용) ===
// 좌우 바퀴 중심 거리 = leg_center_x * 2
// 앞뒤 바퀴 중심 거리 = leg_center_y * 2

/* [다리기둥] */
// 다리기둥 전체 높이 (mm)
leg_height = 100;          // [60:5:200]
// 다리기둥 직경 (mm)
leg_diameter = 20;         // [15:1:35]

/* [상단 베이스] */
// 상단 베이스 너비 (mm)
top_base_width = 300;       // [20:5:60]
// 상단 베이스 두께 (mm)
top_base_thickness = 10;   // [5:1:20]
// 상단 베이스 길이 모드: 0=바퀴거리, 1=사용자지정
top_base_length_mode = 0;  // [0:바퀴거리 자동, 1:사용자지정]
// 상단 베이스 길이 (사용자지정 모드)
top_base_length_custom = 200; // [100:10:400]

/* [하단 베이스] */
// 하단 베이스 사용 여부
use_bottom_base = true;
// 하단 베이스 외곽 너비 (mm)
bottom_base_width = 50;    // [20:5:60]
// 하단 베이스 두께 (mm)
bottom_base_thickness = 10; // [5:1:20]
// 하단 베이스 크기 모드: 0=자동, 1=사용자지정
bottom_base_size_mode = 0; // [0:자동, 1:사용자지정]
// 하단 베이스 X 크기 (사용자지정)
bottom_base_x_custom = 200; // [80:10:350]
// 하단 베이스 Y 크기 (사용자지정)
bottom_base_y_custom = 300; // [80:10:300]
// 하단 베이스 Z 위치 (0=바닥, 양수=위로)
bottom_base_z_offset = 0;  // [0:5:50]

/* [상단 브라켓] */
// 상단 브라켓 사용
use_top_bracket = true;
// 상단 브라켓 Z 위치 (상단 베이스 하단 기준, 음수=아래)
top_bracket_z_offset = -5; // [-50:5:0]
// 상단 브라켓 너비 (mm)
top_bracket_width = 25;    // [15:5:40]
// 상단 브라켓 높이 (mm)
top_bracket_height = 30;   // [20:5:50]

/* [하단 브라켓] */
// 하단 브라켓 사용
use_bottom_bracket = true;
// 하단 브라켓 Z 위치 (하단 베이스 상단 기준, 양수=위)
bottom_bracket_z_offset = 5; // [0:5:50]
// 하단 브라켓 너비 (mm)
bottom_bracket_width = 25; // [15:5:40]
// 하단 브라켓 높이 (mm)
bottom_bracket_height = 30; // [20:5:50]

/* [인휠 모터] */
// 바퀴 직경 (mm)
wheel_diameter = 50;       // [30:5:100]
// 바퀴 너비 (mm)
wheel_width = 30;          // [20:5:60]
// 모터 본체 직경 (mm)
motor_body_diameter = 45;  // [30:5:80]
// 모터 본체 길이 (mm)
motor_body_length = 35;    // [25:5:60]
// 모터-다리 간격 (mm)
motor_gap = 5;             // [2:1:15]

/* [뷰 설정] */
// 뷰 모드
view_mode = 0;             // [0:3D, 1:측면, 2:상면]
// 치수 표시
show_dimensions = true;

// === 색상 정의 ===
color_base = [1, 0.6, 0];      // 주황색 - 베이스
color_bracket = [1, 0.2, 0.6]; // 분홍색 - 브라켓
color_leg = [0.2, 0.8, 0.3];   // 녹색 - 다리기둥
color_wheel = [0.5, 0.8, 1];   // 하늘색 - 인휠 모터

// === 계산된 값 ===
// 기둥 거리에서 바퀴 거리 계산
wheel_distance = leg_center_x * 2;  // 좌우 바퀴 중심 거리
wheelbase = leg_center_y * 2;       // 앞뒤 바퀴 중심 거리

// 상단 베이스 실제 길이
top_base_length = (top_base_length_mode == 0) ? wheel_distance : top_base_length_custom;

// 하단 베이스 실제 크기
bottom_base_x = (bottom_base_size_mode == 0) ? wheel_distance - 40 : bottom_base_x_custom;
bottom_base_y = (bottom_base_size_mode == 0) ? wheelbase - 20 : bottom_base_y_custom;

// 베이스 Z 위치 (상단 베이스 하단면 = 0 기준)
top_base_bottom_z = 0;
bottom_base_top_z = -leg_height + bottom_base_z_offset;

// === 모듈 정의 ===

// 인휠 모터 + 바퀴
module inwheel_motor() {
    // 모터 본체
    color(color_wheel)
    rotate([0, 90, 0])
    cylinder(d=motor_body_diameter, h=motor_body_length, center=true, $fn=32);

    // 바퀴
    color(color_wheel, 0.8)
    rotate([0, 90, 0])
    cylinder(d=wheel_diameter, h=wheel_width, center=true, $fn=48);
}

// 브라켓 모듈
module bracket(b_width, b_height) {
    bracket_thickness = 8;
    color(color_bracket)
    difference() {
        cube([b_width, b_width, b_height], center=true);
        // 다리기둥 관통 홀
        cylinder(d=leg_diameter+1, h=b_height+1, center=true, $fn=24);
        // 고정 볼트 홀 (양쪽)
        for (angle = [0, 90]) {
            rotate([0, 0, angle])
            translate([b_width/2, 0, 0])
            rotate([0, 90, 0])
            cylinder(d=5, h=10, center=true, $fn=16);
        }
    }
}

// 다리기둥
module leg_column(height) {
    color(color_leg)
    cylinder(d=leg_diameter, h=height, center=false, $fn=24);
}

// 상단 베이스 프레임 (가로 바)
module top_base_bar() {
    color(color_base)
    cube([top_base_length, top_base_width, top_base_thickness], center=true);
}

// 하단 베이스 프레임 (사각형)
module bottom_base_frame() {
    color(color_base)
    difference() {
        cube([bottom_base_x, bottom_base_y, bottom_base_thickness], center=true);
        cube([bottom_base_x - bottom_base_width*2,
              bottom_base_y - bottom_base_width*2,
              bottom_base_thickness+1], center=true);
    }
}

// 코너 다리 조립체 (다리기둥 + 브라켓 + 휠)
module corner_leg_assembly(x_sign, y_sign) {
    // 기둥 위치 = 베이스 중심에서 X/Y 거리
    x_pos = x_sign * leg_center_x;
    y_pos = y_sign * leg_center_y;

    translate([x_pos, y_pos, 0]) {
        // 다리기둥 (상단 베이스 하단에서 아래로)
        translate([0, 0, -leg_height])
        leg_column(leg_height);

        // 상단 브라켓 (상단 베이스 기준)
        if (use_top_bracket) {
            translate([0, 0, top_bracket_z_offset - top_bracket_height/2])
            bracket(top_bracket_width, top_bracket_height);
        }

        // 하단 브라켓 (하단 베이스 기준)
        if (use_bottom_bracket) {
            translate([0, 0, bottom_base_top_z + bottom_bracket_z_offset + bottom_bracket_height/2])
            bracket(bottom_bracket_width, bottom_bracket_height);
        }

        // 인휠 모터 (다리 끝에 위치)
        translate([x_sign * (leg_diameter/2 + motor_body_length/2 + motor_gap),
                   0,
                   -leg_height])
        inwheel_motor();
    }
}

// === 전체 조립 ===
module full_robot() {
    // 상단 베이스 (가로 바)
    translate([0, 0, top_base_thickness/2])
    top_base_bar();

    // 하단 베이스 (사각 프레임)
    if (use_bottom_base) {
        translate([0, 0, bottom_base_top_z - bottom_base_thickness/2])
        bottom_base_frame();
    }

    // 4개 코너 다리 조립체
    corner_leg_assembly(1, 1);   // 우측 전방
    corner_leg_assembly(-1, 1);  // 좌측 전방
    corner_leg_assembly(1, -1);  // 우측 후방
    corner_leg_assembly(-1, -1); // 좌측 후방
}

// === 치수 표시 ===
module dimension_lines() {
    if (show_dimensions) {
        // 좌우 거리 표시선 (빨강)
        color("red", 0.6)
        translate([0, wheelbase/2 + 40, -leg_height/2])
        cube([wheel_distance, 2, 2], center=true);

        // 좌우 거리 끝점
        for (x_sign = [-1, 1]) {
            color("red")
            translate([x_sign * wheel_distance/2, wheelbase/2 + 40, -leg_height/2])
            sphere(d=5, $fn=16);
        }

        // 앞뒤 거리 표시선 (파랑)
        color("blue", 0.6)
        translate([wheel_distance/2 + 40, 0, -leg_height/2])
        cube([2, wheelbase, 2], center=true);

        // 앞뒤 거리 끝점
        for (y_sign = [-1, 1]) {
            color("blue")
            translate([wheel_distance/2 + 40, y_sign * wheelbase/2, -leg_height/2])
            sphere(d=5, $fn=16);
        }

        // 높이 표시선 (초록)
        color("green", 0.6)
        translate([wheel_distance/2 + 60, wheelbase/2 + 20, -leg_height/2])
        cube([2, 2, leg_height], center=true);

        // 높이 끝점
        for (z = [0, -leg_height]) {
            color("green")
            translate([wheel_distance/2 + 60, wheelbase/2 + 20, z])
            sphere(d=5, $fn=16);
        }
    }
}

// === 렌더링 ===
if (view_mode == 0) {
    // 3D 전체 뷰
    full_robot();
    dimension_lines();
} else if (view_mode == 1) {
    // 측면 뷰
    projection(cut=false)
    rotate([0, -90, 0])
    full_robot();
} else if (view_mode == 2) {
    // 상면 뷰
    projection(cut=false)
    rotate([180, 0, 0])
    full_robot();
}

// === 파라미터 가이드 ===
/*
 * ============================================
 * 파라미터 조절 가이드
 * ============================================
 *
 * [기둥-베이스중심 거리]
 * - leg_center_x: 기둥에서 베이스 중심까지 X방향 거리
 * - leg_center_y: 기둥에서 베이스 중심까지 Y방향 거리
 * - (좌우 바퀴 거리 = leg_center_x × 2)
 * - (앞뒤 바퀴 거리 = leg_center_y × 2)
 *
 * [다리기둥]
 * - leg_height: 전체 높이 (상단~하단 베이스)
 * - leg_diameter: 다리 굵기
 *
 * [상단 베이스]
 * - top_base_width: 프레임 너비
 * - top_base_thickness: 프레임 두께
 * - top_base_length_mode: 0=바퀴거리 자동, 1=사용자지정
 * - top_base_length_custom: 사용자지정 길이
 *
 * [하단 베이스]
 * - use_bottom_base: 사용 여부
 * - bottom_base_width: 프레임 너비
 * - bottom_base_size_mode: 0=자동, 1=사용자지정
 * - bottom_base_x/y_custom: 사용자지정 크기
 * - bottom_base_z_offset: Z 위치 오프셋 (바닥 기준)
 *
 * [브라켓 위치] - 베이스 기준!
 * - top_bracket_z_offset: 상단 베이스 하단 기준 (음수=아래로)
 * - bottom_bracket_z_offset: 하단 베이스 상단 기준 (양수=위로)
 * - 브라켓 크기도 개별 조절 가능
 *
 * [인휠 모터]
 * - wheel_diameter/width: 바퀴 크기
 * - motor_body_diameter/length: 모터 크기
 * - motor_gap: 다리와의 간격
 *
 * OpenSCAD Customizer: View → Customizer 활성화
 * ============================================
 */
