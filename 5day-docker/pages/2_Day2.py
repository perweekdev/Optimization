import streamlit as st

st.title("🛳️ Day2: 이미지 다루기")
st.progress(2/5)

st.header("01. 이미지 관리하기")
st.markdown("docker images, docker rmi 명령어로 확인/삭제")
st.code("docker images\n docker rmi <image_id>", "bash")

st.header("02. python 이미지 관리하기")
st.markdown("공식 Python 이미지 사용")
st.code("docker pull python:3.12-slim", "bash")

st.header("03. Dockerfile 작성하기")
st.code("""
FROM python:3.12-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD [\"python\", \"app.py\"]
""")

st.header("04. 이미지 빌드 / 배포하기")
st.code("docker build -t myapp .", "bash")