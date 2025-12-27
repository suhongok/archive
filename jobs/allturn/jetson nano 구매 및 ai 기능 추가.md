# jetson nano 구매 및 ai 기능 추가

> **생성일:** 2025-12-03T00:54:00.000Z
> **수정일:** 2025-12-03T05:20:00.000Z

```mermaid
flowchart TD

A[Voice Input - Microphone] --> B[STT - Whisper]

B --> C[LLM Command Parsing - Qwen or Phi]

C --> D[Parsed Command Topic]

D --> E[AI Processing - Jetson Orin Nano<br>LiDAR SLAM, Camera Detection, Sensor Fusion]

E --> F[Velocity Command - cmd_vel]

F --> G[MCU Control - ESP32 or STM32<br>Mecanum Inverse Kinematics, Motor Control]

G --> H[Mecanum Wheel Driving]

H --> I[Robot State Feedback]

I --> J[TTS Response - Piper or Coqui]

J --> A

```

Jetson Orin nano 구매 llm 및 비전처리용