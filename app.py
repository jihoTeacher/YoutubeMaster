import streamlit as st

st.title("연결 테스트")
st.write("앱이 정상적으로 부팅되었습니다!")

# 라이브러리 로드 테스트
try:
    import pandas as pd
    from streamlit_gsheets import GSheetsConnection
    import yt_dlp
    st.success("모든 라이브러리가 성공적으로 로드되었습니다.")
except Exception as e:
    st.error(f"라이브러리 로드 중 오류: {e}")
