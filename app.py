import streamlit as st
import yt_dlp
import os
import glob

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="YouTube Downloader",
    page_icon="🎬",
    layout="centered"
)

# 2. 제목 및 UI 구성
st.title("🎬 YouTube Downloader")
st.markdown("---")
st.write("유튜브 링크를 입력하면 **MP4 영상** 또는 **MP3 오디오**로 변환하여 다운로드할 수 있습니다.")

# URL 입력 창
url = st.text_input("YouTube URL을 입력하세요", placeholder="https://www.youtube.com/watch?v=...")

# 다운로드 옵션 선택
format_choice = st.radio(
    "저장 형식을 선택하세요:",
    ("MP4 (동영상 + 음성)", "MP3 (음원만 추출)"),
    horizontal=True
)

# 3. 다운로드 및 변환 로직
if url:
    try:
        # 영상 정보 미리 가져오기
        with yt_dlp.YoutubeDL() as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'video_file')
            thumbnail = info.get('thumbnail')
            
            # 영상 정보 표시
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(thumbnail, use_container_width=True)
            with col2:
                st.subheader(title)
                st.write(f"📺 채널: {info.get('uploader')}")

        # 다운로드 실행 버튼
        if st.button("🚀 변환 및 다운로드 준비", use_container_width=True):
            with st.spinner("서버에서 변환 중입니다. 잠시만 기다려 주세요..."):
                
                # 파일 확장자 설정
                is_mp3 = "MP3" in format_choice
                ext = "mp3" if is_mp3 else "mp4"
                
                # yt-dlp 옵션 설정
                ydl_opts = {
                    'format': 'bestaudio/best' if is_mp3 else 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                    'outtmpl': f'downloads/%(title)s.%(ext)s',  # downloads 폴더에 저장
                    'noplaylist': True,
                }

                # MP3 선택 시 오디오 추출 옵션 추가
                if is_mp3:
                    ydl_opts['postprocessors'] = [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }]

                # 실제 다운로드 실행
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                # 생성된 파일 경로 찾기
                # 특수 문자로 인한 파일명 변형 방지를 위해 glob 사용
                files = glob.glob("downloads/*")
                if files:
                    latest_file = max(files, key=os.path.getctime)
                    
                    with open(latest_file, "rb") as f:
                        file_data = f.read()
                        
                    st.success("✅ 변환 완료! 아래 버튼을 클릭하여 저장하세요.")
                    st.download_button(
                        label=f"💾 {ext.upper()} 파일 저장하기",
                        data=file_data,
                        file_name=os.path.basename(latest_file),
                        mime="audio/mpeg" if is_mp3 else "video/mp4",
                        use_container_width=True
                    )
                    
                    # (선택 사항) 서버 용량 관리를 위해 다운로드 후 임시 파일 삭제 로직을 넣을 수 있습니다.

    except Exception as e:
        st.error(f"❌ 오류가 발생했습니다: {e}")
        st.info("URL이 올바른지, 혹은 해당 영상이 국가 제한이나 연령 제한이 있는지 확인해 보세요.")

else:
    st.info("위 입력창에 유튜브 링크를 붙여넣어 주세요.")

# 하단 정보
st.markdown("---")
st.caption("⚠️ 본 도구는 개인 소장용 학습 목적으로만 사용하시기 바랍니다.")
