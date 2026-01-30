import streamlit as st
import pandas as pd
from datetime import datetime, date

# --- 시험 대비 공지 페이지 ---
if menu == "📝 시험 대비 공지":
    st.title("📝 시험 대비 정보 공유")
    
    # 1. D-Day 설정
    st.subheader("⏳ 시험 카운트다운")
    exam_date = st.date_input("시험 시작일을 선택하세요", date(2024, 7, 1)) # 기본값 설정
    today = date.today()
    d_day = (exam_date - today).days
    
    if d_day > 0:
        st.metric(label="기말고사까지", value=f"D-{d_day}")
    elif d_day == 0:
        st.balloons()
        st.metric(label="기말고사", value="D-Day")
    else:
        st.metric(label="기말고사", value=f"D+{-d_day}")

    st.divider()

    # 2. 수행평가 일정 (입력 및 출력)
    st.subheader("📅 수행평가 일정")
    
    # 입력 폼
    with st.expander("➕ 수행평가 일정 추가하기"):
        with st.form("performance_test_form", clear_on_submit=True):
            sub_name = st.text_input("과목명")
            test_date = st.date_input("시험 날짜")
            test_info = st.text_input("시험 내용 (예: 에세이 쓰기, 발표 등)")
            submit_test = st.form_submit_button("등록하기")
            
            if submit_test:
                # [구글 시트 연동 시] 위 건의함처럼 conn.update 로직 추가 필요
                st.success(f"{sub_name} 수행평가가 등록되었습니다.")
                # 테스트용 데이터 저장 (실제 배포 시엔 구글 시트에 누적 저장되도록 설정)

    # 출력 게시판 (예시 데이터)
    # 실제로는 conn.read()로 가져온 데이터를 보여줍니다.
    sample_data = pd.DataFrame([
        {"과목": "수학", "날짜": "2024-06-15", "내용": "삼각함수 프린트물 풀이"},
        {"과목": "영어", "날짜": "2024-06-18", "내용": "단어 200개 받아쓰기"}
    ])
    st.table(sample_data) # 게시판 형태로 깔끔하게 출력

    st.divider()

    # 3. 과목별 시험범위
    st.subheader("📚 지필평가 시험범위")
    
    # 과목별로 탭을 나누어 깔끔하게 표시
    tab1, tab2, tab3 = st.tabs(["국어", "수학", "영어"])
    with tab1:
        st.info("교과서: 1단원 ~ 3단원 / 유인물: 현대시 5선")
    with tab2:
        st.info("교과서: 처음부터 미분까지 / 익힘책: 전 범위")
    with tab3:
        st.info("모의고사: 2023년 6월물 / 교과서: 5, 6과")
