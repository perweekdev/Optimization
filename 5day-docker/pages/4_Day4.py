import streamlit as st

st.title("🛳️ Day4: 컨테이너 다루기(2)")
st.progress(4/5)

st.header("04. 네트워크")
st.markdown("docker network create, inspect")
st.code("docker network create mynet", "bash")

st.header("06. 같은 네트워크에서 fastapi 서버에 요청하기")
st.code("docker run --network mynet busybox wget fastapi-app:8000", "bash")

st.header("08. 볼륨")
st.markdown("데이터 지속성")

st.header("09. 볼륨으로 MySQL 데이터 유지하기")
st.code("""
docker volume create mysql-data
docker run -v mysql-data:/var/lib/mysql mysql
""")

st.header("10. 바인드 마운트로 MySQL 데이터 유지하기")
st.code("docker run -v /host/path:/var/lib/mysql mysql")
