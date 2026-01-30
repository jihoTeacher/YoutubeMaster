import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 페이지 설정
st.set_page_config(page_title="우리 반 온라인 건의함", page_icon="📮")

st.title("📮 행복한 우리 반 건의함")
st.markdown("여러분의 소중한 의견이 더 좋은 우리 반을 만듭니다.")

# --- 구글 스프레드시트 연결 설정 ---
# 시트 URL을 여기에 붙여넣으세요 (또는 secrets에 저장 가능)
sheet_url = "https://docs.google.com/spreadsheets/d/1SpUO6iHX1cnEkp26xEF-w1apY2NzF7ScJg8Ka0tTa-g/edit?usp=sharing"

conn = st.connection("gsheets", type=GSheetsConnection)

# --- 메뉴 선택 ---
menu = st.sidebar.radio("메뉴", ["의견 남기기", "선생님 확인용"])

if menu == "의견 남기기":
    st.subheader("📝 익명 건의서 작성")
    
    with st.form("suggestion_form"):
        category = st.selectbox("분류", ["환경개선", "수업관련", "교우관계", "기타"])
        title = st.text_input("한 줄 요약")
        content = st.text_area("상세 내용")
        submit = st.form_submit_button("전송하기")
        
        if submit:
            if title and content:
                # 1. 기존 데이터 읽기
                existing_data = conn.read(spreadsheet=sheet_url, usecols=[0,1,2,3])
                existing_data = existing_data.dropna(how="all")
                
                # 2. 새 데이터 생성
                new_entry = pd.DataFrame({
                    "날짜": [datetime.now().strftime("%Y-%m-%d %H:%M")],
                    "카테고리": [category],
                    "제목": [title],
                    "내용": [content]
                })
                
                # 3. 데이터 합치기 및 업데이트
                updated_df = pd.concat([existing_data, new_entry], ignore_index=True)
                conn.update(spreadsheet=sheet_url, data=updated_df)
                
                st.success("성공적으로 전달되었습니다. 익명이 보장되니 안심하세요!")
            else:
                st.warning("내용을 모두 채워주세요.")

elif menu == "선생님 확인용":
    st.subheader("🔒 건의함 목록")
    password = st.text_input("비밀번호", type="password")
    
    if password == "1234":  # 선생님만 아는 비밀번호
        # 시트 데이터 실시간 읽기
        data = conn.read(spreadsheet=sheet_url)
        data = data.dropna(how="all") # 빈 줄 제거
        
        if not data.empty:
            st.dataframe(data.sort_values(by="날짜", ascending=False), use_container_width=True)
            
            # 간단한 통계
            st.divider()
            st.write(f"현재 총 **{len(data)}건**의 의견이 접수되었습니다.")
        else:
            st.info("아직 접수된 내용이 없습니다.")
    elif password:
        st.error("비밀번호가 올바르지 않습니다.")
