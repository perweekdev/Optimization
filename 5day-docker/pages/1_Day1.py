import streamlit as st

st.title("🛳️ Day1: Hello Docker")
progress = st.progress(1/5)
st.success("✅ Day1 완료!")

st.header("01. Hello Docker!")
st.markdown("""
도커는 컨테이너 기술로 애플리케이션을 패키징·배포합니다.
**docker --version**으로 설치 확인하세요.
```bash
docker --version
""")

st.header("02. 컨테이너와 이미지")
st.markdown("""

이미지: 실행 가능한 패키지 (템플릿)

컨테이너: 이미지의 실행 인스턴스
""")
st.code("""
docker pull hello-world # 이미지 다운로드
docker run hello-world # 컨테이너 실행
""", language="bash")