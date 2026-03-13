import streamlit as st

st.title("🛳️ Day3: 컨테이너 다루기")
st.progress(3/5)

st.header("01. 컨테이너 실행하기")
st.code("docker run -d -p 8000:8000 myapp", "bash")

st.header("02. 컨테이너 관리하기")
st.markdown("docker ps, docker stop, docker logs")
st.code("docker ps -a\n docker stop <container_id>", "bash")

st.header("03. fastapi 컨테이너 실행하기")
st.code("""
docker run -d -p 8000:8000 --name fastapi-app python:3.12-slim uvicorn main:app
""")
