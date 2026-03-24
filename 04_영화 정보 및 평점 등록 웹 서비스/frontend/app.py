"""
Movie Review Service - Main App
로그인 + 회원가입 모달
"""

import streamlit as st
import requests
from dotenv import load_dotenv


# 환경변수 로드
load_dotenv()


# 페이지 설정
st.set_page_config(
    page_title="Movie Review 🎬",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# 세션 상태 초기화
if "token" not in st.session_state:
    st.session_state.token = None
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "username" not in st.session_state:
    st.session_state.username = None


# API URL
API_URL = "http://localhost:8000"


# ===== 회원가입 모달 함수 =====
@st.dialog("📝 회원가입", width="medium")
def register_dialog():
    st.markdown("### 새 계정 생성")

    reg_username = st.text_input("아이디", placeholder="ID")
    reg_email = st.text_input("이메일", placeholder="user@example.com")
    reg_password = st.text_input("비밀번호", type="password", placeholder="password")

    if st.button("회원가입 완료", use_container_width=True):
        if not all([reg_username, reg_email, reg_password]):
            st.error("모든 필드를 입력하세요.")
        else:
            register_url = f"{API_URL}/auth/register"
            register_data = {
                "username": reg_username,
                "email": reg_email,
                "password": reg_password
            }

            try:
                response = requests.post(register_url, json=register_data)
                if response.status_code == 200:
                    st.success("✅ 회원가입 성공! 이제 로그인하세요.")
                    st.rerun()
                else:
                    try:
                        detail = response.json().get("detail", "Unknown")
                    except Exception:
                        detail = response.text
                    st.error(f"회원가입 실패: {detail}")
            except Exception as e:
                st.error(f"서버 오류: {str(e)}")

    if st.button("❌ 취소", use_container_width=True):
        st.rerun()


# ===== 마이 프로필 모달 =====
@st.dialog("👤 My Profile", width="medium")
def my_profile_dialog():
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    response = requests.get(f"{API_URL}/auth/me", headers=headers)

    if response.status_code == 200:
        user_info = response.json()
        st.markdown("### 내 정보")
        st.write(f"**Username**: {user_info.get('username', '-')}")
        st.write(f"**Email**: {user_info.get('email', '-')}")
        st.write(f"**User ID**: {user_info.get('user_id', '-')}")
    else:
        st.error("프로필 정보를 불러오지 못했습니다.")

    if st.button("닫기", use_container_width=True):
        st.rerun()


# ===== 메인 앱 =====
st.title("🎬 Movie Review Service")
st.markdown("---")


# 로그인 상태 표시
if st.session_state.token:
    st.markdown(f"## {st.session_state.username} 님, 환영합니다!")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    ### 서비스 이용 안내
    사이드바에서 아래 페이지들을 이용해보세요.
    - **Movies**: 최신 영화 조회, 리뷰 보기 및 작성
    - **My Reviews**: 내 리뷰 관리
    - **Recent Reviews**: 최근 리뷰 확인
    """)

    action_col1, action_col2, action_spacer = st.columns([0.6, 0.6, 6])

    with action_col1:
        if st.button("My Profile"):
            my_profile_dialog()

    with action_col2:
        if st.button("Logout"):
            for key in ["token", "user_id", "username"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.success("로그아웃 완료!")
            st.rerun()

else:
    st.markdown("## 🔐 로그인")

    username = st.text_input("👤 ID", key="login_username")
    password = st.text_input("🔑 Password", type="password", key="login_password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("로그인", use_container_width=True, type="primary"):
            if not username or not password:
                st.error("아이디와 비밀번호를 모두 입력하세요.")
            else:
                login_url = f"{API_URL}/auth/login"
                login_data = {"username": username, "password": password}

                try:
                    response = requests.post(login_url, data=login_data)

                    if response.status_code == 200:
                        token_data = response.json()
                        st.session_state.token = token_data.get("access_token")

                        headers = {"Authorization": f"Bearer {st.session_state.token}"}
                        me_response = requests.get(f"{API_URL}/auth/me", headers=headers)

                        if me_response.status_code == 200:
                            user_info = me_response.json()
                            st.session_state.user_id = user_info.get("user_id")
                            st.session_state.username = user_info.get("username")
                            st.success("✅ 로그인 성공!")
                            st.rerun()
                        else:
                            st.error("로그인 후 사용자 정보 조회 실패")
                    else:
                        try:
                            detail = response.json().get("detail", "로그인 실패")
                        except Exception:
                            detail = response.text
                        st.error(f"❌ 로그인 실패: {detail}")

                except Exception as e:
                    st.error(f"서버 오류: {str(e)}")

    with col2:
        if st.button("회원가입", use_container_width=True):
            register_dialog()