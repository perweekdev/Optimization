import streamlit as st
import os

st.set_page_config(page_title="도커 스터디 챌린지 5일", page_icon="🛳️", layout="wide")

st.title("🛳️ 도커 스터디 챌린지 5일")
st.markdown("""
이 챌린지는 도커의 기초부터 Docker Compose까지 5일 만에 익히는 웹입니다.  
매일 1~4개의 주제를 따라하며 실습하세요!
""")

# 사이드바에 일자 목록 (새 파일명에 맞춤)
st.sidebar.title("📅 일정")
st.sidebar.page_link("pages/1_Day1.py", label="🛳️ Day1: Hello Docker")
st.sidebar.page_link("pages/2_Day2.py", label="🛳️ Day2: 이미지 다루기")
st.sidebar.page_link("pages/3_Day3.py", label="🛳️ Day3: 컨테이너 다루기")
st.sidebar.page_link("pages/4_Day4.py", label="🛳️ Day4: 컨테이너 다루기(2)")
st.sidebar.page_link("pages/5_Day5.py", label="🛳️ Day5: Docker Compose")

st.markdown("---")
st.info("💡 **시작하세요:** 사이드바에서 Day를 선택하거나 직접 페이지로 이동하세요.")