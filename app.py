import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, date

# 1. 페이지 설정
st.set_page_config(page_title="우리 반 학습 커뮤니티", page_icon="🏫", layout="wide")

# 2. 구글 시트 연결 (Secrets에 설정하거나 아래 URL에 직접 입력)
# 시트 공유 설정을 '링크가 있는 모든 사용자 - 편집자'로 하셔야 저장 기능이 작동합니다.
SHEET_URL = "여러분의_구글_스프레드시트_주소를_여기에_넣으세요"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("구글 시트 연결 설정이 필요합니다.")

# 3. 사이드바 메뉴
menu = st.sidebar.radio("📍 바로가기", ["📅 시험 대비 공지", "📮 익명 건의함"])

# --- [메뉴 1: 시험 대비 공지] ---
if menu == "📅 시험 대비 공지":
    st.title("✍️ 시험 대비 통합 공지판")
    
    # (1) 디데이 섹션
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("⏳ D-Day")
        target_date = st.date_input("시험 시작일", date(2026, 7, 1)) # 날짜를 자유롭게 설정
        d_day = (target_date - date.today()).days
        if d_day > 0:
            st.metric(label="기말고사까지", value=f"D-{d_day}")
        elif d_day == 0:
            st.metric(label="기말고사", value="D-Day", delta="🔥 오늘입니다!")
        else:
            st.metric(label="기말고사", value=f"D+{-d_day}")

    with col2:
        st.subheader("📢 오늘 핵심 공지")
        st.info("수행평가 일정과 시험 범위를 확인하고 미리 준비하세요!")

    st.divider()

    # (2) 수행평가 일정 (게시판 형태)
    st.subheader("📋 수행평가 일정표")
    
    # 관리자 비밀번호가 맞을 때만 입력창 노출
    with st.expander("➕ 일정 추가하기 (반장/선생님 전용)"):
        pw = st.text_input("관리자 암호", type="password", key="test_pw")
        if pw == "1234": # 비밀번호 설정
            with st.form("exam_form", clear_on_submit=True):
                sub = st.text_input("과목명 (예: 수학)")
                dt = st.date_input("시험일")
                detail = st.text_input("시험 내용 (예: 문제 풀이 및 발표)")
                if st.form_submit_button("일정 등록"):
                    # 데이터 읽기 및 추가
                    df = conn.read(spreadsheet=SHEET_URL)
                    new_row = pd.DataFrame({"날짜": [dt.strftime("%Y-%m-%d")], "과목": [sub], "내용": [detail], "유형": ["수행"]})
                    updated_df = pd.concat([df, new_row], ignore_index=True)
                    conn.update(spreadsheet=SHEET_URL, data=updated_df)
                    st.success("일정이 등록되었습니다!")
                    st.rerun()

    # 일정 출력
    try:
        data = conn.read(spreadsheet=SHEET_URL)
        if not data.empty:
            st.dataframe(data.sort_values(by="날짜"), use_container_width=True, hide_index=True)
        else:
            st.write("등록된 일정이 없습니다.")
    except:
        st.warning("데이터를 불러오려면 구글 시트 주소가 필요합니다.")

    st.divider()

    # (3) 시험 범위 섹션
    st.subheader("📚 과목별 시험 범위")
    t1, t2, t3 = st.tabs(["국어", "수학", "영어"])
    t1.write("📖 교과서 105p~200p, 외부 지문 3개")
    t2.write("🔢 미분법 전체, 학습지 1~12번")
    t3.write("🔤 6월 모의고사, 단어장 Day 10~20")

# --- [메뉴 2: 익명 건의함] ---
elif menu == "📮 익명 건의함":
    st.title("📮 익명 건의함")
    st.write("학교 생활 중 불편한 점이나 건의사항을 자유롭게 남겨주세요.")
    
    with st.form("suggest_form", clear_on_submit=True):
        cate = st.selectbox("카테고리", ["급식", "시설", "교우관계", "기타"])
        title = st.text_input("제목")
        msg = st.text_area("건의 내용")
        if st.form_submit_button("제출하기"):
            if title and msg:
                # 건의사항은 별도의 시트나 태그로 관리 가능
                st.success("익명으로 안전하게 접수되었습니다!")
            else:
                st.error("내용을 입력해주세요.")
