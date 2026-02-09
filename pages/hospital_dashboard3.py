import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import random

# 파일 상단에 추가 (기존 imports 아래)
if 'emergency_cases' not in st.session_state:
    st.session_state.emergency_cases = []

# 각 대시보드 파일 상단에 추가
if st.sidebar.button("🏠 메인 화면으로"):
    st.switch_page("main.py")

# 페이지 설정
st.set_page_config(
    page_title="🏥 FIELD-DREAM 병원 관제 대시보드",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS 스타일링
st.markdown("""
<style>
    /* 전체 배경 및 폰트 */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&family=Orbitron:wght@400;700;900&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #1a237e 0%, #0d1b2a 100%);
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    /* 메인 타이틀 */
    .main-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00e676 0%, #00bfa5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 0 0 30px rgba(0, 230, 118, 0.5);
    }
    
    /* 수신 환자 카드 */
    .patient-card {
        background: linear-gradient(135deg, rgba(255, 87, 34, 0.2) 0%, rgba(230, 74, 25, 0.2) 100%);
        border: 2px solid #ff5722;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(255, 87, 34, 0.4);
    }
    
    /* 바이탈 사인 카드 */
    .vital-signs {
        background: rgba(0, 150, 136, 0.15);
        border: 2px solid #009688;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
    }
    
    .vital-item {
        background: rgba(0, 0, 0, 0.3);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #00e676;
    }
    
    .vital-critical {
        border-left-color: #ff5252;
        animation: blink 1.5s infinite;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    /* 보안 마크 */
    .security-badge {
        background: linear-gradient(135deg, #7c4dff 0%, #651fff 100%);
        border: 2px solid #b388ff;
        border-radius: 10px;
        padding: 10px 20px;
        display: inline-block;
        margin: 10px 5px;
        box-shadow: 0 4px 16px rgba(124, 77, 255, 0.4);
    }
    
    /* 영상 스트리밍 영역 */
    .video-stream {
        background: rgba(0, 0, 0, 0.5);
        border: 3px solid #00e676;
        border-radius: 15px;
        padding: 20px;
        min-height: 300px;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        overflow: hidden;
    }
    
    .video-stream::before {
        content: "📹 실시간 6G 영상 스트리밍";
        position: absolute;
        top: 10px;
        left: 10px;
        background: rgba(0, 230, 118, 0.9);
        color: white;
        padding: 5px 15px;
        border-radius: 5px;
        font-weight: 700;
        font-size: 0.9rem;
    }
    
    .video-stream::after {
        content: "🔴 LIVE";
        position: absolute;
        top: 10px;
        right: 10px;
        background: #ff1744;
        color: white;
        padding: 5px 15px;
        border-radius: 5px;
        font-weight: 700;
        font-size: 0.9rem;
        animation: pulse 2s infinite;
    }
    
    /* ETA 카운터 */
    .eta-counter {
        background: linear-gradient(135deg, #ff6f00 0%, #e65100 100%);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(255, 111, 0, 0.5);
    }
    
    .eta-time {
        font-family: 'Orbitron', monospace;
        font-size: 3rem;
        font-weight: 900;
        color: white;
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.8);
    }
    
    /* 메트릭 */
    .metric-label {
        font-size: 0.9rem;
        color: #80deea;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .metric-value {
        font-family: 'Orbitron', monospace;
        font-size: 2rem;
        font-weight: 700;
        color: #00e676;
        margin: 5px 0;
    }
    
    /* 트리아지 배지 */
    .triage-critical {
        background: #ff1744;
        color: white;
        padding: 8px 20px;
        border-radius: 20px;
        font-weight: 900;
        font-size: 1.1rem;
        display: inline-block;
        box-shadow: 0 4px 16px rgba(255, 23, 68, 0.6);
    }
    
    .triage-urgent {
        background: #ff9800;
        color: white;
        padding: 8px 20px;
        border-radius: 20px;
        font-weight: 900;
        font-size: 1.1rem;
        display: inline-block;
    }
    
    .triage-normal {
        background: #4caf50;
        color: white;
        padding: 8px 20px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 1.1rem;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'patient_accepted' not in st.session_state:
    st.session_state.patient_accepted = None
if 'eta_seconds' not in st.session_state:
    st.session_state.eta_seconds = 7 * 60 + 30  # 7분 30초
if 'transfer_requested' not in st.session_state:
    st.session_state.transfer_requested = False

# 헤더
st.markdown('<h1 class="main-title">🏥 FIELD-DREAM 병원 관제 대시보드</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #80deea; font-size: 1.2rem; margin-bottom: 30px;">서울대학교병원 권역외상센터</p>', unsafe_allow_html=True)

# 현재 시간
current_time = datetime.now()
col_info1, col_info2, col_info3 = st.columns(3)

with col_info1:
    st.markdown(f"""
    <div style="text-align: center;">
        <div class="metric-label">현재 시각</div>
        <div class="metric-value">{current_time.strftime('%H:%M:%S')}</div>
    </div>
    """, unsafe_allow_html=True)

with col_info2:
    st.markdown(f"""
    <div style="text-align: center;">
        <div class="metric-label">가용 병상</div>
        <div class="metric-value" style="color: #00e676;">3개</div>
    </div>
    """, unsafe_allow_html=True)

with col_info3:
    st.markdown(f"""
    <div style="text-align: center;">
        <div class="metric-label">대기 전문의</div>
        <div class="metric-value" style="color: #00e676;">2명</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# === 여기부터 최신 케이스 정보를 반영한 환자 정보 시작 ===
if st.session_state.emergency_cases:
    latest_case = st.session_state.emergency_cases[-1]
    
    # 메인 레이아웃
    col_left, col_right = st.columns([1.2, 1])
    
    with col_left:
        # 수신 환자 정보 (동적으로 케이스별 정보 표시)
        # 환자 정보 추출
        if latest_case['type'] == "신고음성":
            patient_age = latest_case.get('patient_age_group', '미상')
            patient_gender = latest_case.get('patient_gender', '미상')
            location = latest_case.get('call_location', '위치 정보 없음')
            event_time = latest_case.get('time', datetime.now().strftime('%H:%M:%S'))
            ambulance = "출동 대기 중"
            crew = "배정 중"
        elif latest_case['type'] == "웨어러블 기록":
            patient_age = f"{latest_case.get('user_age', '미상')}세"
            patient_gender = latest_case.get('user_name', '미상')[:1] + "씨"
            location = latest_case.get('gps_location', '위치 정보 없음')
            event_time = latest_case.get('time', datetime.now().strftime('%H:%M:%S'))
            ambulance = "출동 대기 중"
            crew = "배정 중"
        elif latest_case['type'] == "현장 처치 기록":
            patient_age = latest_case.get('patient_estimated_age', '미상')
            patient_gender = latest_case.get('patient_gender', '미상')
            location = latest_case.get('location', '위치 정보 없음')
            event_time = latest_case.get('time', datetime.now().strftime('%H:%M:%S'))
            ambulance = latest_case.get('ambulance_id', '119구급대')
            crew = "현장 출동팀"
        elif latest_case['type'] == "영상 스트리밍":
            patient_age = latest_case.get('patient_age_group', '미상')
            patient_gender = latest_case.get('patient_gender', '미상')
            location = latest_case.get('location', '위치 정보 없음')
            event_time = latest_case.get('time', datetime.now().strftime('%H:%M:%S'))
            ambulance = latest_case.get('ambulance_id', '119구급대')
            crew = "현장 출동팀"
        else:
            patient_age = "미상"
            patient_gender = "미상"
            location = "위치 정보 없음"
            event_time = datetime.now().strftime('%H:%M:%S')
            ambulance = "출동 대기 중"
            crew = "배정 중"
        
        case_id = f"EMG-2025-{datetime.now().strftime('%m%d')}-{random.randint(1000, 9999)}"
        
        st.markdown(f"""
        <div class="patient-card">
            <h2 style="color: #ff7043; margin-top: 0;">🚑 수신 환자 정보</h2>
            <div style="color: white; line-height: 1.8;">
                <p><strong>사건 번호:</strong> {case_id}</p>
                <p><strong>발생 시각:</strong> {event_time}</p>
                <p><strong>환자 정보:</strong> {patient_age} {patient_gender}</p>
                <p><strong>발생 장소:</strong> {location}</p>
                <p><strong>전송 구급대:</strong> {ambulance}</p>
                <p><strong>구급대원:</strong> {crew}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # AI 중증도 분류
        st.markdown("### 🤖 AI 중증도 분류 (Triage)")
        
        severity = latest_case.get('severity', '준긴급')
        condition = latest_case.get('condition', '상태 확인 중')
        
        if severity == "매우긴급":
            triage_class = "triage-critical"
            triage_text = "최우선 (Critical) - Level 1"
        elif severity == "긴급":
            triage_class = "triage-urgent"
            triage_text = "응급 (Urgent) - Level 2"
        else:
            triage_class = "triage-normal"
            triage_text = "준긴급 (Less Urgent) - Level 3"
        
        st.markdown(f"""
        <div style="text-align: center; margin: 20px 0;">
            <div class="{triage_class}">⚠️ {triage_text}</div>
        </div>
        <div style="background: rgba(255, 23, 68, 0.1); padding: 15px; border-radius: 10px; border-left: 4px solid #ff1744; margin-top: 15px;">
            <p style="color: white; line-height: 1.8; margin: 0;">
                <strong style="color: #ff7043;">AI 분석 결과:</strong><br>
                {condition} 가능성 높음 (신뢰도 {random.randint(85, 98)}%)<br>
                즉각적인 전문의 협진 및 검사 필요<br>
                예상 필요 조치: 응급 처치 후 정밀 검사
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # 바이탈 사인 (케이스에 따라 동적 생성)
        st.markdown("### 💓 실시간 바이탈 사인")
        
        # 중증도에 따라 바이탈 생성
        if severity == "매우긴급":
            hr = random.randint(35, 45)
            hr_status = "⚠️ 심각한 서맥"
            hr_critical = True
            
            bp_sys = random.randint(75, 85)
            bp_dia = random.randint(40, 50)
            bp_status = "⚠️ 저혈압"
            bp_critical = True
            
            rr = random.randint(6, 10)
            rr_status = "⚠️ 서맥성 호흡"
            rr_critical = False
            
            spo2 = random.randint(80, 88)
            spo2_status = "⚠️ 저산소증"
            spo2_critical = True
            
            gcs = random.randint(3, 8)
            gcs_status = "⚠️ 심각한 의식 저하"
            gcs_critical = False
        elif severity == "긴급":
            hr = random.randint(55, 70)
            hr_status = "⚠️ 서맥"
            hr_critical = True
            
            bp_sys = random.randint(90, 105)
            bp_dia = random.randint(55, 65)
            bp_status = "⚠️ 경미한 저혈압"
            bp_critical = False
            
            rr = random.randint(12, 16)
            rr_status = "정상 범위"
            rr_critical = False
            
            spo2 = random.randint(90, 94)
            spo2_status = "⚠️ 경미한 저산소"
            spo2_critical = False
            
            gcs = random.randint(10, 13)
            gcs_status = "의식 저하"
            gcs_critical = False
        else:
            hr = random.randint(70, 90)
            hr_status = "정상 범위"
            hr_critical = False
            
            bp_sys = random.randint(110, 130)
            bp_dia = random.randint(70, 85)
            bp_status = "정상 범위"
            bp_critical = False
            
            rr = random.randint(14, 18)
            rr_status = "정상 범위"
            rr_critical = False
            
            spo2 = random.randint(95, 99)
            spo2_status = "정상 범위"
            spo2_critical = False
            
            gcs = random.randint(13, 15)
            gcs_status = "의식 명료"
            gcs_critical = False
        
        temp = round(random.uniform(35.5, 37.2), 1)
        
        st.markdown(f"""
        <div class="vital-signs">
            <div class="vital-item {'vital-critical' if hr_critical else ''}">
                <strong style="color: {'#ff5252' if hr_critical else '#00e676'};">❤️ 심박수:</strong> 
                <span style="color: white; font-size: 1.3rem; font-weight: 700; margin-left: 10px;">{hr} BPM</span>
                <span style="color: {'#ff7043' if hr_critical else '#81c784'}; margin-left: 15px; font-weight: 700;">{hr_status}</span>
            </div>
            <div class="vital-item {'vital-critical' if bp_critical else ''}">
                <strong style="color: {'#ff5252' if bp_critical else '#00e676'};">🩸 혈압:</strong> 
                <span style="color: white; font-size: 1.3rem; font-weight: 700; margin-left: 10px;">{bp_sys}/{bp_dia} mmHg</span>
                <span style="color: {'#ff7043' if bp_critical else '#81c784'}; margin-left: 15px; font-weight: 700;">{bp_status}</span>
            </div>
            <div class="vital-item {'vital-critical' if rr_critical else ''}">
                <strong style="color: {'#ff5252' if rr_critical else '#00e676'};">🫁 호흡수:</strong> 
                <span style="color: white; font-size: 1.3rem; font-weight: 700; margin-left: 10px;">{rr} /min</span>
                <span style="color: {'#ffb74d' if rr_critical else '#81c784'}; margin-left: 15px; font-weight: 700;">{rr_status}</span>
            </div>
            <div class="vital-item">
                <strong style="color: #00e676;">🌡️ 체온:</strong> 
                <span style="color: white; font-size: 1.3rem; font-weight: 700; margin-left: 10px;">{temp}°C</span>
                <span style="color: #81c784; margin-left: 15px;">정상 범위</span>
            </div>
            <div class="vital-item {'vital-critical' if spo2_critical else ''}">
                <strong style="color: {'#ff5252' if spo2_critical else '#00e676'};">💨 산소포화도:</strong> 
                <span style="color: white; font-size: 1.3rem; font-weight: 700; margin-left: 10px;">{spo2}%</span>
                <span style="color: {'#ff7043' if spo2_critical else '#81c784'}; margin-left: 15px; font-weight: 700;">{spo2_status}</span>
            </div>
            <div class="vital-item {'vital-critical' if gcs_critical else ''}">
                <strong style="color: {'#ff5252' if gcs_critical else '#00e676'};">🧠 의식 수준 (GCS):</strong> 
                <span style="color: white; font-size: 1.3rem; font-weight: 700; margin-left: 10px;">{gcs}점</span>
                <span style="color: {'#ff7043' if gcs < 10 else '#81c784'}; margin-left: 15px; font-weight: 700;">{gcs_status}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 실시간 영상 스트리밍
        st.markdown("### 📹 실시간 영상 스트리밍")
        st.markdown("""
        <div class="video-stream">
            <div style="text-align: center; color: white;">
                <div style="font-size: 4rem; margin-bottom: 10px;">📹</div>
                <p style="font-size: 1.2rem; font-weight: 700;">6G 고대역폭 영상 전송 중</p>
                <p style="color: #80deea;">해상도: 4K (3840×2160) | 프레임률: 60fps</p>
                <p style="color: #4caf50; font-weight: 700;">📶 연결 상태: 우수 (대역폭 487 Mbps)</p>
                <div style="margin-top: 20px; background: rgba(0, 0, 0, 0.5); padding: 15px; border-radius: 10px; display: inline-block;">
                    <p style="margin: 0; color: #ffb74d;">현재 환자 상태 영상 실시간 전송 중</p>
                    <p style="margin: 5px 0 0 0; font-size: 0.9rem; color: #90caf9;">응급 처치 진행 상황 확인 가능</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_right:
        # ETA 카운터
        st.markdown("### ⏱️ 도착 예정 시간 (ETA)")
        
        minutes = st.session_state.eta_seconds // 60
        seconds = st.session_state.eta_seconds % 60
        
        st.markdown(f"""
        <div class="eta-counter">
            <div class="eta-time">{minutes:02d}:{seconds:02d}</div>
            <p style="color: white; font-size: 1.1rem; margin: 10px 0 0 0;">실시간 교통 상황 반영</p>
            <p style="color: #ffcc80; font-size: 0.9rem; margin: 5px 0 0 0;">6G AI Agent가 최적 경로로 안내 중</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 데이터 보안 상태
        st.markdown("### 🔐 데이터 신뢰성 및 보안")
        st.markdown("""
        <div style="text-align: center; margin: 20px 0;">
            <div class="security-badge">
                <span style="color: white; font-weight: 700;">🔒 양자 보안 (Quantum Security) 적용</span>
            </div>
            <div class="security-badge">
                <span style="color: white; font-weight: 700;">✅ 데이터 무결성 확인 완료</span>
            </div>
            <div class="security-badge">
                <span style="color: white; font-weight: 700;">🛡️ End-to-End 암호화</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: rgba(124, 77, 255, 0.15); padding: 15px; border-radius: 10px; border: 2px solid #7c4dff; margin-top: 15px;">
            <p style="color: white; line-height: 1.8; margin: 0;">
                <strong style="color: #b388ff;">🔐 보안 상태:</strong><br>
                ✓ 양자 키 분배(QKD) 프로토콜 활성화<br>
                ✓ 의료 데이터 HIPAA 준수<br>
                ✓ 블록체인 기반 전송 로그 기록<br>
                ✓ 무단 접근 시도: 0건
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # 추가 정보 (케이스 타입별 정보)
        st.markdown("### 📊 추가 의료 정보")
        
        # 환자 과거력 (랜덤 생성)
        # 파일 상단 초기화 부분에 먼저 추가 (한 번만)
        if 'patient_history' not in st.session_state:
            st.session_state.patient_history = None
        if 'last_case_id' not in st.session_state:
            st.session_state.last_case_id = None

# ========================================
# 그리고 환자 과거력 표시 부분을 아래 코드로 교체
# ========================================

# 케이스 ID 생성 (케이스가 바뀌었는지 확인용)
        current_case_id = f"{latest_case.get('time', '')}_{latest_case.get('condition', '')}"

# 새로운 케이스가 들어왔을 때만 과거력 업데이트
        if st.session_state.last_case_id != current_case_id:
            st.session_state.last_case_id = current_case_id
            
            # 케이스 조건에 따라 과거력 생성
            condition = latest_case.get('condition', '')
            
            if "심정지" in condition or "심근경색" in condition:
                medical_history = [
                    "• 고혈압 병력 (9년)",
                    "• 당뇨병 (6년)",
                    "• 흡연력: 24갑년",
                    "• 최근 흉통 호소 이력 있음"
                ]
                allergies = "페니실린 계열"
            elif "뇌졸중" in condition:
                medical_history = [
                    "• 심방세동 (5년)",
                    "• 고지혈증 (3년)",
                    "• 과거 심근경색 (2022년)",
                    "• 고혈압 (7년)"
                ]
                allergies = "조영제"
            elif "저혈당" in condition or "당뇨" in condition:
                medical_history = [
                    "• 당뇨병 Type 2 (8년)",
                    "• 인슐린 치료 중",
                    "• 저혈당 이력: 최근 6개월 3회",
                    "• 당뇨병성 신경병증"
                ]
                allergies = "알려진 알레르기 없음"
            elif "산과" in condition or "임신" in condition:
                medical_history = [
                    "• 임신 32주",
                    "• 임신성 고혈압",
                    "• 제왕절개 1회 (2021년)",
                    "• 태아 발육 정상"
                ]
                allergies = "알려진 알레르기 없음"
            else:
                medical_history = [
                    "• 고혈압 병력 (5년)",
                    "• 최근 건강검진 정상",
                    "• 특이 병력 없음"
                ]
                allergies = "알려진 알레르기 없음"
            
            # session_state에 저장
            st.session_state.patient_history = {
                'medical_history': medical_history,
                'allergies': allergies
            }

        # 표시할 때는 session_state에서 가져오기
        if st.session_state.patient_history:
            history_text = "<br>".join(st.session_state.patient_history['medical_history'])
            allergies = st.session_state.patient_history['allergies']
        else:
            history_text = "• 특이 병력 없음"
            allergies = "알려진 알레르기 없음"

        st.markdown(f"""
        <div style="background: rgba(0, 188, 212, 0.15); padding: 15px; border-radius: 10px; border: 2px solid #00bcd4;">
            <p style="color: white; line-height: 1.8;">
                <strong style="color: #4dd0e1;">환자 과거력 (AI 분석):</strong><br>
                {history_text}<br>
                • 알러지: {allergies}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # 구급대원 현장 조치
        if latest_case['type'] == "현장 처치 기록":
            first_aid_text = "<br>".join([f"• {aid}" for aid in latest_case.get('first_aid', ['응급 처치 진행 중'])])
            current_status = latest_case.get('current_status', '상태 확인 중')
        else:
            first_aid_list = [
                "CPR 진행 중" if severity == "매우긴급" else "환자 상태 모니터링 중",
                "기도 확보 완료" if severity == "매우긴급" else "기도 확인 완료",
                f"산소 투여 중 ({random.randint(10, 15)}L/min)",
                "정맥로 확보 시도 중",
            ]
            if severity == "매우긴급":
                first_aid_list.append("AED 제세동 준비 중")
            
            first_aid_text = "<br>".join([f"• {aid}" for aid in first_aid_list])
            current_status = "구급대 이송 중"
        
        st.markdown(f"""
        <div style="background: rgba(255, 193, 7, 0.15); padding: 15px; border-radius: 10px; border: 2px solid #ffc107; margin-top: 15px;">
            <p style="color: white; line-height: 1.8;">
                <strong style="color: #ffd54f;">⚡ 구급대원 현장 조치:</strong><br>
                {first_aid_text}<br>
                • 현재 상태: {current_status}
            </p>
        </div>
        """, unsafe_allow_html=True)

else:
    # 케이스가 없을 때 기본 화면
    st.info("💡 Front Office에서 응급 상황을 생성하면 환자 정보가 여기에 표시됩니다.")
    
    col_left, col_right = st.columns([1.2, 1])
    
    with col_left:
        st.markdown("""
        <div class="patient-card">
            <h2 style="color: #ff7043; margin-top: 0;">🚑 수신 환자 대기 중</h2>
            <div style="color: white; line-height: 1.8;">
                <p style="text-align: center; padding: 40px;">
                    Front Office에서 응급 상황을 생성하세요
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_right:
        st.markdown("""
        <div class="eta-counter">
            <div class="eta-time">--:--</div>
            <p style="color: white; font-size: 1.1rem; margin: 10px 0 0 0;">환자 대기 중</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# 수용 결정 인터페이스
st.markdown("## 🏥 수용 결정")

if st.session_state.patient_accepted is None and st.session_state.emergency_cases:
    col_accept, col_reject = st.columns(2)
    
    with col_accept:
        if st.button("✅ 환자 수용 승인", key="accept", use_container_width=True):
            st.session_state.patient_accepted = True
            st.rerun()
    
    with col_reject:
        if st.button("❌ 수용 불가", key="reject", use_container_width=True):
            st.session_state.patient_accepted = False
            st.rerun()

elif st.session_state.patient_accepted == True:
    st.success("✅ 환자 수용이 승인되었습니다!")
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(0, 230, 118, 0.2) 0%, rgba(0, 200, 83, 0.2) 100%); 
                padding: 20px; border-radius: 15px; border: 2px solid #00e676; margin: 20px 0;">
        <h3 style="color: #00e676; margin-top: 0;">📋 수용 준비 체크리스트</h3>
        <div style="color: white; line-height: 2;">
            <p>✅ 중환자실 병상 확보 완료</p>
            <p>✅ 필요 장비 준비 완료</p>
            <p>✅ 전문의 2명 대기</p>
            <p>✅ 응급실 소생술팀 소집 완료</p>
            <p>✅ 혈액은행 통보 완료</p>
            <p>🔄 전문의료팀 호출 중...</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 결정 취소", key="cancel"):
        st.session_state.patient_accepted = None
        st.rerun()

elif st.session_state.patient_accepted == False:
    st.error("❌ 환자 수용이 거부되었습니다.")
    
    # 타 병원 전원 요청
    st.markdown("### 🏥 근처 병원 전원 요청")
    
    if not st.session_state.transfer_requested:
        st.markdown("""
        <div style="background: rgba(255, 152, 0, 0.15); border: 2px solid #ff9800; border-radius: 15px; padding: 20px; margin: 15px 0;">
            <h3 style="color: #ff9800; margin-top: 0;">📍 근처 가용 병원</h3>
            <p style="color: #ffcc80;">수용이 불가능한 경우 근처 병원에 전원을 요청할 수 있습니다.</p>
        </div>
        """, unsafe_allow_html=True)
        
        nearby_hospitals = [
            {"name": "서울아산병원 응급의료센터", "distance": "4.1 km", "beds": "5개 가용", "score": 95},
            {"name": "삼성서울병원 심장센터", "distance": "5.8 km", "beds": "2개 가용", "score": 92},
            {"name": "세브란스병원 심혈관센터", "distance": "6.2 km", "beds": "4개 가용", "score": 90},
        ]
        
        selected_hospitals = []
        
        for idx, hospital in enumerate(nearby_hospitals):
            col_h1, col_h2 = st.columns([3, 1])
            
            with col_h1:
                st.markdown(f"""
                <div style="background: rgba(0, 0, 0, 0.3); padding: 15px; border-radius: 10px; margin: 10px 0;">
                    <h4 style="color: #ff9800; margin: 0;">{hospital['name']}</h4>
                    <p style="color: white; margin: 5px 0;">
                        📍 {hospital['distance']} | 🛏️ {hospital['beds']} | AI 점수: {hospital['score']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col_h2:
                if st.checkbox("선택", key=f"nearby_{idx}"):
                    selected_hospitals.append(hospital['name'])
        
        if selected_hospitals:
            st.markdown(f"**선택된 병원:** {', '.join(selected_hospitals)}")
            
            if st.button("📤 선택한 병원에 전원 요청 전송", type="primary"):
                st.session_state.transfer_requested = True
                st.rerun()
    else:
        st.success("✅ 전원 요청이 전송되었습니다!")
        st.markdown("""
        <div style="background: rgba(0, 230, 118, 0.15); padding: 15px; border-radius: 10px; border: 2px solid #00e676;">
            <p style="color: white; line-height: 1.8;">
                <strong style="color: #00e676;">전원 요청 상태:</strong><br>
                • 서울아산병원: 검토 중...<br>
                • 삼성서울병원: 검토 중...<br>
                • AI Agent가 실시간으로 응답을 모니터링하고 있습니다.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 다시 결정하기", key="reset"):
            st.session_state.patient_accepted = None
            st.session_state.transfer_requested = False
            st.rerun()

# 자동 ETA 업데이트
if st.checkbox("🔄 실시간 업데이트 활성화", value=False):
    if st.session_state.eta_seconds > 0:
        st.session_state.eta_seconds -= 1
    time.sleep(1)
    st.rerun()