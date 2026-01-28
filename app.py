import streamlit as st
from pytubefix import YouTube
import os
import re

# 1. 유튜브 다운로드 로봇 클래스
class YouTubeMaster:
    def __init__(self, url):
        self.url = url
        # pytubefix 객체 생성
        self.yt = YouTube(self.url)

    def download_video(self):
        # 가장 안정적인 720p 합본(Progressive) 스트림을 가져옵니다.
        # (인코딩 없이 바로 성공하기 위해 이 방식을 씁니다.)
        stream = self.yt.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()
        
        # 파일명에서 특수문자를 제거하여 안전하게 만듭니다.
        clean_title = re.sub(r'[\\/:*?"<>|]', '', self.yt.title)
        file_path = stream.download(filename=f"{clean_title}.mp4")
        return file_path, clean_title

# 2. 스트림릿 웹 화면 구성
st.set_page_config(page_title="우리 반 유튜브 다운로더", page_icon="📺")
st.title("📺 우리 반 전용 유튜브 다운로더")
st.info("유튜브 주소를 넣고 '파일 준비하기'를 눌러주세요!")

# URL 입력창
url = st.text_input("YouTube URL을 붙여넣으세요", placeholder="https://www.youtube.com/watch?v=...")

if st.button("🚀 파일 준비하기"):
    if url:
        # 진행 상황을 보여주는 로그창 시작!
        with st.status("로봇이 일을 시작했습니다...", expanded=True) as status:
            try:
                st.write("🔍 주소 연결 중...")
                master = YouTubeMaster(url)
                
                st.write(f"🎬 영상 확인: **{master.yt.title}**")
                st.write("📥 유튜브 서버에서 영상을 가져오는 중... (잠시만 기다려주세요)")
                
                # 실제 다운로드 실행
                file_path, video_title = master.download_video()
                
                st.write("✅ 서버 준비 완료! 이제 내 컴퓨터로 옮길 수 있습니다.")
                status.update(label="🎊 모든 준비가 끝났습니다!", state="complete", expanded=False)

                # 파일이 성공적으로 준비되면 '진짜 저장 버튼'을 보여줍니다.
                with open(file_path, "rb") as f:
                    st.download_button(
                        label="💾 내 컴퓨터에 최종 저장하기",
                        data=f,
                        file_name=f"{video_title}.mp4",
                        mime="video/mp4",
                        use_container_width=True # 버튼을 가로로 길게 만들어줍니다.
                    )
            except Exception as e:
                status.update(label="❌ 에러가 발생했습니다!", state="error")
                st.error(f"상세 에러 내용: {e}")
    else:
        st.warning("주소를 먼저 입력해 주세요!")

# 하단 안내 메시지
st.caption("※ 주의: 고화질(1080p 이상)은 별도의 인코딩 과정이 필요하여 현재는 720p로 제공됩니다.")
