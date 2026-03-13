import streamlit as st

st.title("🛳️ Day5: Docker Compose")
st.progress(5/5)
st.balloons()

st.header("01. Docker Compose")
st.markdown("docker-compose.yml로 멀티 컨테이너 관리")

st.header("02. Docker Compose로 전환하기")
st.code("""
version: '3'
services:
  app:
    build: .
    ports: [\"8000:8000\"]
""")

st.header("03. 서비스 간 의존 관계 설정하기")
st.code("""
  db:
    image: mysql
  app:
    depends_on: [db]
""")
st.info("🏆 챌린지 완료! docker-compose up으로 실행해보세요.")
