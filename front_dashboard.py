import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import json
import random

# 페이지 설정
st.set_page_config(
    page_title="🎯 FIELD-DREAM Front - 계층형 메모리",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 세션 상태 초기화
if 'emergency_cases' not in st.session_state:
    st.session_state.emergency_cases = []
if 'data_stream' not in st.session_state:
    st.session_state.data_stream = []
if 'processing_logs' not in st.session_state:
    st.session_state.processing_logs = []

# 메인 화면으로 돌아가기 버튼
if st.sidebar.button("🏠 메인 화면으로"):
    st.switch_page("main.py")

# CSS 스타일링
st.markdown("""
<style>
    /* 전체 배경 */
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;400;500;700&family=Noto+Sans+KR:wght@300;400;700;900&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    /* 메인 타이틀 */
    .main-title {
        font-family: 'Fira Code', monospace;
        font-size: 2.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        text-align: center;
        color: #a78bfa;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* 데이터 흐름 카드 */
    .data-flow-card {
        background: rgba(102, 126, 234, 0.1);
        border: 2px solid #667eea;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    /* JSON 뷰어 스타일 */
    .json-viewer {
        background: rgba(0, 0, 0, 0.4);
        border-left: 4px solid #10b981;
        border-radius: 8px;
        padding: 15px;
        font-family: 'Fira Code', monospace;
        font-size: 0.85rem;
        color: #10b981;
        overflow-x: auto;
        margin: 10px 0;
    }
    
    .json-hot {
        border-left-color: #ef4444;
        color: #fca5a5;
    }
    
    .json-warm {
        border-left-color: #f59e0b;
        color: #fcd34d;
    }
    
    .json-cold {
        border-left-color: #3b82f6;
        color: #93c5fd;
    }
    
    /* 메모리 계층 표시 */
    .memory-layer {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(37, 99, 235, 0.2) 100%);
        border: 2px solid #3b82f6;
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        transition: all 0.3s ease;
    }
    
    .memory-layer:hover {
        transform: translateX(5px);
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.4);
    }
    
    .memory-hot {
        border-color: #ef4444;
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(220, 38, 38, 0.2) 100%);
    }
    
    .memory-warm {
        border-color: #f59e0b;
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(217, 119, 6, 0.2) 100%);
    }
    
    .memory-cold {
        border-color: #3b82f6;
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(37, 99, 235, 0.2) 100%);
    }
    
    /* 처리 단계 파이프라인 */
    .pipeline-stage {
        background: rgba(168, 85, 247, 0.15);
        border: 2px solid #a855f7;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        position: relative;
    }
    
    .pipeline-stage::before {
        content: "→";
        position: absolute;
        right: -20px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 2rem;
        color: #a855f7;
    }
    
    .pipeline-stage:last-child::before {
        content: "";
    }
    
    /* 스트림 라인 */
    .stream-line {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 8px;
        padding: 8px 12px;
        margin: 5px 0;
        font-family: 'Fira Code', monospace;
        font-size: 0.8rem;
        border-left: 3px solid #8b5cf6;
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-10px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* 실시간 모니터 */
    .realtime-monitor {
        background: rgba(0, 0, 0, 0.5);
        border: 2px solid #10b981;
        border-radius: 10px;
        padding: 15px;
        font-family: 'Fira Code', monospace;
        max-height: 400px;
        overflow-y: auto;
    }
    
    .log-entry {
        color: #10b981;
        margin: 5px 0;
        padding: 5px;
        border-bottom: 1px solid rgba(16, 185, 129, 0.2);
    }
    
    .log-entry.error {
        color: #ef4444;
    }
    
    .log-entry.warning {
        color: #f59e0b;
    }
    
    .log-entry.info {
        color: #3b82f6;
    }
    
    /* 메트릭 */
    .metric-box {
        background: rgba(139, 92, 246, 0.15);
        border: 2px solid #8b5cf6;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }
    
    .metric-value {
        font-family: 'Fira Code', monospace;
        font-size: 2rem;
        font-weight: 700;
        color: #a78bfa;
    }
    
    .metric-label {
        color: #c4b5fd;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 5px;
    }
    
    /* 태그 */
    .tag {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 700;
        margin: 2px;
    }
    
    .tag-hot {
        background: #ef4444;
        color: white;
    }
    
    .tag-warm {
        background: #f59e0b;
        color: white;
    }
    
    .tag-cold {
        background: #3b82f6;
        color: white;
    }
    
    .tag-processing {
        background: #8b5cf6;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# 시뮬레이션 데이터 풀
SIMULATION_DATA = {
    "신고음성": [
        {
            "type": "신고음성",
            "call_location": "하나고등학교 정문 앞",
            "patient_gender": "남성",
            "patient_age_group": "10대",
            "witness_report": "학생이 운동장에서 쓰러졌어요. 의식이 없고 경련을 일으키고 있습니다",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "severity": "긴급",
            "condition": "경련성 발작"
        },
        {
            "type": "신고음성",
            "call_location": "서울역 광장 분수대 근처",
            "patient_gender": "여성",
            "patient_age_group": "60대",
            "witness_report": "할머니가 갑자기 쓰러지셨어요. 얼굴 한쪽이 마비된 것 같고 말을 못하세요",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "severity": "매우긴급",
            "condition": "뇌졸중 의심"
        },
        {
            "type": "신고음성",
            "call_location": "강남구 테헤란로 427 현대백화점 5층 푸드코트",
            "patient_gender": "남성",
            "patient_age_group": "40대",
            "witness_report": "식사 중 갑자기 가슴을 움켜쥐고 쓰러졌습니다. 식은땀 흘리고 있어요",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "severity": "매우긴급",
            "condition": "심근경색 의심"
        },
        {
            "type": "신고음성",
            "call_location": "인천국제공항 제2여객터미널 출국장",
            "patient_gender": "여성",
            "patient_age_group": "30대",
            "witness_report": "임산부가 배를 잡고 쓰러졌어요. 출혈이 있습니다",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "severity": "매우긴급",
            "condition": "산과 응급"
        }
    ],
    "웨어러블": [
        {
            "type": "웨어러블 기록",
            "user_name": "김철수",
            "user_age": 55,
            "gps_location": "서울시 종로구 세종대로 172 (광화문 교보빌딩 앞)",
            "gps_coordinates": "37.5703, 126.9770",
            "heart_rate": 165,
            "spo2": 88,
            "activity": "걷기 중 급정지",
            "device_alert": "⚠️ 비정상 심박수 감지 - 심방세동 의심",
            "alert_duration": "2분 지속",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "severity": "긴급",
            "condition": "부정맥"
        },
        {
            "type": "웨어러블 기록",
            "user_name": "이영희",
            "user_age": 28,
            "gps_location": "경기도 성남시 분당구 판교역로 235 (카카오 판교오피스 인근)",
            "gps_coordinates": "37.3949, 127.1110",
            "heart_rate": 45,
            "blood_glucose": 42,
            "activity": "정지 상태",
            "device_alert": "⚠️ 심각한 저혈당 감지 - 의식 저하 가능성",
            "alert_duration": "5분 지속",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "severity": "매우긴급",
            "condition": "저혈당"
        },
        {
            "type": "웨어러블 기록",
            "user_name": "박민수",
            "user_age": 62,
            "gps_location": "부산광역시 해운대구 우동 1408 (해운대 해수욕장 산책로)",
            "gps_coordinates": "35.1588, 129.1603",
            "heart_rate": 142,
            "blood_pressure": "185/115",
            "activity": "조깅 중",
            "device_alert": "⚠️ 고혈압 위험 수준 - 운동 중 심혈관 이상 감지",
            "alert_duration": "1분 지속",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "severity": "긴급",
            "condition": "고혈압성 응급"
        },
        {
            "type": "웨어러블 기록",
            "user_name": "최지은",
            "user_age": 19,
            "gps_location": "대전광역시 유성구 대학로 99 (KAIST 본관 앞)",
            "gps_coordinates": "36.3741, 127.3650",
            "heart_rate": 0,
            "spo2": 0,
            "fall_detected": True,
            "device_alert": "🚨 낙상 감지 및 생체신호 미감지 - 즉시 대응 필요",
            "alert_duration": "30초 경과",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "severity": "매우긴급",
            "condition": "심정지 의심"
        }
    ],
    "현장처치": [
        {
            "type": "현장 처치 기록",
            "patient_estimated_age": "20대 후반",
            "patient_gender": "남성",
            "first_aid": ["기도 확보", "경추 고정", "산소 투여 (15L/min)", "정맥로 확보"],
            "current_status": "의식 명료, GCS 15점, 경추 통증 호소",
            "injury": "교통사고 (오토바이), 목 통증 및 우측 상지 골절 의심",
            "urgency_level": "준긴급",
            "transport_time": "현장 도착 후 12분",
            "destination": "이송 중 - 삼성서울병원 응급실",
            "eta": "5분 후 도착 예정",
            "ambulance_id": "강남119-05",
            "location": "서울시 강남구 테헤란로 (강남역 사거리)",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "severity": "준긴급",
            "condition": "경추 손상 의심"
        },
        {
            "type": "현장 처치 기록",
            "patient_estimated_age": "70대 초반",
            "patient_gender": "여성",
            "first_aid": ["CPR 실시 (5분)", "제세동 1회 실시", "기관 삽관", "에피네프린 1mg 투여"],
            "current_status": "자발 순환 회복, 의식 혼미, GCS 8점",
            "injury": "심정지 (목격자 CPR 실시됨)",
            "urgency_level": "최고긴급",
            "transport_time": "현장 도착 후 18분",
            "destination": "이송 중 - 서울아산병원 응급실",
            "eta": "3분 후 도착 예정",
            "ambulance_id": "송파119-02",
            "location": "서울시 송파구 올림픽로 (롯데월드타워 인근)",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "severity": "매우긴급",
            "condition": "심정지 소생 후"
        },
        {
            "type": "현장 처치 기록",
            "patient_estimated_age": "50대 중반",
            "patient_gender": "남성",
            "first_aid": ["상처 지혈 및 드레싱", "파상풍 예방 조치", "진통제 투여"],
            "current_status": "의식 명료, 우측 대퇴부 열상 출혈 조절됨",
            "injury": "작업장 사고 - 우측 하지 열상 (길이 15cm, 깊이 3cm)",
            "urgency_level": "비긴급",
            "transport_time": "현장 도착 후 8분",
            "destination": "이송 중 - 인천의료원",
            "eta": "7분 후 도착 예정",
            "ambulance_id": "인천119-14",
            "location": "인천광역시 남동구 논현동 공단",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "severity": "경증",
            "condition": "외상"
        },
        {
            "type": "현장 처치 기록",
            "patient_estimated_age": "30대 후반",
            "patient_gender": "여성",
            "first_aid": ["산소 투여", "정맥로 확보", "항히스타민제 투여", "에피네프린 근육주사"],
            "current_status": "호흡곤란 호전 중, 의식 명료, 두드러기 지속",
            "injury": "아나필락시스 쇼크 (새우 섭취 후)",
            "urgency_level": "긴급",
            "transport_time": "현장 도착 후 6분",
            "destination": "이송 중 - 세브란스병원 응급실",
            "eta": "4분 후 도착 예정",
            "ambulance_id": "서대문119-03",
            "location": "서울시 서대문구 연세로 (신촌역 인근)",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "severity": "긴급",
            "condition": "알레르기 쇼크"
        }
    ],
    "영상스트리밍": [
        {
            "type": "영상 스트리밍",
            "visual_status": "환자 의식 저하, 우측 안면 처짐, 우측 팔 마비 확인됨",
            "patient_age_group": "60대",
            "patient_gender": "남성",
            "symptoms_observed": ["언어 장애", "편측 마비", "안면 비대칭"],
            "onset_time": "15분 전 증상 시작",
            "last_normal_time": "20분 전",
            "current_action": "구급차 이송 중, 산소 투여 중",
            "ambulance_id": "경기119-22",
            "location": "경기도 수원시 영통구 광교중앙로",
            "eta_to_hospital": "8분",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "severity": "매우긴급",
            "condition": "뇌졸중"
        },
        {
            "type": "영상 스트리밍",
            "visual_status": "소아 환자 발열 및 경련 중, 입술 청색증 보임",
            "patient_age_group": "5세",
            "patient_gender": "남성",
            "symptoms_observed": ["고열 (39.8°C)", "전신 경련", "청색증"],
            "onset_time": "5분 전 경련 시작",
            "seizure_duration": "3분 지속 후 멈춤",
            "current_action": "측와위 유지, 산소 투여, 해열제 투여 준비",
            "ambulance_id": "광주119-08",
            "location": "광주광역시 서구 상무대로",
            "eta_to_hospital": "5분",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "severity": "긴급",
            "condition": "열성경련"
        },
        {
            "type": "영상 스트리밍",
            "visual_status": "복부 팽만 및 압통, 환자 창백하고 식은땀 흘림",
            "patient_age_group": "40대",
            "patient_gender": "남성",
            "symptoms_observed": ["복부 강직", "저혈압 (80/50)", "빈맥 (HR 125)"],
            "onset_time": "30분 전 증상 시작",
            "injury_mechanism": "사다리에서 3m 높이 추락",
            "current_action": "수액 급속 투여 중, 쇼크 체위 유지",
            "ambulance_id": "대전119-11",
            "location": "대전광역시 서구 둔산대로",
            "eta_to_hospital": "6분",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "severity": "매우긴급",
            "condition": "복부 내출혈 의심"
        },
        {
            "type": "영상 스트리밍",
            "visual_status": "산모 출혈 지속, 태아 만출 임박 상태",
            "patient_age_group": "30대",
            "patient_gender": "여성",
            "symptoms_observed": ["질 출혈", "규칙적 진통 (2분 간격)", "태아 머리 보임"],
            "onset_time": "20분 전 진통 시작",
            "gestation_week": "임신 38주",
            "current_action": "분만 준비 중, 산모 안정화",
            "ambulance_id": "울산119-06",
            "location": "울산광역시 남구 삼산로",
            "eta_to_hospital": "4분 (산부인과 전문병원)",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "severity": "매우긴급",
            "condition": "응급 분만"
        }
    ]
}

# 헤더
st.markdown('<h1 class="main-title">🎯 FIELD-DREAM Front</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">계층형 메모리 & 실시간 데이터 처리 모니터링</p>', unsafe_allow_html=True)

# 시뮬레이션 버튼 섹션
st.markdown("---")
st.subheader("🎮 응급 상황 시뮬레이션")
st.caption("버튼을 클릭하여 다양한 응급 상황을 생성하고 Mid Office 대시보드에서 확인하세요")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📞 신고음성", use_container_width=True):
        case = random.choice(SIMULATION_DATA["신고음성"])
        st.session_state.emergency_cases.append(case)
        st.success(f"📞 신고 접수\n📍 {case['call_location']}\n👤 {case['patient_age_group']} {case['patient_gender']}\n💬 {case['witness_report'][:30]}...")

with col2:
    if st.button("⌚ 웨어러블 기록", use_container_width=True):
        case = random.choice(SIMULATION_DATA["웨어러블"])
        st.session_state.emergency_cases.append(case)
        st.success(f"⌚ 웨어러블 감지\n👤 {case['user_name']} ({case['user_age']}세)\n📍 {case['gps_location']}\n⚠️ {case['device_alert'][:35]}...")

with col3:
    if st.button("🏥 현장 처치 기록", use_container_width=True):
        case = random.choice(SIMULATION_DATA["현장처치"])
        st.session_state.emergency_cases.append(case)
        st.success(f"🚑 현장 처치 진행\n🚨 {case['ambulance_id']}\n👤 {case['patient_estimated_age']} {case['patient_gender']}\n⏱️ 이송 시간: {case['transport_time']}")

with col4:
    if st.button("📹 영상 스트리밍", use_container_width=True):
        case = random.choice(SIMULATION_DATA["영상스트리밍"])
        st.session_state.emergency_cases.append(case)
        st.success(f"📹 영상 수신\n🚨 {case['ambulance_id']}\n👁️ {case['visual_status'][:40]}...\n⏱️ 발생: {case['onset_time']}")

# 최근 케이스 표시
if st.session_state.emergency_cases:
    with st.expander(f"📋 최근 생성된 케이스 ({len(st.session_state.emergency_cases)}건)", expanded=True):
        for idx, case in enumerate(reversed(st.session_state.emergency_cases[-5:]), 1):
            # 케이스 타입별로 다른 필드 사용
            if case['type'] == "신고음성":
                location = case.get('call_location', '위치 정보 없음')
                patient_info = f"{case.get('patient_age_group', '-')} {case.get('patient_gender', '-')}"
            elif case['type'] == "웨어러블 기록":
                location = case.get('gps_location', '위치 정보 없음')
                patient_info = f"{case.get('user_name', '-')} ({case.get('user_age', '-')}세)"
            elif case['type'] == "현장 처치 기록":
                location = case.get('location', '위치 정보 없음')
                patient_info = f"{case.get('patient_estimated_age', '-')} {case.get('patient_gender', '-')}"
            elif case['type'] == "영상 스트리밍":
                location = case.get('location', '위치 정보 없음')
                patient_info = f"{case.get('patient_age_group', '-')} {case.get('patient_gender', '-')}"
            else:
                location = "위치 정보 없음"
                patient_info = "-"
            
            st.markdown(f"""
            **케이스 #{len(st.session_state.emergency_cases) - idx + 1}** - {case['type']}
            - 📍 위치: {location}
            - 👤 환자: {patient_info}
            - 🚨 상태: {case.get('condition', '-')}
            - ⏰ 시각: {case.get('time', '-')}
            """)
            st.markdown("---")

st.markdown("---")

# 현재 시간
current_time = datetime.now()

# 상단 메트릭
col_m1, col_m2, col_m3, col_m4 = st.columns(4)

with col_m1:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-label">총 처리 데이터</div>
        <div class="metric-value">1,247</div>
        <div style="color: #10b981; font-size: 0.8rem;">▲ +89 (5분)</div>
    </div>
    """, unsafe_allow_html=True)

with col_m2:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-label">실시간 스트림</div>
        <div class="metric-value">23/s</div>
        <div style="color: #f59e0b; font-size: 0.8rem;">평균 처리 속도</div>
    </div>
    """, unsafe_allow_html=True)

with col_m3:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-label">메모리 사용률</div>
        <div class="metric-value">67%</div>
        <div style="color: #3b82f6; font-size: 0.8rem;">Hot: 12% | Warm: 28%</div>
    </div>
    """, unsafe_allow_html=True)

