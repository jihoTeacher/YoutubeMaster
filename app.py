import streamlit as st
from pytubefix import YouTube
import os
import re

# 1. 요리 로봇 (기능)
class YouTubeMaster:
    def download_logic(self, url, mode):
        try:
            yt = YouTube(url)
            clean_title = re.sub(r'[\\/:*?"<>|]', '', yt.title)
            
            if mode == "🎬 영상 (720p)":
                stream = yt.streams.get_highest_resolution()
                file_path = stream.download(filename=f"{clean_title}.mp4")
                return file_path, f"{clean_title}.mp4"
            else:
                stream = yt.streams.get_audio_only()
                out_file = stream.download(filename=f"{clean_title}.m4a")
                new_file = clean_title + '.mp3'
                os.rename(out_file, new_file)
                return new_file, new_file
        except Exception as e:
            return None, f"❌ 에러 발생: {e}"

# 2. 웹 화면 꾸미기
st.set_page_config(page_title="나만의 유튜버 비서", page_icon="📺")
st.title("📺 YouTube Downloader")
st.write("주소를 넣고 원하는 형식을 골라보세요!")

url = st.text_input("YouTube URL을 붙여넣으세요", placeholder="https://www.youtube.com/...")
mode = st.radio("다운로드 형식 선택", ["🎬 영상 (720p)", "🎵 오디오 (MP3)"])

if st.button("파일 준비하기"):
    if url:
        master = YouTubeMaster()
        with st.spinner("유튜브에서 데이터를 가져오는 중..."):
            file_path, display_name = master.download_logic(url, mode)
            
        if file_path:
            st.success(f"준비 완료: {display_name}")
            # 웹앱은 서버에 저장된 파일을 사용자가 '다운로드' 버튼을 눌러 가져가게 해야 합니다.
            with open(file_path, "rb") as f:
                st.download_button(
                    label="내 컴퓨터로 저장하기",
                    data=f,
                    file_name=display_name
                    mime="video/mp4" if "🎬" in mode else "audio/mpeg"
                )
    else:

        st.warning("주소를 먼저 입력해주세요!")
