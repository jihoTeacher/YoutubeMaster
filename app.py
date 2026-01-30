import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 페이지 설정
st.set_page_config(page_title="행복한 우리 반 건의함", page_icon="📮")

# 데이터 저장 파일 경로
DATA_FILE = "suggestions.csv"

# 데이터 불러오기 함수
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["날짜", "카테고리", "제목", "내용"])

# 데이터 저장 함수
def save_data(category, title, content):
    df = load_data()
    new_data = pd.DataFrame({
        "날짜": [datetime.now().strftime("%Y-%m-%d %H:%M")],
        "카테고리": [category],
        "제목": [title],
        "내용": [content]
    })
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')

# 사이드바 메뉴
menu = st.sidebar.selectbox("메뉴", ["건의하기", "건의함 확인(관리자)"])

# --- 건의하기 화면 ---
if menu == "건의하기":
    st.title("📮 우리 반 비밀 건의함")
    st.write("학급을 위해 하고 싶은 말을 자유롭게 남겨주세요. 내용은 익명으로 전달됩니다.")
    
    with st.form("suggestion_form", clear_on_submit=True):
        category = st.selectbox("카테고리", ["시설/환경", "수업 관련", "교우관계", "기타 의견"])
        title = st.text_input("제목", placeholder="한 줄 요약을 입력하세요.")
        content = st.text_area("내용", placeholder="상세한 의견을 적어주세요.")
        
        submit_button = st.form_submit_button("보내기")
        
        if submit_button:
            if title and content:
                save_data(category, title, content)
                st.success("건의사항이 안전하게 전달되었습니다! 감사합니다.")
            else:
                st.error("제목과 내용을 모두 입력해주세요.")

# --- 관리자 화면 ---
elif menu == "건의함 확인(관리자)":
    st.title("🔒 건의함 확인")
    
    password = st.text_input("관리자 비밀번호를 입력하세요.", type="password")
    
    # 실제 배포시에는 비밀번호를 환경변수 등으로 안전하게 관리해야 합니다.
    if password == "1234": # 초기 비밀번호
        st.success("환영합니다, 선생님!")
        df = load_data()
        
        if not df.empty:
            st.dataframe(df.sort_values(by="날짜", ascending=False), use_container_width=True)
            
            # 통계 보기
            st.subheader("📊 카테고리별 통계")
            st.bar_chart(df["카테고리"].value_counts())
            
            if st.button("내용 초기화(모두 삭제)"):
                if os.path.exists(DATA_FILE):
                    os.remove(DATA_FILE)
                    st.rerun()
        else:
            st.write("아직 접수된 건의사항이 없습니다.")
    elif password:
        st.error("비밀번호가 틀렸습니다.")
