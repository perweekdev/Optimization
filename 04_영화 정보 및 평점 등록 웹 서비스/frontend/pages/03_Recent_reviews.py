"""
03_Recent_Reviews.py - 최근 리뷰 목록
최근 10개 리뷰 조회 + 본인 리뷰 삭제
"""

import streamlit as st
import requests


# API URL
API_URL = "http://localhost:8000"


# 스타일
st.markdown(
    """
    <style>
    .recent-review-card {
        padding: 14px 16px;
        border: 1px solid rgba(128, 128, 128, 0.25);
        border-radius: 12px;
        margin-bottom: 12px;
        background-color: rgba(255, 255, 255, 0.02);
    }

    .recent-movie-title {
        font-size: 1rem;
        font-weight: 700;
        margin-bottom: 6px;
    }

    .recent-review-meta {
        font-size: 0.8rem;
        color: #888;
        margin-bottom: 10px;
    }

    .recent-review-content {
        font-size: 0.95rem;
        line-height: 1.5;
        white-space: pre-wrap;
        word-break: break-word;
    }

    div[data-testid="stButton"] > button {
        border-radius: 8px !important;
        font-size: 0.5rem !important;
        padding: 0.15rem 0.45rem !important;
        line-height: 1.1 !important;
        min-height: 20px !important;
        white-space: nowrap !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# 페이지 제목
st.header("🔥 Recent Reviews")
st.markdown("---")


# 로그인 체크
if not st.session_state.get("token"):
    st.warning("⚠️ 로그인 후 최근 리뷰를 확인할 수 있습니다.")
    st.stop()


headers = {"Authorization": f"Bearer {st.session_state.token}"}


# 상단 버튼
top_btn1, top_spacer = st.columns([1, 6])

with top_btn1:
    if st.button("Reload 🔄"):
        st.rerun()


# 최근 리뷰 조회
response = requests.get(f"{API_URL}/reviews/latest", headers=headers)

if response.status_code != 200:
    st.error(f"최근 리뷰 조회 실패: {response.status_code}")
    st.stop()


reviews = response.json()

if not reviews:
    st.info("아직 등록된 최근 리뷰가 없습니다.")
    st.stop()


st.caption(f"최근 리뷰 {len(reviews)}개를 표시합니다.")


# 리뷰 목록
for review in reviews:
    col1, col2 = st.columns([6, 1])

    with col1:
        st.markdown(
            f"""
            <div class="recent-review-card">
                <div class="recent-movie-title">{review.get("movie_title", "미상")}</div>
                <div class="recent-review-content">{review["content"]}</div>
                <div class="recent-review-meta">
                    작성자: {review.get("username", "알수없음")} | 작성일: {review["created_at"][:10]}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        if review.get("user_id") == st.session_state.user_id:
            if st.button("삭제", key=f"delete_recent_review_{review['id']}"):
                delete_response = requests.delete(
                    f"{API_URL}/reviews/{review['id']}",
                    headers=headers
                )

                if delete_response.status_code == 200:
                    st.success("✅ 리뷰가 삭제되었습니다.")
                    st.rerun()
                else:
                    try:
                        detail = delete_response.json().get("detail", "Unknown error")
                    except Exception:
                        detail = delete_response.text
                    st.error(f"❌ 삭제 실패: {detail}")