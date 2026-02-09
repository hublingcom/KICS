import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import streamlit as st
import plotly.graph_objects as go

# 각 대시보드 파일 상단에 추가
if st.sidebar.button("🏠 메인 화면으로"):
    st.switch_page("main.py")

# 페이지 설정
st.set_page_config(
    page_title="⚙️ FIELD-DREAM Back Office",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS 스타일링
st.markdown("""
<style>
    /* 전체 배경 */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700;800&family=Noto+Sans+KR:wght@300;400;700;900&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #141e30 0%, #243b55 100%);
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    /* 메인 타이틀 */
    .main-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        text-align: center;
        color: #f093fb;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* KPI 카드 */
    .kpi-card {
        background: linear-gradient(135deg, rgba(240, 147, 251, 0.15) 0%, rgba(245, 87, 108, 0.15) 100%);
        border: 2px solid #f093fb;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(240, 147, 251, 0.3);
    }
    
    .kpi-excellent {
        border-color: #10b981;
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(5, 150, 105, 0.15) 100%);
    }
    
    .kpi-good {
        border-color: #3b82f6;
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(37, 99, 235, 0.15) 100%);
    }
    
    .kpi-warning {
        border-color: #f59e0b;
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(217, 119, 6, 0.15) 100%);
    }
    
    .kpi-danger {
        border-color: #ef4444;
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(220, 38, 38, 0.15) 100%);
    }
    
    /* Agent Tool 카드 */
    .tool-card {
        background: rgba(99, 102, 241, 0.1);
        border: 2px solid #6366f1;
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        transition: all 0.3s ease;
    }
    
    .tool-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.4);
    }
    
    .tool-active {
        border-color: #10b981;
        background: rgba(16, 185, 129, 0.1);
    }
    
    .tool-inactive {
        border-color: #6b7280;
        background: rgba(107, 114, 128, 0.1);
        opacity: 0.6;
    }
    
    /* 비용 분석 */
    .cost-box {
        background: rgba(245, 158, 11, 0.1);
        border: 2px solid #f59e0b;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    
    /* 리스크 알림 */
    .risk-alert {
        background: rgba(239, 68, 68, 0.15);
        border-left: 5px solid #ef4444;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        animation: pulse 2s infinite;
    }
    
    .risk-alert.medium {
        background: rgba(245, 158, 11, 0.15);
        border-left-color: #f59e0b;
    }
    
    .risk-alert.low {
        background: rgba(59, 130, 246, 0.15);
        border-left-color: #3b82f6;
    }
    
    /* 효율성 게이지 */
    .efficiency-gauge {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 10px;
        padding: 20px;
        text-align: center;
    }
    
    .gauge-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #10b981 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* 메트릭 */
    .metric-label {
        color: #cbd5e1;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 5px;
    }
    
    .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 2rem;
        font-weight: 700;
        color: #f093fb;
    }
    
    /* 테이블 스타일 */
    .data-table {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 10px;
        padding: 15px;
        overflow-x: auto;
    }
    
    .data-table table {
        width: 100%;
        border-collapse: collapse;
    }
    
    .data-table th {
        background: rgba(99, 102, 241, 0.3);
        color: #c7d2fe;
        padding: 12px;
        text-align: left;
        font-weight: 700;
        border-bottom: 2px solid #6366f1;
    }
    
    .data-table td {
        padding: 10px 12px;
        color: #e2e8f0;
        border-bottom: 1px solid rgba(99, 102, 241, 0.2);
    }
    
    .data-table tr:hover {
        background: rgba(99, 102, 241, 0.1);
    }
    
    /* 상태 배지 */
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 700;
    }
    
    .status-running {
        background: #10b981;
        color: white;
    }
    
    .status-idle {
        background: #6b7280;
        color: white;
    }
    
    .status-warning {
        background: #f59e0b;
        color: white;
    }
    
    .status-error {
        background: #ef4444;
        color: white;
    }
    
    /* 로그 뷰어 */
    .log-viewer {
        background: rgba(0, 0, 0, 0.5);
        border: 2px solid #6366f1;
        border-radius: 10px;
        padding: 15px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        max-height: 300px;
        overflow-y: auto;
        color: #10b981;
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'selective_ris_enabled' not in st.session_state:
    st.session_state.selective_ris_enabled = False
if 'total_cost' not in st.session_state:
    st.session_state.total_cost = 3240.50

# 헤더
st.markdown('<h1 class="main-title">⚙️ FIELD-DREAM Back Office</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">운영 리스크 관리 & KPI 모니터링 & AI Agent 제어</p>', unsafe_allow_html=True)

# 현재 시간
current_time = datetime.now()

# 상단 KPI 요약
st.markdown("### 📊 핵심 성과 지표 (KPI) 실시간 계산")

col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

with col_kpi1:
    st.markdown("""
    <div class="kpi-card kpi-warning">
        <div class="metric-label">운영목표달성도</div>
        <div class="metric-value" style="color: #f59e0b;">0.87</div>
        <div style="color: #fbbf24; font-size: 0.85rem; margin-top: 5px;">목표: 0.90 (3% 부족)</div>
        <div style="background: rgba(0,0,0,0.3); padding: 8px; border-radius: 5px; margin-top: 10px; font-size: 0.8rem; color: #fde68a;">
            • 골든타임 준수율: 94.2%<br>
            • 병원 매칭 성공률: 98.1%<br>
            • 평균 이송 시간: 8.3분
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_kpi2:
    st.markdown("""
    <div class="kpi-card kpi-good">
        <div class="metric-label">비용효율성</div>
        <div class="metric-value" style="color: #3b82f6;">0.90</div>
        <div style="color: #60a5fa; font-size: 0.85rem; margin-top: 5px;">목표: 0.85 (초과 달성)</div>
        <div style="background: rgba(0,0,0,0.3); padding: 8px; border-radius: 5px; margin-top: 10px; font-size: 0.8rem; color: #bfdbfe;">
            • 건당 운영비: ₩18,250<br>
            • RIS 모드 최적화율: 87%<br>
            • 에너지 절감: 23%
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_kpi3:
    st.markdown("""
    <div class="kpi-card kpi-excellent">
        <div class="metric-label">안정성지수</div>
        <div class="metric-value" style="color: #10b981;">0.98</div>
        <div style="color: #34d399; font-size: 0.85rem; margin-top: 5px;">목표: 0.95 (우수)</div>
        <div style="background: rgba(0,0,0,0.3); padding: 8px; border-radius: 5px; margin-top: 10px; font-size: 0.8rem; color: #6ee7b7;">
            • 시스템 가동률: 99.9%<br>
            • 네트워크 안정성: 99.2%<br>
            • 데이터 무결성: 100%
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_kpi4:
    st.markdown("""
    <div class="kpi-card kpi-excellent">
        <div class="metric-label">AI 정확도</div>
        <div class="metric-value" style="color: #10b981;">96.3%</div>
        <div style="color: #34d399; font-size: 0.85rem; margin-top: 5px;">목표: 95% (달성)</div>
        <div style="background: rgba(0,0,0,0.3); padding: 8px; border-radius: 5px; margin-top: 10px; font-size: 0.8rem; color: #6ee7b7;">
            • 트리아지 정확도: 97.1%<br>
            • 병원 매칭 정확도: 95.8%<br>
            • 오탐률: 2.3%
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# 메인 레이아웃
col_left, col_right = st.columns([1.2, 1])

with col_left:
    # Agentic AI Tool 현황
    st.markdown("### 🤖 Agentic AI Tool 현황")
    
    tools = [
        {
            "name": "Triage Analyzer",
            "status": "running",
            "description": "환자 중증도 자동 분류",
            "calls": 1247,
            "accuracy": "97.1%",
            "cost_per_call": "₩12"
        },
        {
            "name": "Hospital Matcher",
            "status": "running",
            "description": "최적 병원 매칭 알고리즘",
            "calls": 1189,
            "accuracy": "95.8%",
            "cost_per_call": "₩15"
        },
        {
            "name": "Network Optimizer",
            "status": "running",
            "description": "6G 네트워크 자원 최적화",
            "calls": 3421,
            "accuracy": "99.2%",
            "cost_per_call": "₩8"
        },
        {
            "name": "RIS Controller",
            "status": "running" if st.session_state.selective_ris_enabled else "idle",
            "description": "Selective Active RIS 제어",
            "calls": 234 if st.session_state.selective_ris_enabled else 0,
            "accuracy": "98.5%" if st.session_state.selective_ris_enabled else "N/A",
            "cost_per_call": "₩45"
        },
        {
            "name": "Cost Predictor",
            "status": "running",
            "description": "운영 비용 예측 및 최적화",
            "calls": 892,
            "accuracy": "94.3%",
            "cost_per_call": "₩10"
        }
    ]
    
    for tool in tools:
        status_class = f"status-{tool['status']}"
        tool_class = "tool-active" if tool['status'] == "running" else "tool-inactive"
        
        st.markdown(f"""
        <div class="tool-card {tool_class}">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="color: #818cf8; margin: 0;">{tool['name']}</h4>
                    <p style="color: #c7d2fe; font-size: 0.9rem; margin: 5px 0;">{tool['description']}</p>
                </div>
                <div class="status-badge {status_class}">{tool['status'].upper()}</div>
            </div>
            <div style="display: flex; gap: 20px; margin-top: 10px; color: #e0e7ff; font-size: 0.85rem;">
                <div>📞 호출: <strong>{tool['calls']}</strong></div>
                <div>🎯 정확도: <strong>{tool['accuracy']}</strong></div>
                <div>💰 건당 비용: <strong>{tool['cost_per_call']}</strong></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # 경고 및 알림
    st.markdown("### ⚠️ 운영 리스크 알림")
    
    st.markdown("""
    <div class="risk-alert medium">
        <h4 style="color: #f59e0b; margin: 0;">🟡 중간 리스크</h4>
        <p style="color: #fde68a; margin: 5px 0; line-height: 1.6;">
            <strong>운영목표달성도 0.87 (목표: 0.90)</strong><br>
            • 원인: 일부 병원 수용 지연으로 인한 평균 이송 시간 증가<br>
            • 영향: 골든타임 준수율 94.2% (목표: 97%)<br>
            • 권장 조치: Hospital Matcher AI 모델 재학습 또는 예비 병원 네트워크 확대
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="risk-alert low">
        <h4 style="color: #3b82f6; margin: 0;">🔵 낮은 리스크</h4>
        <p style="color: #bfdbfe; margin: 5px 0; line-height: 1.6;">
            <strong>Warm 메모리 사용률 28% (임계값: 80%)</strong><br>
            • 상태: 정상 범위 내<br>
            • 예상 최대 사용률: 45% (피크 타임 기준)<br>
            • 조치: 불필요 (모니터링 지속)
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="risk-alert low">
        <h4 style="color: #3b82f6; margin: 0;">🔵 낮은 리스크</h4>
        <p style="color: #bfdbfe; margin: 5px 0; line-height: 1.6;">
            <strong>RIS Controller 유휴 상태</strong><br>
            • 상태: Selective Active RIS 미활성화<br>
            • 잠재 영향: 인파 밀집 지역 통신 품질 저하 가능<br>
            • 권장: 필요 시 Front/Mid 계층에서 수동 활성화
        </p>
    </div>
    """, unsafe_allow_html=True)



with col_right:
    # 비용 운영 효율 분석
    st.markdown("### 💰 비용 운영 효율 분석")
    
    st.markdown(f"""
    <div class="efficiency-gauge">
        <div class="gauge-value">90%</div>
        <div style="color: #cbd5e1; font-size: 1rem; margin-top: 10px;">비용 효율성 지수</div>
        <div style="color: #10b981; font-size: 0.85rem; margin-top: 5px;">✓ 목표 대비 +5% 초과 달성</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="cost-box">
        <h4 style="color: #fbbf24; margin-top: 0;">📈 금일 운영 비용 (실시간)</h4>
        <div style="font-size: 2rem; font-weight: 700; color: #fde68a; margin: 10px 0;">
            ₩{st.session_state.total_cost:,.2f}
        </div>
        <div style="color: #fef3c7; font-size: 0.85rem; line-height: 1.8;">
            • AI Tool 사용료: ₩1,847.30<br>
            • 6G 네트워크 비용: ₩892.50<br>
            • RIS 운영비: ₩{(234 * 45) if st.session_state.selective_ris_enabled else 0:,.0f}<br>
            • 클라우드 인프라: ₩500.70
        </div>
        <div style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 5px; margin-top: 10px;">
            <strong style="color: #fcd34d;">예상 월간 비용:</strong> 
            <span style="color: #fef3c7; font-size: 1.2rem; font-weight: 700;">₩97,215</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Selective RIS 비용 최적화
    st.markdown("### 🎛️ Selective Active RIS 제어")
    
    if not st.session_state.selective_ris_enabled:
        st.markdown("""
        <div style="background: rgba(107, 114, 128, 0.2); border: 2px solid #6b7280; border-radius: 10px; padding: 15px;">
            <h4 style="color: #9ca3af; margin-top: 0;">현재 상태: Passive Mode (기본)</h4>
            <p style="color: #d1d5db; font-size: 0.9rem; line-height: 1.6;">
                • 에너지 절약 모드 운영 중<br>
                • 건당 추가 비용: ₩0<br>
                • 통신 품질: 일반 수준
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: rgba(16, 185, 129, 0.2); border: 2px solid #10b981; border-radius: 10px; padding: 15px;">
            <h4 style="color: #34d399; margin-top: 0;">현재 상태: Active Mode (활성화)</h4>
            <p style="color: #6ee7b7; font-size: 0.9rem; line-height: 1.6;">
                • 고성능 모드 운영 중<br>
                • 오늘 활성화 횟수: 234회<br>
                • 추가 비용: ₩10,530 (건당 ₩45)<br>
                • 통신 품질: 우수 (+32dB → +45dB)
            </p>
            <div style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 5px; margin-top: 10px;">
                <strong style="color: #10b981;">💡 비용 vs 효과 분석:</strong><br>
                <span style="color: #a7f3d0; font-size: 0.85rem;">
                추가 비용 대비 통신 안정성 15% 향상<br>
                병원 매칭 성공률 2.3% 증가 → ROI: 긍정적
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # 최적화 권장사항
    st.markdown("### 💡 AI 최적화 권장사항")
    
    st.markdown("""
    <div style="background: rgba(99, 102, 241, 0.15); border: 2px solid #6366f1; border-radius: 10px; padding: 15px;">
        <h4 style="color: #818cf8; margin-top: 0;">📌 우선순위 Top 3</h4>
        <div style="color: #e0e7ff; font-size: 0.9rem; line-height: 2;">
            <strong>1. Hospital Matcher 재학습</strong><br>
            <span style="color: #c7d2fe; font-size: 0.85rem;">
            → 최근 2주 데이터 기반 모델 업데이트<br>
            → 예상 정확도 향상: 95.8% → 97.5%<br>
            → 예상 비용: ₩50,000 (1회성)
            </span><br><br>
            
            <strong>2. Cold 메모리 아카이브 정책 조정</strong><br>
            <span style="color: #c7d2fe; font-size: 0.85rem;">
            → 30일 → 90일 보관으로 변경<br>
            → 장기 트렌드 분석 가능<br>
            → 추가 저장 비용: ₩12,000/월
            </span><br><br>
            
            <strong>3. RIS 자동 모드 전환 임계값 조정</strong><br>
            <span style="color: #c7d2fe; font-size: 0.85rem;">
            → 현재: 수동 전환<br>
            → 권장: 인파 밀도 8.0명/m² 이상 시 자동 전환<br>
            → 예상 비용 절감: 15% (불필요한 활성화 방지)
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# 하단: 상세 테이블 및 로그
col_table, col_log = st.columns([1.2, 1])

with col_table:
    st.markdown("### 📊 AI Tool 성능 상세 테이블")
    
    df_tools = pd.DataFrame([
        ["Triage Analyzer", "1,247", "97.1%", "₩12", "18ms", "정상"],
        ["Hospital Matcher", "1,189", "95.8%", "₩15", "22ms", "정상"],
        ["Network Optimizer", "3,421", "99.2%", "₩8", "12ms", "정상"],
        ["RIS Controller", "234" if st.session_state.selective_ris_enabled else "0", 
         "98.5%" if st.session_state.selective_ris_enabled else "N/A", "₩45", 
         "35ms" if st.session_state.selective_ris_enabled else "N/A", 
         "활성화" if st.session_state.selective_ris_enabled else "유휴"],
        ["Cost Predictor", "892", "94.3%", "₩10", "15ms", "정상"]
    ], columns=["Tool 이름", "총 호출", "정확도", "건당 비용", "평균 응답", "상태"])
    
    st.markdown("""
    <div class="data-table">
    """ + df_tools.to_html(index=False, escape=False) + """
    </div>
    """, unsafe_allow_html=True)
    
    # KPI 계산 공식
    st.markdown("### 🧮 KPI 계산 공식")
    st.markdown("""
    <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 10px; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: #cbd5e1;">
        <strong style="color: #f093fb;">운영목표달성도 (KPI₁):</strong><br>
        KPI₁ = (골든타임_준수율 × 0.4) + (병원매칭_성공률 × 0.35) + (평균이송시간_점수 × 0.25)<br>
        = (0.942 × 0.4) + (0.981 × 0.35) + (0.83 × 0.25) = <strong style="color: #f59e0b;">0.87</strong><br><br>
        
        <strong style="color: #f093fb;">비용효율성 (KPI₂):</strong><br>
        KPI₂ = 1 - (실제_비용 / 예산_비용) + (절감률 × 0.3)<br>
        = 1 - (97,215 / 120,000) + (0.23 × 0.3) = <strong style="color: #3b82f6;">0.90</strong><br><br>
        
        <strong style="color: #f093fb;">안정성지수 (KPI₃):</strong><br>
        KPI₃ = (시스템_가동률 × 0.4) + (네트워크_안정성 × 0.35) + (데이터_무결성 × 0.25)<br>
        = (0.999 × 0.4) + (0.992 × 0.35) + (1.0 × 0.25) = <strong style="color: #10b981;">0.98</strong>
    </div>
    """, unsafe_allow_html=True)

with col_log:
    st.markdown("### 📝 Back Office 운영 로그")
    
    logs = [
        f"[{current_time.strftime('%H:%M:%S')}] ✓ KPI 자동 계산 완료",
        f"[{(current_time - timedelta(seconds=5)).strftime('%H:%M:%S')}] ⚠️ 운영목표달성도 0.87 (목표 미달)",
        f"[{(current_time - timedelta(seconds=10)).strftime('%H:%M:%S')}] ✓ AI Tool 성능 모니터링 완료",
        f"[{(current_time - timedelta(seconds=15)).strftime('%H:%M:%S')}] ℹ️ Hospital Matcher 재학습 권장",
        f"[{(current_time - timedelta(seconds=20)).strftime('%H:%M:%S')}] ✓ 비용 예측 업데이트: ₩97,215/월",
        f"[{(current_time - timedelta(seconds=25)).strftime('%H:%M:%S')}] ✓ RIS Controller 상태 체크",
        f"[{(current_time - timedelta(seconds=30)).strftime('%H:%M:%S')}] ℹ️ Cold 메모리 아카이브 진행 중",
        f"[{(current_time - timedelta(seconds=35)).strftime('%H:%M:%S')}] ✓ Network Optimizer 정상 작동",
        f"[{(current_time - timedelta(seconds=40)).strftime('%H:%M:%S')}] ✓ 데이터 무결성 검증 완료",
    ]
    
    log_html = ""
    for log in logs:
        log_html += f'<div style="margin: 5px 0; padding: 5px; border-bottom: 1px solid rgba(99,102,241,0.2);">{log}</div>'
    
    st.markdown(f'<div class="log-viewer">{log_html}</div>', unsafe_allow_html=True)
    
    # 시스템 헬스 체크
    st.markdown("### 🏥 시스템 헬스 체크")
    
    health_items = [
        ("CPU 사용률", "42%", "정상", "#10b981"),
        ("메모리 사용률", "67%", "정상", "#10b981"),
        ("디스크 I/O", "1.2 GB/s", "정상", "#10b981"),
        ("API 응답 시간", "18ms", "정상", "#10b981"),
        ("동시 접속", "47", "정상", "#10b981"),
    ]
    
    for item, value, status, color in health_items:
        st.markdown(f"""
        <div style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 8px; margin: 8px 0; border-left: 4px solid {color};">
            <div style="display: flex; justify-content: space-between;">
                <span style="color: #cbd5e1;">{item}</span>
                <div>
                    <span style="color: {color}; font-weight: 700; margin-right: 10px;">{value}</span>
                    <span style="color: {color}; font-size: 0.85rem;">✓ {status}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ========================================
# 신호 품질 개선 그래프 (RIS 효과 시각화)
# ========================================
st.markdown("### 📈 신호 품질 개선 효과 (Selective Active RIS)")

# 시간 데이터 생성 (0~60초)
time_points = list(range(0, 61))

# RIS 미적용 시나리오 (신호가 떨어지고 회복 안됨)
snr_without_ris = []
for t in time_points:
    if t < 20:
        # 정상 구간
        snr_without_ris.append(25 + np.random.normal(0, 0.5))
    elif t < 40:
        # 인파 밀집 지역 진입 - 신호 급락
        drop_factor = (t - 20) / 20
        snr_without_ris.append(25 - 18 * drop_factor + np.random.normal(0, 1))
    else:
        # 저품질 지속
        snr_without_ris.append(7 + np.random.normal(0, 0.8))

# Selective RIS 적용 시나리오 (신호 떨어지다가 Active Mode로 회복)
snr_with_ris = []
uncertainty_point = 25  # 불확실성 감지 시점
active_start = 28       # Active Mode 활성화 시점

for t in time_points:
    if t < 20:
        # 정상 구간
        snr_with_ris.append(25 + np.random.normal(0, 0.5))
    elif t < uncertainty_point:
        # 인파 밀집 지역 진입 - 신호 하락 시작
        drop_factor = (t - 20) / 5
        snr_with_ris.append(25 - 8 * drop_factor + np.random.normal(0, 1))
    elif t < active_start:
        # 불확실성 감지, Active Mode 전환 준비
        snr_with_ris.append(17 + np.random.normal(0, 0.8))
    elif t < active_start + 5:
        # Active Mode 활성화 - 급격한 신호 회복 (+32dB 증폭)
        recovery_factor = (t - active_start) / 5
        snr_with_ris.append(17 + 15 * recovery_factor + np.random.normal(0, 0.5))
    else:
        # Active Mode로 고품질 유지
        snr_with_ris.append(32 + np.random.normal(0, 0.5))

# 데이터프레임 생성
df_signal = pd.DataFrame({
    'Time (초)': time_points,
    'RIS 미적용 (Passive Mode)': snr_without_ris,
    'Selective Active RIS': snr_with_ris
})

# Plotly 그래프 생성
import plotly.graph_objects as go
fig = go.Figure()

# RIS 미적용 라인
fig.add_trace(go.Scatter(
    x=df_signal['Time (초)'],
    y=df_signal['RIS 미적용 (Passive Mode)'],
    mode='lines',
    name='RIS 미적용 (Passive Mode)',
    line=dict(color='#ef4444', width=3, dash='dash'),
    hovertemplate='시간: %{x}초<br>신호품질: %{y:.1f} dB<extra></extra>'
))

# Selective RIS 적용 라인
fig.add_trace(go.Scatter(
    x=df_signal['Time (초)'],
    y=df_signal['Selective Active RIS'],
    mode='lines',
    name='Selective Active RIS',
    line=dict(color='#10b981', width=3),
    hovertemplate='시간: %{x}초<br>신호품질: %{y:.1f} dB<extra></extra>'
))

# 불확실성 감지 지점 표시 (선만)
fig.add_vline(
    x=uncertainty_point, 
    line_dash="dot", 
    line_color="#fbbf24"
)

# Active Mode 활성화 지점 표시 (선만)
fig.add_vline(
    x=active_start, 
    line_dash="dot", 
    line_color="#10b981"
)

# 레이아웃 설정
fig.update_layout(
    title={
        'text': '📡 신호 품질 비교: RIS 미적용 vs Selective Active RIS',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 18, 'color': '#00d4ff', 'family': 'Orbitron'}
    },
    xaxis_title='시간 (초)',
    yaxis_title='신호 품질 (SNR, dB)',
    hovermode='x unified',
    plot_bgcolor='rgba(0, 0, 0, 0.3)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    font=dict(color='white', size=12),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5,
        bgcolor='rgba(0, 0, 0, 0.5)',
        bordercolor='#00d4ff',
        borderwidth=1
    ),
    height=400,
    margin=dict(l=50, r=50, t=80, b=50)
)

# 그리드 및 축 스타일링
fig.update_xaxes(
    showgrid=True,
    gridwidth=1,
    gridcolor='rgba(255, 255, 255, 0.1)',
    zeroline=False
)

fig.update_yaxes(
    showgrid=True,
    gridwidth=1,
    gridcolor='rgba(255, 255, 255, 0.1)',
    zeroline=False,
    range=[0, 40]
)

# annotation을 별도로 추가 (레이아웃 이후에)
fig.add_annotation(
    x=uncertainty_point,
    y=35,  # Y축 고정 위치
    text="🚨 불확실성 감지",
    showarrow=True,
    arrowhead=2,
    arrowcolor="#fbbf24",
    font=dict(color="#fbbf24", size=11),
    bgcolor="rgba(0, 0, 0, 0.7)",
    bordercolor="#fbbf24"
)

fig.add_annotation(
    x=active_start,
    y=32,  # 다른 Y축 위치
    text="⚡ Active Mode ON",
    showarrow=True,
    arrowhead=2,
    arrowcolor="#10b981",
    font=dict(color="#10b981", size=11),
    bgcolor="rgba(0, 0, 0, 0.7)",
    bordercolor="#10b981"
)

# 그래프 표시
st.plotly_chart(fig, use_container_width=True)

# 그래프 설명
st.markdown("""
<div style="background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%); 
            border: 2px solid #00d4ff; border-radius: 10px; padding: 20px; margin-top: 15px;">
    <h4 style="color: #00d4ff; margin-top: 0;">💡 그래프 해석</h4>
    <p style="color: white; line-height: 1.8;">
        <strong style="color: #ef4444;">🔴 RIS 미적용 (빨간선):</strong> 
        인파 밀집 지역(명동역) 진입 시 신호 품질이 25dB에서 7dB까지 급락하여 
        통신 품질이 크게 저하되고 회복되지 않습니다.<br><br>
        
        <strong style="color: #10b981;">🟢 Selective Active RIS (초록선):</strong> 
        불확실성 감지(25초) 후 Active Mode 전환(28초)과 동시에 
        <strong style="color: #fbbf24;">+15dB 증폭</strong>되어 32dB의 고품질 신호로 즉시 회복됩니다.<br><br>
        
        <strong style="color: #00d4ff;">✅ 효과:</strong> 
        극한 환경(인파 밀집)에서도 <strong>끊김 없는 6G 의료 서비스(URLLC)</strong>를 보장하여 
        응급 상황에서 생명을 구하는 통신 품질을 유지합니다.
    </p>
</div>
""", unsafe_allow_html=True)

# 자동 새로고침
if st.checkbox("🔄 실시간 모니터링 활성화", value=False):
    time.sleep(1)
    st.rerun()
