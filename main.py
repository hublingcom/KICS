import streamlit as st

st.set_page_config(page_title="Emergency Management System", layout="wide")

st.title("🏥 Emergency Management System")
st.markdown("---")

# 3개의 섹션으로 나누어 표시
col1, col2, col3 = st.columns(3)

with col1:
    st.header("🚑 Front Office")
    st.write("현장 응급 관리 대시보드")
    if st.button("Front Office 이동", key="front", use_container_width=True):
        st.switch_page("pages/front_dashboard.py")

with col2:
    st.header("📊 Mid Office")
    st.write("병원 및 구급 현황 모니터링")
    
    if st.button("병원 대시보드", key="hospital", use_container_width=True):
        st.switch_page("pages/hospital_dashboard3.py")
    
    if st.button("구급 대시보드", key="paramedic", use_container_width=True):
        st.switch_page("pages/paramedic_dashboard3.py")

with col3:
    st.header("⚙️ Back Office")
    st.write("시스템 관리 및 설정")
    if st.button("Back Office 이동", key="back", use_container_width=True):
        st.switch_page("pages/back_office_dashboard.py")

st.markdown("---")
st.info("👆 원하시는 대시보드를 선택하세요")