import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

# 페이지 설정
st.set_page_config(
    page_title="🚑 FIELD-DREAM 구급대원 대시보드",
    page_icon="🚑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 세션 상태 초기화
if 'emergency_cases' not in st.session_state:
    st.session_state.emergency_cases = []
if 'selected_hospital' not in st.session_state:
    st.session_state.selected_hospital = None

# CSS 스타일링 (기존과 동일)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Noto+Sans+KR:wght@300;400;700;900&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1419 100%);
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    .main-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        text-shadow: 0 0 30px rgba(0, 212, 255, 0.5);
        margin-bottom: 0.5rem;
        letter-spacing: 2px;
    }
    
    .subtitle {
        text-align: center;
        color: #00d4ff;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 3px;
    }
    
    .network-status {
        background: rgba(0, 212, 255, 0.1);
        border: 2px solid #00d4ff;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
        backdrop-filter: blur(10px);
    }
    
    .metric-label {
        color: #90caf9;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-family: 'Orbitron', sans-serif;
    }
    
    .hospital-card {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(0, 153, 204, 0.05) 100%);
        border: 2px solid #00d4ff;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(0, 212, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .hospital-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 212, 255, 0.4);
        border-color: #00ffff;
    }
    
    .network-log {
        background: rgba(0, 0, 0, 0.5);
        border-left: 4px solid #00d4ff;
        border-radius: 8px;
        padding: 15px;
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
        color: #90caf9;
        max-height: 300px;
        overflow-y: auto;
    }
    
    .ai-context-box {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.15) 0%, rgba(0, 153, 204, 0.1) 100%);
        border: 2px solid #00d4ff;
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 0 30px rgba(0, 212, 255, 0.3);
    }
    
    .treatment-guide-box {
        background: linear-gradient(135deg, rgba(255, 152, 0, 0.15) 0%, rgba(255, 87, 34, 0.1) 100%);
        border: 2px solid #ffa726;
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 0 30px rgba(255, 152, 0, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# 헤더
st.markdown('<h1 class="main-title">🚑 FIELD-DREAM 구급대원 대시보드</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">6G-BASED EMERGENCY RESPONSE SYSTEM</p>', unsafe_allow_html=True)

# 현재 시간
current_time = datetime.now()

# 메인 레이아웃
col_left, col_right = st.columns([1.2, 1])

with col_left:
    # 실시간 케이스 모니터링
    st.markdown("---")
    st.subheader("🚨 실시간 응급 케이스")
    
    if st.session_state.emergency_cases:
        # 가장 최근 케이스
        latest_case = st.session_state.emergency_cases[-1]
        
        # ========================================
        # AI 상황 요약 (Context) - 동적 생성
        # ========================================
        st.markdown("### 🤖 AI 상황 요약 (Context)")
        
        # 케이스 정보 추출
        case_type = latest_case.get('type', '알 수 없음')
        
        # 환자 기본 정보
        if case_type == "신고음성":
            patient_info = f"{latest_case.get('patient_age_group', '연령 미상')} {latest_case.get('patient_gender', '성별 미상')}"
            location = latest_case.get('call_location', '위치 미상')
            condition = latest_case.get('condition', '증상 미상')
            severity = latest_case.get('severity', '긴급')
        elif case_type == "웨어러블 기록":
            patient_info = f"{latest_case.get('user_age', '?')}세 {latest_case.get('user_name', '사용자')}"
            location = latest_case.get('gps_location', '위치 미상')
            condition = latest_case.get('condition', '증상 미상')
            severity = latest_case.get('severity', '긴급')
        elif case_type == "현장 처치 기록":
            patient_info = f"{latest_case.get('patient_estimated_age', '연령 미상')} {latest_case.get('patient_gender', '성별 미상')}"
            location = latest_case.get('location', '위치 미상')
            condition = latest_case.get('condition', '증상 미상')
            severity = latest_case.get('urgency_level', '긴급')
        else:
            patient_info = "환자 정보 없음"
            location = "위치 정보 없음"
            condition = "증상 정보 없음"
            severity = "긴급도 미상"
        
        # 추정 상황 및 초기 판단 생성
        initial_assessment = ""
        suspected_diagnosis = ""
        vital_status = ""
        
        if "심정지" in condition or "의식소실" in condition:
            suspected_diagnosis = "심정지 의심 (심근경색 가능성 높음)"
            vital_status = "무반응 (GCS 3점)"
            initial_assessment = "갑작스러운 가슴 통증 후 의식 소실"
        elif "뇌졸중" in condition or "반신마비" in condition:
            suspected_diagnosis = "뇌졸중 의심 (허혈성 가능성)"
            vital_status = "심정지 외심 (심근경색 가능성 높음)"
            initial_assessment = "갑작스런 언어장애 및 편측 마비 증상"
        elif "저혈당" in condition:
            suspected_diagnosis = "중증 저혈당 쇼크"
            vital_status = "의식 저하 (혈당 40mg/dL)"
            initial_assessment = "당뇨 환자의 갑작스런 의식 저하"
        elif "부정맥" in condition:
            suspected_diagnosis = "심방세동으로 인한 급성 부정맥"
            vital_status = "빈맥 (심박수 180bpm)"
            initial_assessment = "심계항진 및 호흡곤란 호소"
        elif "교통사고" in condition or "외상" in condition:
            suspected_diagnosis = "다발성 외상 (복부 내출혈 의심)"
            vital_status = "쇼크 진행 중 (BP 80/50)"
            initial_assessment = "고속 충돌 사고, 복부 타박상"
        elif "산과" in condition or "임신" in condition:
            suspected_diagnosis = "조기 진통 또는 태반조기박리"
            vital_status = "불안정 (자궁수축 빈번)"
            initial_assessment = "임신 32주, 갑작스런 복통 및 출혈"
        else:
            suspected_diagnosis = "응급 상황 (상세 평가 필요)"
            vital_status = "평가 중"
            initial_assessment = "신고 접수됨, 현장 도착 대기 중"
        
        st.markdown(f"""
        <div class="ai-context-box">
            <h4 style="color: #00d4ff; margin-top: 0;">📋 환자 정보</h4>
            <p style="color: white; line-height: 1.8; font-size: 1.05rem;">
                <strong>환자 정보:</strong> {patient_info}<br>
                <strong>주 증상:</strong> {condition}<br>
                <strong>추정 상황:</strong> {initial_assessment}<br>
                <strong>의식 상태:</strong> {vital_status}<br>
                <strong>발견 장소:</strong> {location} (인파 밀집 지역)
            </p>
            
            <h4 style="color: #ffa726; margin-top: 20px;">🩺 신고자 진술 요약</h4>
            <p style="color: white; line-height: 1.8; font-size: 1.05rem;">
                "{latest_case.get('witness_report', '갑자기 쓰러졌어요! 숨을 안 쉬는 것 같아요!')}"
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # ========================================
        # AI 중증도 분류
        # ========================================
        st.markdown("### 🤖 AI 중증도 분류")
        if severity in ["매우긴급", "최고긴급"]:
            st.error(f"**KTAS 1단계 (소생)** - {suspected_diagnosis}")
            st.write("- 즉시 치료 필요")
            st.write("- 전문의 즉시 대기 필요")
        elif severity == "긴급":
            st.warning(f"**KTAS 2단계 (응급)** - {suspected_diagnosis}")
            st.write("- 15분 이내 치료 시작 권장")
        else:
            st.info(f"**KTAS 3단계 (준응급)** - {suspected_diagnosis}")
        
        # ========================================
        # 추천 병원 3개 - 동적 생성 (환자 위치 기반)
        # ========================================
        st.markdown("### 🏥 추천 병원 (환자 위치 기반)")
        
        # 위치 정보 파싱 (서울 중구, 명동역 등의 정보를 기반으로 근처 병원 추천)
        hospitals = []
        
        if "심정지" in condition or "심근경색" in condition:
            # 심장 관련 응급 - 심혈관센터 우선
            if "명동" in location or "중구" in location:
                hospitals = [
                    {
                        "name": "서울대학교병원 권역외상센터",
                        "distance": "2.3 km",
                        "eta": "7분 30초",
                        "available": True,
                        "beds": "3개 가용",
                        "specialists": "심장내과 전문의 2명 대기",
                        "equipment": "심혈관조영술(CAG) 준비 완료",
                        "score": 98
                    },
                    {
                        "name": "서울아산병원 응급의료센터",
                        "distance": "4.1 km",
                        "eta": "11분 20초",
                        "available": True,
                        "beds": "5개 가용",
                        "specialists": "순환기내과 전문의 3명 대기",
                        "equipment": "중환자실 즉시 가용",
                        "score": 95
                    },
                    {
                        "name": "삼성서울병원 심장센터",
                        "distance": "5.8 km",
                        "eta": "14분 50초",
                        "available": True,
                        "beds": "2개 가용",
                        "specialists": "심혈관외과 전문의 1명 대기",
                        "equipment": "ECMO 장비 대기",
                        "score": 92
                    }
                ]
            else:
                hospitals = [
                    {
                        "name": "근처 심장센터 A",
                        "distance": "3.2 km",
                        "eta": "9분",
                        "available": True,
                        "beds": "2개 가용",
                        "specialists": "심장내과 전문의 대기중",
                        "equipment": "CAG 준비완료",
                        "score": 94
                    },
                    {
                        "name": "근처 심장센터 B",
                        "distance": "5.1 km",
                        "eta": "13분",
                        "available": True,
                        "beds": "3개 가용",
                        "specialists": "순환기내과 전문의 대기",
                        "equipment": "중환자실 가용",
                        "score": 90
                    },
                    {
                        "name": "근처 심장센터 C",
                        "distance": "7.2 km",
                        "eta": "17분",
                        "available": False,
                        "beds": "포화",
                        "specialists": "대기중",
                        "equipment": "준비중",
                        "score": 85
                    }
                ]
        
        elif "뇌졸중" in condition or "반신마비" in condition:
            # 뇌졸중 - 뇌졸중센터 우선
            if "명동" in location or "중구" in location:
                hospitals = [
                    {
                        "name": "서울대학교병원 뇌졸중센터",
                        "distance": "2.3 km",
                        "eta": "7분 30초",
                        "available": True,
                        "beds": "2개 가용",
                        "specialists": "신경과 전문의 2명 대기",
                        "equipment": "MRI/CT 즉시 가용",
                        "score": 98
                    },
                    {
                        "name": "분당서울대병원 뇌졸중센터",
                        "distance": "8.5 km",
                        "eta": "19분",
                        "available": True,
                        "beds": "3개 가용",
                        "specialists": "신경외과 전문의 대기",
                        "equipment": "혈전제거술 가능",
                        "score": 93
                    },
                    {
                        "name": "세브란스병원 신경과",
                        "distance": "6.2 km",
                        "eta": "15분",
                        "available": True,
                        "beds": "1개 가용",
                        "specialists": "뇌졸중 전문의 대기",
                        "equipment": "tPA 준비완료",
                        "score": 91
                    }
                ]
            else:
                hospitals = [
                    {
                        "name": "근처 뇌졸중센터 A",
                        "distance": "3.5 km",
                        "eta": "10분",
                        "available": True,
                        "beds": "2개 가용",
                        "specialists": "신경과 전문의 대기",
                        "equipment": "MRI 가용",
                        "score": 95
                    },
                    {
                        "name": "근처 뇌졸중센터 B",
                        "distance": "6.1 km",
                        "eta": "16분",
                        "available": True,
                        "beds": "1개 가용",
                        "specialists": "신경외과 대기",
                        "equipment": "CT 가용",
                        "score": 88
                    }
                ]
        
        elif "산과" in condition or "임신" in condition:
            # 산과 응급 - 산부인과 병원
            hospitals = [
                {
                    "name": "강남차병원 산부인과",
                    "distance": "4.2 km",
                    "eta": "11분",
                    "available": True,
                    "beds": "분만실 2개 가용",
                    "specialists": "산부인과 전문의 2명 대기",
                    "equipment": "신생아집중치료실 준비",
                    "score": 96
                },
                {
                    "name": "삼성제일병원",
                    "distance": "5.8 km",
                    "eta": "14분",
                    "available": True,
                    "beds": "분만실 1개 가용",
                    "specialists": "산부인과 전문의 대기",
                    "equipment": "NICU 가용",
                    "score": 93
                },
                {
                    "name": "미즈메디병원",
                    "distance": "7.1 km",
                    "eta": "17분",
                    "available": True,
                    "beds": "분만실 가용",
                    "specialists": "고위험 산모 전문",
                    "equipment": "응급 제왕절개 가능",
                    "score": 90
                }
            ]
        
        elif "저혈당" in condition or "당뇨" in condition:
            # 내분비 응급
            hospitals = [
                {
                    "name": "서울아산병원 응급의료센터",
                    "distance": "4.1 km",
                    "eta": "11분",
                    "available": True,
                    "beds": "응급실 5개 가용",
                    "specialists": "내분비내과 전문의 대기",
                    "equipment": "혈당 모니터링 시스템",
                    "score": 95
                },
                {
                    "name": "삼성서울병원",
                    "distance": "5.8 km",
                    "eta": "15분",
                    "available": True,
                    "beds": "응급실 3개 가용",
                    "specialists": "당뇨병센터 전문의 대기",
                    "equipment": "중환자실 준비",
                    "score": 92
                },
                {
                    "name": "세브란스병원",
                    "distance": "6.5 km",
                    "eta": "16분",
                    "available": True,
                    "beds": "응급실 2개 가용",
                    "specialists": "내과 전문의 대기",
                    "equipment": "응급처치 가능",
                    "score": 89
                }
            ]
        
        else:
            # 일반 응급
            if "명동" in location or "중구" in location:
                hospitals = [
                    {
                        "name": "서울대학교병원 권역외상센터",
                        "distance": "2.3 km",
                        "eta": "7분 30초",
                        "available": True,
                        "beds": "3개 가용",
                        "specialists": "응급의학과 전문의 대기",
                        "equipment": "종합 응급시설",
                        "score": 98
                    },
                    {
                        "name": "서울아산병원 응급의료센터",
                        "distance": "4.1 km",
                        "eta": "11분 20초",
                        "available": True,
                        "beds": "5개 가용",
                        "specialists": "응급의학과 전문의 3명",
                        "equipment": "중환자실 가용",
                        "score": 95
                    },
                    {
                        "name": "중앙대학교병원",
                        "distance": "3.5 km",
                        "eta": "9분 40초",
                        "available": False,
                        "beds": "포화 상태",
                        "specialists": "대기 중",
                        "equipment": "준비 중",
                        "score": 75
                    }
                ]
            else:
                hospitals = [
                    {
                        "name": "근처 종합병원 A",
                        "distance": "2.5 km",
                        "eta": "7분",
                        "available": True,
                        "beds": "응급실 3개",
                        "specialists": "응급의학과 대기",
                        "equipment": "종합 응급시설",
                        "score": 90
                    },
                    {
                        "name": "근처 종합병원 B",
                        "distance": "4.8 km",
                        "eta": "12분",
                        "available": True,
                        "beds": "응급실 2개",
                        "specialists": "전문의 대기",
                        "equipment": "응급시설 가용",
                        "score": 85
                    }
                ]
        
        # 병원 카드 렌더링
        # 병원 카드 렌더링 (원본 디자인)
        for idx, hospital in enumerate(hospitals):
            if hospital["available"]:
                card_style = "hospital-card"
                availability_text = f"<span style='color: #4caf50; font-weight: 700;'>✅ 수용 가능</span>"
            else:
                card_style = "hospital-card" 
                availability_text = f"<span style='color: #f44336; font-weight: 700;'>❌ 수용 불가</span>"
            
            with st.container():
                st.markdown(f"""
                <div class="{card_style}">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <h3 style="color: #00d4ff; margin: 0;">{hospital['name']}</h3>
                        <div style="background: rgba(0, 212, 255, 0.2); padding: 5px 15px; border-radius: 20px;">
                            <span style="color: #00d4ff; font-weight: 700;">AI 점수: {hospital['score']}</span>
                        </div>
                    </div>
                    <div style="color: white; line-height: 1.6;">
                        <p><strong>📍 거리:</strong> {hospital['distance']} | <strong>⏱️ ETA:</strong> {hospital['eta']}</p>
                        <p><strong>🛏️ 병상:</strong> {hospital['beds']} | <strong>👨‍⚕️ 전문의:</strong> {hospital['specialists']}</p>
                        <p><strong>🔬 장비:</strong> {hospital['equipment']}</p>
                        <p><strong>수용 여부:</strong> {availability_text}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # 병원 선택 버튼
        if st.button(f"🏥 {hospital['name']} 상세보기", key=f"hospital_{idx}", disabled=not hospital["available"]):
            st.session_state.selected_hospital = hospital
        
        # ========================================
        # 실시간 처치 가이드 - 동적 생성
        # ========================================
        st.markdown("### 💊 실시간 처치 가이드")
        
        if "심정지" in condition or "무반응" in vital_status:
            st.markdown("""
            <div class="treatment-guide-box">
                <h4 style="color: #ff5722; margin-top: 0;">🚨 우선순위 1: CPR 지속 (현재 5분 경과)</h4>
                <p style="color: white; line-height: 2; font-size: 1.05rem;">
                    <strong>✅ 우선순위 1:</strong> CPR 지속 (30:2 비율 유지)<br>
                    <strong>✅ 우선순위 2:</strong> 제세동기 준비 및 부착 (리듬 확인)<br>
                    <strong>✅ 우선순위 3:</strong> 고급 기도 확보 (기관삽관 또는 LMA)<br>
                    <strong>✅ 우선순위 4:</strong> 에피네프린 1mg IV 투여 (3-5분 간격)<br>
                    <strong>⏱️ 우선순위 5:</strong> 2분마다 리듬 체크 및 재평가
                </p>
                <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px; margin-top: 15px;">
                    <p style="color: #ffa726; margin: 0; font-size: 0.95rem;">
                        <strong>⚠️ 주의사항:</strong><br>
                        • CPR 중단 시간 최소화 (10초 이내)<br>
                        • 가슴 압박 깊이: 5-6cm, 속도: 100-120회/분<br>
                        • 과환기 주의 (1회 환기량 500-600mL)
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        elif "뇌졸중" in condition or "반신마비" in condition:
            st.markdown("""
            <div class="treatment-guide-box">
                <h4 style="color: #ff9800; margin-top: 0;">⚠️ 뇌졸중 프로토콜 (골든타임: 4.5시간)</h4>
                <p style="color: white; line-height: 2; font-size: 1.05rem;">
                    <strong>✅ 우선순위 1:</strong> FAST 검사 실시 및 기록<br>
                    <strong>✅ 우선순위 2:</strong> 혈당 측정 (저혈당 배제)<br>
                    <strong>✅ 우선순위 3:</strong> 산소 투여 (SpO2 <94% 시)<br>
                    <strong>✅ 우선순위 4:</strong> 정맥로 확보 (생리식염수)<br>
                    <strong>⚠️ 금기사항:</strong> 혈압 강하제 투여 금지<br>
                    <strong>🚑 조치:</strong> 즉시 뇌졸중센터 이송 준비
                </p>
                <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px; margin-top: 15px;">
                    <p style="color: #ffa726; margin: 0; font-size: 0.95rem;">
                        <strong>📋 FAST 체크리스트:</strong><br>
                        • Face (안면 마비 확인)<br>
                        • Arm (팔 거상 저하 확인)<br>
                        • Speech (언어 장애 확인)<br>
                        • Time (증상 발생 시간 기록 필수)
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        elif "심근경색" in condition or "흉통" in condition:
            st.markdown("""
            <div class="treatment-guide-box">
                <h4 style="color: #ff9800; margin-top: 0;">⚠️ 급성심근경색 프로토콜</h4>
                <p style="color: white; line-height: 2; font-size: 1.05rem;">
                    <strong>✅ 우선순위 1:</strong> 12-Lead ECG 시행 (10분 이내)<br>
                    <strong>✅ 우선순위 2:</strong> 아스피린 300mg 씹어서 복용<br>
                    <strong>✅ 우선순위 3:</strong> 니트로글리세린 설하 투여 (0.4mg)<br>
                    <strong>✅ 우선순위 4:</strong> 산소 투여 (SpO2 <90% 시)<br>
                    <strong>✅ 우선순위 5:</strong> 정맥로 확보 및 진통제 고려<br>
                    <strong>🚑 조치:</strong> 심혈관센터 직행 (PCI 가능 병원)
                </p>
                <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px; margin-top: 15px;">
                    <p style="color: #ffa726; margin: 0; font-size: 0.95rem;">
                        <strong>⏱️ 골든타임:</strong><br>
                        • Door-to-Balloon 시간 90분 이내 목표<br>
                        • 증상 발생 12시간 이내 재관류 치료 효과적
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        elif "저혈당" in condition:
            st.markdown("""
            <div class="treatment-guide-box">
                <h4 style="color: #ff9800; margin-top: 0;">⚠️ 중증 저혈당 프로토콜</h4>
                <p style="color: white; line-height: 2; font-size: 1.05rem;">
                    <strong>✅ 우선순위 1:</strong> 혈당 측정 및 기록<br>
                    <strong>✅ 우선순위 2:</strong> 정맥로 확보<br>
                    <strong>✅ 우선순위 3:</strong> 50% 포도당 50mL IV 천천히 투여<br>
                    <strong>✅ 우선순위 4:</strong> 5분 후 혈당 재측정<br>
                    <strong>✅ 우선순위 5:</strong> 의식 회복 후 경구 당분 섭취
                </p>
                <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px; margin-top: 15px;">
                    <p style="color: #ffa726; margin: 0; font-size: 0.95rem;">
                        <strong>⚠️ 주의사항:</strong><br>
                        • 의식 없는 경우 경구 투여 금지<br>
                        • 글루카곤 1mg IM 투여 고려 (정맥로 확보 실패 시)
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        elif "산과" in condition or "임신" in condition:
            st.markdown("""
            <div class="treatment-guide-box">
                <h4 style="color: #ff9800; margin-top: 0;">⚠️ 산과 응급 프로토콜</h4>
                <p style="color: white; line-height: 2; font-size: 1.05rem;">
                    <strong>✅ 우선순위 1:</strong> 산모 활력징후 모니터링<br>
                    <strong>✅ 우선순위 2:</strong> 태아 심박동 확인 (가능 시)<br>
                    <strong>✅ 우선순위 3:</strong> 산소 투여 (100% O2)<br>
                    <strong>✅ 우선순위 4:</strong> 좌측위 자세 유지<br>
                    <strong>✅ 우선순위 5:</strong> 정맥로 확보 (2개 이상)<br>
                    <strong>🚑 조치:</strong> 산부인과 전문병원 즉시 이송
                </p>
                <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px; margin-top: 15px;">
                    <p style="color: #ffa726; margin: 0; font-size: 0.95rem;">
                        <strong>⚠️ 주의사항:</strong><br>
                        • 응급 분만 준비 (분만 키트 확인)<br>
                        • 태반조기박리 의심 시 즉각 이송<br>
                        • 자궁수축 간격 및 강도 기록
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        else:
            st.markdown("""
            <div class="treatment-guide-box">
                <h4 style="color: #ff9800; margin-top: 0;">⚠️ 일반 응급 프로토콜</h4>
                <p style="color: white; line-height: 2; font-size: 1.05rem;">
                    <strong>✅ 우선순위 1:</strong> 환자 평가 (의식, 기도, 호흡, 순환)<br>
                    <strong>✅ 우선순위 2:</strong> 활력징후 측정 및 모니터링<br>
                    <strong>✅ 우선순위 3:</strong> 산소 투여 (필요 시)<br>
                    <strong>✅ 우선순위 4:</strong> 정맥로 확보<br>
                    <strong>🚑 조치:</strong> 증상에 따른 적절한 병원 이송
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        st.info("현재 수신된 응급 케이스가 없습니다. Front Dashboard에서 케이스가 전송되면 자동으로 업데이트됩니다.")
    
    # 6G 네트워크 상태
    st.markdown("---")
    st.markdown("### 📡 6G 네트워크 상태")
    
    koi_col1, koi_col2, koi_col3 = st.columns(3)
    
    with koi_col1:
        st.markdown("""
        <div class="network-status">
            <div style="text-align: center;">
                <div class="metric-label">Middle 지표</div>
                <div style="font-size: 2rem; font-weight: 700; color: #4caf50; margin-top: 5px;">
                    0.95
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with koi_col2:
        st.markdown("""
        <div class="network-status">
            <div style="text-align: center;">
                <div class="metric-label">통화실성</div>
                <div style="font-size: 2rem; font-weight: 700; color: #ffa726; margin-top: 5px;">
                    0.90
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with koi_col3:
        st.markdown("""
        <div class="network-status">
            <div style="text-align: center;">
                <div class="metric-label">안정성지수</div>
                <div style="font-size: 2rem; font-weight: 700; color: #4caf50; margin-top: 5px;">
                    0.98
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Selective Active RIS 제어
    st.markdown("### 🔧 Selective Active RIS 제어")
    
    if 'ris_approved' not in st.session_state:
        st.session_state.ris_approved = False
    
    if not st.session_state.ris_approved:
        st.markdown("""
        <div style="background: rgba(255, 152, 0, 0.2); border: 2px solid #ff9800; border-radius: 10px; padding: 20px; margin: 15px 0;">
            <h4 style="color: #ffa726; margin-top: 0;">⚠️ Selective Active RIS 활성화 필요</h4>
            <p style="color: white; line-height: 1.8;">
                <strong>상황:</strong> 명동역 인근 불확실성 감지 (인파 밀집도 증가)<br>
                <strong>현재 모드:</strong> Passive RIS (기본 모드)<br>
                <strong>권장 조치:</strong> Active RIS로 전환하여 신호 품질 및 통신 안정성 향상
            </p>
            <div style="background: rgba(0, 0, 0, 0.3); padding: 10px; border-radius: 5px; margin-top: 10px;">
                <p style="color: #ffcc80; margin: 0; font-size: 0.95rem;">
                    <strong>⚡ Active RIS 효과:</strong><br>
                    • 신호 증폭률: +32dB → +45dB 향상<br>
                    • 링크 품질 개선 (Middle 통화실성 지표 상승)<br>
                    • 에이전트 AI의 비용 대비 효과 분석 완료
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col_ris1, col_ris2 = st.columns(2)
        with col_ris1:
            if st.button("✅ Active RIS 활성화 승인", key="approve_ris", use_container_width=True):
                st.session_state.ris_approved = True
                st.rerun()
        with col_ris2:
            if st.button("❌ 현재 모드 유지", key="deny_ris", use_container_width=True):
                st.info("Passive RIS 모드를 유지합니다.")
    else:
        st.success("✅ Active RIS 모드가 활성화되었습니다!")
        st.markdown("""
        <div style="background: rgba(76, 175, 80, 0.2); border: 2px solid #4caf50; border-radius: 10px; padding: 15px; margin: 15px 0;">
            <p style="color: white; line-height: 1.8; margin: 0;">
                <strong style="color: #81c784;">📡 Active RIS 상태:</strong><br>
                • 신호 증폭률: +45dB (High Performance Mode)<br>
                • 링크 품질: 우수 (Middle 지표 98.5%)<br>
                • 패턴 기반 자동 전환: 활성화됨<br>
                • 예상 추가 비용: 최소 (고품질 라벨)
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Passive 모드로 복귀", key="reset_ris"):
            st.session_state.ris_approved = False
            st.rerun()
    
    # 네트워크 제어 로그
    st.markdown("### 📋 네트워크 제어 로그")
    
    if st.session_state.ris_approved:
        log_content = f"""
        [{current_time.strftime('%H:%M:%S')}] 🚨 긴급 출동 감지 → URLLC 모드 자동 활성화<br>
        [{(current_time - timedelta(seconds=15)).strftime('%H:%M:%S')}] 📍 명동역 인근 인파 밀집 감지 (밀도: 8.2명/m²)<br>
        [{(current_time - timedelta(seconds=30)).strftime('%H:%M:%S')}] ⚡ <strong style="color: #4caf50;">Selective Active RIS 모드 활성화 승인됨</strong><br>
        [{(current_time - timedelta(seconds=35)).strftime('%H:%M:%S')}] 🔄 Active RIS 반사 모드 가동 중 (신호 증폭률: +45dB)<br>
        [{(current_time - timedelta(seconds=45)).strftime('%H:%M:%S')}] 🌐 6G AI Agent: 최적 경로 재계산 완료<br>
        [{(current_time - timedelta(seconds=60)).strftime('%H:%M:%S')}] ✅ 병원 3곳과 데이터 동기화 완료<br>
        [{(current_time - timedelta(seconds=75)).strftime('%H:%M:%S')}] 🔐 양자 보안 채널 수립 완료
        """
    else:
        log_content = f"""
        [{current_time.strftime('%H:%M:%S')}] 🚨 긴급 출동 감지 → URLLC 모드 자동 활성화<br>
        [{(current_time - timedelta(seconds=15)).strftime('%H:%M:%S')}] 📍 명동역 인근 인파 밀집 감지 (밀도: 8.2명/m²)<br>
        [{(current_time - timedelta(seconds=30)).strftime('%H:%M:%S')}] 🔄 RIS 반사 모드 가동 중 (신호 증폭률: +32dB)<br>
        [{(current_time - timedelta(seconds=45)).strftime('%H:%M:%S')}] 🌐 6G AI Agent: 최적 경로 재계산 완료<br>
        [{(current_time - timedelta(seconds=60)).strftime('%H:%M:%S')}] ✅ 병원 3곳과 데이터 동기화 완료<br>
        [{(current_time - timedelta(seconds=75)).strftime('%H:%M:%S')}] 🔐 양자 보안 채널 수립 완료
        """
    
    st.markdown(f"""
    <div class="network-log">
        {log_content}
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown("### 📊 시스템 모니터링")
    st.markdown('<p style="color: #90caf9; margin-bottom: 20px;">실시간 시스템 상태를 모니터링합니다.</p>', unsafe_allow_html=True)
    
    # 시스템 상태
    status_col1, status_col2 = st.columns(2)
    
    with status_col1:
        st.metric("활성 케이스", f"{len(st.session_state.emergency_cases)}건")
        st.metric("네트워크 지연", "< 10ms", delta="-2ms")
    
    with status_col2:
        st.metric("AI 응답 속도", "1.2초", delta="-0.3초")
        st.metric("시스템 가동률", "99.9%")
    
    st.markdown("---")
    
    # 최근 케이스 히스토리
    st.markdown("### 📋 최근 케이스 히스토리")
    
    if st.session_state.emergency_cases:
        for idx, case in enumerate(reversed(st.session_state.emergency_cases[-5:])):
            case_type = case.get('type', '알 수 없음')
            case_time = case.get('time', '시간 미상')
            
            if case_type == "신고음성":
                case_desc = f"{case.get('condition', '증상 미상')} - {case.get('call_location', '위치 미상')}"
            elif case_type == "웨어러블 기록":
                case_desc = f"{case.get('condition', '증상 미상')} - {case.get('gps_location', '위치 미상')}"
            elif case_type == "현장 처치 기록":
                case_desc = f"{case.get('condition', '증상 미상')} - {case.get('location', '위치 미상')}"
            else:
                case_desc = "상세 정보 없음"
            
            with st.expander(f"#{len(st.session_state.emergency_cases) - idx} - {case_type} ({case_time})"):
                st.write(f"**상황:** {case_desc}")
                st.write(f"**긴급도:** {case.get('severity', '미상')}")
    else:
        st.info("아직 케이스 히스토리가 없습니다.")

# 하단 안내
st.markdown("---")
st.markdown("### 💡 사용 안내")
st.info("""
이 대시보드는 Front Dashboard로부터 실시간으로 응급 케이스를 수신합니다.
- **AI 상황 요약**: 최신 케이스의 환자 정보와 상황을 자동으로 분석합니다.
- **추천 병원**: 환자의 위치와 증상에 따라 최적의 병원 3곳을 추천합니다.
- **처치 가이드**: 환자의 상태에 맞는 응급 처치 프로토콜을 실시간으로 제공합니다.
""")

# 자동 새로고침 옵션
if st.checkbox("🔄 실시간 업데이트 활성화 (2초마다 갱신)", value=False):
    time.sleep(2)
    st.rerun()