with col_m4:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-label">처리 지연</div>
        <div class="metric-value">24ms</div>
        <div style="color: #10b981; font-size: 0.8rem;">✓ 정상 범위</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# 메인 레이아웃
col_left, col_right = st.columns([1.3, 1])

with col_left:
    # 실시간 데이터 입력 스트림
    st.markdown("### 📥 실시간 데이터 입력 스트림")
    
    # 샘플 데이터 생성
    sample_emergency_data = {
        "source": "emergency_call",
        "type": "triage_text",
        "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
        "payload": {
            "text": "42세 여성, 교통사고 부상, 의식 명료"
        }
    }
    
    sample_vital_data = {
        "source": "ambulance_sensor",
        "type": "vital_signs",
        "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
        "payload": {
            "heart_rate": 92,
            "bp_systolic": 125,
            "bp_diastolic": 78,
            "spo2": 97,
            "temp": 36.8
        }
    }
    
    sample_location_data = {
        "source": "gps_tracker",
        "type": "location",
        "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
        "payload": {
            "lat": 37.5665,
            "lng": 126.9780,
            "speed": 45.2,
            "heading": "SE"
        }
    }
    
    tab1, tab2, tab3 = st.tabs(["🔴 Hot (긴급 호출)", "🟡 Warm (바이탈)", "🔵 Cold (위치)"])
    
    with tab1:
        st.markdown('<div class="tag tag-hot">HOT MEMORY</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="json-viewer json-hot">
{json.dumps(sample_emergency_data, indent=2, ensure_ascii=False)}
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="tag tag-warm">WARM MEMORY</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="json-viewer json-warm">
{json.dumps(sample_vital_data, indent=2, ensure_ascii=False)}
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="tag tag-cold">COLD MEMORY</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="json-viewer json-cold">
{json.dumps(sample_location_data, indent=2, ensure_ascii=False)}
        </div>
        """, unsafe_allow_html=True)
    
    # 데이터 처리 파이프라인
    st.markdown("### 🔄 데이터 처리 파이프라인 (3단계)")
    
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; margin: 20px 0;">
        <div class="pipeline-stage" style="flex: 1;">
            <h4 style="color: #a855f7; margin: 0;">Stage 1: 수집</h4>
            <p style="color: #c4b5fd; font-size: 0.9rem; margin: 5px 0;">원시 데이터 수신</p>
            <div class="tag tag-processing">RUNNING</div>
        </div>
        <div class="pipeline-stage" style="flex: 1;">
            <h4 style="color: #a855f7; margin: 0;">Stage 2: 분류</h4>
            <p style="color: #c4b5fd; font-size: 0.9rem; margin: 5px 0;">Hot/Warm/Cold 분류</p>
            <div class="tag tag-processing">RUNNING</div>
        </div>
        <div class="pipeline-stage" style="flex: 1;">
            <h4 style="color: #a855f7; margin: 0;">Stage 3: 전달</h4>
            <p style="color: #c4b5fd; font-size: 0.9rem; margin: 5px 0;">Mid 계층으로 전송</p>
            <div class="tag tag-processing">RUNNING</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 처리 상세 로그
    st.markdown("#### 📋 처리 상세 로그")
    
    processing_steps = [
        {
            "time": current_time.strftime("%H:%M:%S.%f")[:-3],
            "stage": "Stage 1",
            "action": "수신: emergency_call 데이터",
            "status": "✓"
        },
        {
            "time": (current_time - timedelta(milliseconds=150)).strftime("%H:%M:%S.%f")[:-3],
            "stage": "Stage 2",
            "action": "분류: HOT 메모리로 할당 (긴급도: 높음)",
            "status": "✓"
        },
        {
            "time": (current_time - timedelta(milliseconds=300)).strftime("%H:%M:%S.%f")[:-3],
            "stage": "Stage 3",
            "action": "전송: 구급대원/병원 대시보드로 전달",
            "status": "✓"
        },
        {
            "time": (current_time - timedelta(milliseconds=450)).strftime("%H:%M:%S.%f")[:-3],
            "stage": "Stage 1",
            "action": "수신: vital_signs 데이터",
            "status": "✓"
        },
        {
            "time": (current_time - timedelta(milliseconds=600)).strftime("%H:%M:%S.%f")[:-3],
            "stage": "Stage 2",
            "action": "분류: WARM 메모리로 할당 (주기적 업데이트)",
            "status": "✓"
        }
    ]
    
    log_html = ""
    for step in processing_steps:
        log_html += f"""
        <div class="stream-line">
            <span style="color: #6366f1;">[{step['time']}]</span>
            <span style="color: #a855f7; font-weight: 700;">{step['stage']}</span>
            <span style="color: #e0e7ff;"> → {step['action']}</span>
            <span style="color: #10b981;"> {step['status']}</span>
        </div>
        """
    
    st.markdown(f'<div style="max-height: 250px; overflow-y: auto;">{log_html}</div>', unsafe_allow_html=True)

with col_right:
    # 계층형 메모리 현황
    st.markdown("### 🗄️ 계층형 메모리 (Hot-Warm-Cold)")
    
    st.markdown("""
    <div class="memory-layer memory-hot">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h4 style="color: #ef4444; margin: 0;">🔴 Hot Memory (긴급 5분)</h4>
                <p style="color: #fca5a5; font-size: 0.85rem; margin: 5px 0;">초고속 접근 | 실시간 처리</p>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 1.8rem; font-weight: 700; color: #fca5a5;">148 MB</div>
                <div style="font-size: 0.8rem; color: #fecaca;">12% 사용 중</div>
            </div>
        </div>
        <div style="margin-top: 10px; background: rgba(0,0,0,0.3); padding: 8px; border-radius: 5px;">
            <div style="color: #fecaca; font-size: 0.85rem;">
                • 긴급 호출 데이터: 23건<br>
                • 심정지 의심 환자: 2건<br>
                • AI 상황 분석 결과: 실시간 업데이트
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="memory-layer memory-warm">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h4 style="color: #f59e0b; margin: 0;">🟡 Warm Memory (20분)</h4>
                <p style="color: #fcd34d; font-size: 0.85rem; margin: 5px 0;">빠른 접근 | 주기적 업데이트</p>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 1.8rem; font-weight: 700; color: #fbbf24;">342 MB</div>
                <div style="font-size: 0.8rem; color: #fde68a;">28% 사용 중</div>
            </div>
        </div>
        <div style="margin-top: 10px; background: rgba(0,0,0,0.3); padding: 8px; border-radius: 5px;">
            <div style="color: #fde68a; font-size: 0.85rem;">
                • 바이탈 사인 데이터: 15분간 기록<br>
                • 이송 중 환자 모니터링: 8건<br>
                • 병원 매칭 히스토리
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="memory-layer memory-cold">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h4 style="color: #3b82f6; margin: 0;">🔵 Cold Memory (아카이브)</h4>
                <p style="color: #93c5fd; font-size: 0.85rem; margin: 5px 0;">장기 보관 | 분석용 데이터</p>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 1.8rem; font-weight: 700; color: #60a5fa;">1.2 GB</div>
                <div style="font-size: 0.8rem; color: #bfdbfe;">27% 사용 중</div>
            </div>
        </div>
        <div style="margin-top: 10px; background: rgba(0,0,0,0.3); padding: 8px; border-radius: 5px;">
            <div style="color: #bfdbfe; font-size: 0.85rem;">
                • GPS 위치 로그: 전체 이송 경로<br>
                • 네트워크 성능 이력<br>
                • 과거 출동 데이터 (30일)
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # API / 텔레메트리
    st.markdown("### 📡 API 설정 / 텔레메트리")
    
    st.markdown("""
    <div class="data-flow-card">
        <h4 style="color: #667eea; margin-top: 0;">설정된 API: 3개</h4>
        <div style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 8px; margin: 10px 0;">
            <div style="color: #c7d2fe; font-family: 'Fira Code', monospace; font-size: 0.85rem;">
                <strong style="color: #818cf8;">POST</strong> /api/v1/network/slice<br>
                <span style="color: #a5b4fc;">→ 6G 네트워크 슬라이스 요청</span><br><br>
                
                <strong style="color: #fbbf24;">PUT</strong> /api/v1/ris/mode<br>
                <span style="color: #fde68a;">→ RIS Active/Passive 모드 전환</span><br><br>
                
                <strong style="color: #f472b6;">PATCH</strong> /api/v1/ai-ran/config<br>
                <span style="color: #fbcfe8;">→ AI-RAN 설정 업데이트</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 실시간 텔레메트리
    st.markdown("""
    <div class="data-flow-card">
        <h4 style="color: #667eea; margin-top: 0;">📊 실시간 텔레메트리</h4>
        <div style="color: #c7d2fe; line-height: 1.8;">
            • 평균 응답 시간: <strong style="color: #10b981;">18ms</strong><br>
            • API 호출 성공률: <strong style="color: #10b981;">99.8%</strong><br>
            • 동시 연결: <strong style="color: #f59e0b;">47개</strong><br>
            • 대기 큐: <strong style="color: #3b82f6;">2건</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# 하단: 실시간 이벤트 모니터
st.markdown("### 📺 실시간 이벤트 모니터")

col_monitor1, col_monitor2 = st.columns(2)

with col_monitor1:
    st.markdown("#### 🟢 성공 로그")
    success_logs = [
        f"[{current_time.strftime('%H:%M:%S')}] ✓ 데이터 수신: emergency_call_7842",
        f"[{(current_time - timedelta(seconds=5)).strftime('%H:%M:%S')}] ✓ Hot 메모리 할당 완료",
        f"[{(current_time - timedelta(seconds=10)).strftime('%H:%M:%S')}] ✓ AI 트리아지 분석 완료 (Level 1)",
        f"[{(current_time - timedelta(seconds=15)).strftime('%H:%M:%S')}] ✓ 병원 3곳 데이터 전송 완료",
        f"[{(current_time - timedelta(seconds=20)).strftime('%H:%M:%S')}] ✓ RIS 모드 전환 요청 처리",
    ]
    
    log_html = ""
    for log in success_logs:
        log_html += f'<div class="log-entry">{log}</div>'
    
    st.markdown(f'<div class="realtime-monitor">{log_html}</div>', unsafe_allow_html=True)

with col_monitor2:
    st.markdown("#### 🟡 경고 / 정보")
    warning_logs = [
        f"[{current_time.strftime('%H:%M:%S')}] ⚠️ Warm 메모리 사용률 28% (정상)",
        f"[{(current_time - timedelta(seconds=8)).strftime('%H:%M:%S')}] ℹ️ Cold 데이터 아카이브 중...",
        f"[{(current_time - timedelta(seconds=12)).strftime('%H:%M:%S')}] ⚠️ API 지연 감지: 45ms (임계값: 50ms)",
        f"[{(current_time - timedelta(seconds=18)).strftime('%H:%M:%S')}] ℹ️ 네트워크 슬라이스 재할당 완료",
        f"[{(current_time - timedelta(seconds=25)).strftime('%H:%M:%S')}] ⚠️ 동시 연결 47개 (최대: 100)",
    ]
    
    log_html = ""
    for idx, log in enumerate(warning_logs):
        log_class = "warning" if "⚠️" in log else "info"
        log_html += f'<div class="log-entry {log_class}">{log}</div>'
    
    st.markdown(f'<div class="realtime-monitor">{log_html}</div>', unsafe_allow_html=True)

# 자동 새로고침
if st.checkbox("🔄 실시간 모니터링 활성화", value=False):
    time.sleep(1)
    st.rerun()