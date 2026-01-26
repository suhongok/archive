// ===== 본체 파라메터 (상/하단 공유) =====
body_width = 1500;   // X축 너비
body_depth = 1000;   // Y축 깊이
body_height = 50;    // Z축 높이
body_wall = 50;      // 외벽 두께

// 본체 Z축 위치
body_top_z = 0;      // 상단 본체 Z 위치
body_bottom_z = 500; // 하단 본체 Z 위치 (기둥 바닥에 맞춤)

// ===== 기둥 파라메터 =====
pillar_width = 50;   // 기둥 X축 너비
pillar_depth = 50;   // 기둥 Y축 깊이
pillar_height = 1500; // 기둥 높이

// 기둥 위치 계산 (프레임 외곽 모서리에 붙임)
pillar_pos_x = body_width/2 - pillar_width/2 - 100;   // X축 위치
pillar_pos_y = body_depth/2 - pillar_depth/2 + pillar_depth;   // Y축 위치
pillar_pos_z = pillar_height/2 - 100;                 // Z축 위치 (기둥 바닥이 본체 중심에 맞춤)
pillar_offset_z = -700;                            // Z축 추가 오프셋

// ===== 지지대 파라메터 =====
support_width = 50;   // 지지대 X축 너비
support_depth = 50;   // 지지대 Y축 깊이
support_height = body_bottom_z - body_top_z;  // 지지대 높이 (본체 사이 거리)

// 지지대 위치 계산 (양옆 X축 외곽에 붙임)
support_pos_x = body_width/2 - support_width/2;   // X축 위치 (외곽)
support_pos_y_offset = 200;  // Y축 간격 (중심에서 떨어진 거리)
support_pos_z = (body_top_z + body_bottom_z) / 2;  // Z축 위치 (두 본체 중간)

// 전후면 지지대 위치 계산 (Y축 외곽에 붙임)
support_pos_y = body_depth/2 - support_depth/2;   // Y축 위치 (외곽)
support_pos_x_offset = 200;  // X축 간격 (중심에서 떨어진 거리)

// ===== 브라켓 파라메터 (바퀴 받침) =====
bracket_width = 150;   // 브라켓 너비 (X축)
bracket_depth = 150;   // 브라켓 깊이 (Y축)
bracket_height = 100;  // 브라켓 높이 (Z축)

// 브라켓 위치 계산 (기둥 바닥 아래)
pillar_bottom_z = pillar_pos_z + pillar_offset_z - pillar_height/2;  // 기둥 바닥 Z 위치
bracket_pos_z = pillar_bottom_z - bracket_height/2;  // 브라켓 Z 위치

// ===== 삼각형 고정부품 파라메터 =====
gusset_size = 100;                // 삼각형 변 길이
gusset_thickness = body_height;   // 두께 (본체 두께와 동일)

// ===== 본체 모듈 =====
module body() {
    inner_width = body_width - body_wall * 2;
    inner_depth = body_depth - body_wall * 2;

    difference() {
        cube([body_width, body_depth, body_height], center = true);
        cube([inner_width, inner_depth, body_height + 1], center = true);
    }
}

// ===== 기둥 모듈 =====
module pillar() {
    cube([pillar_width, pillar_depth, pillar_height], center = true);
}

// ===== 지지대 모듈 =====
module support() {
    cube([support_width, support_depth, support_height], center = true);
}

// ===== 브라켓 모듈 (바퀴 받침) =====
module bracket() {
    cube([bracket_width, bracket_depth, bracket_height], center = true);
}

// ===== 삼각형 고정부품 모듈 (X축=기둥, Y축=본체) =====
module gusset() {
    // Z축이 기둥방향(수직), Y축이 본체방향(수평), X축이 두께
    rotate([0, -90, 0])
        linear_extrude(height = gusset_thickness, center = true)
            polygon(points = [[0, 0], [gusset_size, 0], [0, gusset_size]]);
}

// ===== 조립 =====
union() {
    // 상단 본체
    translate([0, 0, body_top_z])
        body();

    // 하단 본체
    translate([0, 0, body_bottom_z])
        body();

    // 전면 기둥 2개 (Y 양수 방향)
    translate([pillar_pos_x, pillar_pos_y, pillar_pos_z + pillar_offset_z])
        pillar();
    translate([-pillar_pos_x, pillar_pos_y, pillar_pos_z + pillar_offset_z])
        pillar();

