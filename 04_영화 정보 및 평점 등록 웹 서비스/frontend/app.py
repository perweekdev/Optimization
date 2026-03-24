"""
Movie Review Service - Main App
로그인 + 회원가입 모달 (올바른 순서)
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

# ===== 회원가입 모달 함수 (최상단으로 이동) =====
@st.dialog("📝 회원가입", width="medium")
def register_dialog():
    """회원가입 모달"""
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
                    st.error(f"회원가입 실패: {response.json().get('detail', 'Unknown')}")
            except Exception as e:
                st.error(f"서버 오류: {str(e)}")
    
    if st.button("❌ 취소", use_container_width=True):
        st.rerun()

# ===== 메인 앱 =====
st.title("🎬 Movie Review Service")
st.markdown("---")

# 로그인 상태 표시
if st.session_state.token:
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.success(f"👋 환영합니다, **{st.session_state.username}**님!")
    with col2:
        st.info(f"USER_ID: {st.session_state.user_id}")
    with col3:
        if st.button("🚪 로그아웃", use_container_width=True):
            for key in ["token", "user_id", "username"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.success("로그아웃 완료!")
            st.rerun()
    
    st.markdown("---")
    st.markdown("""
    ### 🎯 사용 가능한 메뉴
    사이드바에서 아래 페이지들을 이용해보세요:
    - **Movies**: 인기 영화 + 리뷰 작성
    - **My Reviews**: 내 리뷰 관리
    - **Recent Reviews**: 최근 리뷰 확인
    """)

else:
    # 로그인 폼
    st.markdown("## 🔐 로그인")
    
    username = st.text_input("👤 ID", key="login_username")
    password = st.text_input("🔑 Password", type="password", key="login_password")
    
    # 버튼들
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
                        st.session_state.token = token_data["access_token"]
                        
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
                        st.error("❌ 로그인 실패!")
                except Exception as e:
                    st.error(f"서버 오류: {str(e)}")
    
    with col2:
        if st.button("회원가입", use_container_width=True):
            register_dialog()  # 이제 함수가 위에 정의되어 있음