    // 후면 기둥 2개 (Y 음수 방향)
    translate([pillar_pos_x, -pillar_pos_y, pillar_pos_z + pillar_offset_z])
        pillar();
    translate([-pillar_pos_x, -pillar_pos_y, pillar_pos_z + pillar_offset_z])
        pillar();

    // 우측 지지대 2개 (X 양수 방향)
    translate([support_pos_x, support_pos_y_offset, support_pos_z])
        support();
    translate([support_pos_x, -support_pos_y_offset, support_pos_z])
        support();

    // 좌측 지지대 2개 (X 음수 방향)
    translate([-support_pos_x, support_pos_y_offset, support_pos_z])
        support();
    translate([-support_pos_x, -support_pos_y_offset, support_pos_z])
        support();

    // 전면 지지대 2개 (Y 양수 방향)
    translate([support_pos_x_offset, support_pos_y, support_pos_z])
        support();
    translate([-support_pos_x_offset, support_pos_y, support_pos_z])
        support();

    // 후면 지지대 2개 (Y 음수 방향)
    translate([support_pos_x_offset, -support_pos_y, support_pos_z])
        support();
    translate([-support_pos_x_offset, -support_pos_y, support_pos_z])
        support();

    // 전면 브라켓 2개 (Y 양수 방향, 기둥 밑)
    translate([pillar_pos_x, pillar_pos_y, bracket_pos_z])
        bracket();
    translate([-pillar_pos_x, pillar_pos_y, bracket_pos_z])
        bracket();

    // 후면 브라켓 2개 (Y 음수 방향, 기둥 밑)
    translate([pillar_pos_x, -pillar_pos_y, bracket_pos_z])
        bracket();
    translate([-pillar_pos_x, -pillar_pos_y, bracket_pos_z])
        bracket();

    // ===== 상단 본체 삼각형 고정부품 (4개, 본체 위쪽 ㄱ자) =====
    // 전면 우측 기둥 (X+, Y+)
    translate([pillar_pos_x + gusset_thickness/2, pillar_pos_y - pillar_depth/2, body_top_z + body_height/2])
        rotate([0, 0, 180])
        gusset();
    // 전면 좌측 기둥 (X-, Y+)
    translate([-pillar_pos_x - gusset_thickness/2, pillar_pos_y - pillar_depth/2, body_top_z + body_height/2])
        rotate([0, 0, 180])
        mirror([1, 0, 0])
        gusset();
    // 후면 우측 기둥 (X+, Y-)
    translate([pillar_pos_x + gusset_thickness/2, -pillar_pos_y + pillar_depth/2, body_top_z + body_height/2])
        rotate([0, 0, 0])
        gusset();
    // 후면 좌측 기둥 (X-, Y-)
    translate([-pillar_pos_x - gusset_thickness/2, -pillar_pos_y + pillar_depth/2, body_top_z + body_height/2])
        rotate([0, 0, 0])
        mirror([1, 0, 0])
        gusset();

    // ===== 하단 본체 삼각형 고정부품 (4개, 본체 아래쪽 ㄱ자) =====
    // 전면 우측 기둥 (X+, Y+)
    translate([pillar_pos_x + gusset_thickness/2, pillar_pos_y - pillar_depth/2, body_bottom_z - body_height/2])
        rotate([180, 0, 180])
        gusset();
    // 전면 좌측 기둥 (X-, Y+)
    translate([-pillar_pos_x - gusset_thickness/2, pillar_pos_y - pillar_depth/2, body_bottom_z - body_height/2])
        rotate([180, 0, 180])
        mirror([1, 0, 0])
        gusset();
    // 후면 우측 기둥 (X+, Y-)
    translate([pillar_pos_x + gusset_thickness/2, -pillar_pos_y + pillar_depth/2, body_bottom_z - body_height/2])
        rotate([180, 0, 0])
        gusset();
    // 후면 좌측 기둥 (X-, Y-)
    translate([-pillar_pos_x - gusset_thickness/2, -pillar_pos_y + pillar_depth/2, body_bottom_z - body_height/2])
        rotate([180, 0, 0])
        mirror([1, 0, 0])
        gusset();
}
