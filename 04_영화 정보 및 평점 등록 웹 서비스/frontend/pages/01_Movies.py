"""
01_Movies.py - 영화 목록 + 리뷰 기능
포스터 크기 통일 + 작은 리뷰작성 버튼 + 리뷰작성 모달
"""

import streamlit as st
import requests

# API URL
API_URL = "http://localhost:8000"

# 스타일
st.markdown(
    """
    <style>
    .movie-card-title {
        font-size: 0.95rem;
        font-weight: 700;
        line-height: 1.35;
        min-height: 2.6em;
        max-height: 2.6em;
        overflow: hidden;
        margin-bottom: 8px;
    }

    .movie-meta {
        font-size: 0.78rem;
        color: inherit;
        margin-top: 8px;
        margin-bottom: 8px;
    }

    .movie-poster-wrap {
        width: 180px;
        height: 270px;
        overflow: hidden;
        border-radius: 10px;
        margin-bottom: 8px;
    }

    .movie-poster-wrap img {
        width: 180px;
        height: 270px;
        object-fit: cover;
        display: block;
        border-radius: 10px;
    }

    .movie-bottom-gap {
        height: 20px;
    }

    div[data-testid="stForm"] {
        border: none !important;
        padding: 0 !important;
        background: transparent !important;
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

# ===== 최근 리뷰 모달 =====
@st.dialog("🔥 최근 리뷰 (최대 10개)", width="large")
def recent_reviews_dialog():
    st.markdown("### 최근 등록된 리뷰")

    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    response = requests.get(f"{API_URL}/reviews/latest", headers=headers)

    if response.status_code == 200:
        reviews = response.json()
        if reviews:
            for review in reviews:
                preview = review["content"][:60] + "..." if len(review["content"]) > 60 else review["content"]
                with st.expander(f"🎥 {review.get('movie_title', '미상')} - {preview}"):
                    st.markdown(f"**{review['content']}**")
                    st.caption(f"👤 {review.get('username', '알수없음')} | 📅 {review['created_at'][:10]}")

                    if review.get("user_id") == st.session_state.user_id:
                        if st.button("🗑️ 삭제", key=f"modal_delete_{review['id']}"):
                            delete_response = requests.delete(
                                f"{API_URL}/reviews/{review['id']}",
                                headers=headers
                            )
                            if delete_response.status_code == 200:
                                st.success("✅ 삭제 완료!")
                                st.rerun()
                            else:
                                st.error("❌ 삭제 실패")
        else:
            st.info("아직 리뷰가 없습니다.")
    else:
        st.error(f"리뷰 로드 실패: {response.status_code}")

    if st.button("닫기", use_container_width=True, key="close_recent_reviews_dialog"):
        st.rerun()


# ===== 리뷰 작성 모달 =====
@st.dialog("📝 리뷰 작성", width="large")
def write_review_dialog(movie_id: int, movie_title: str):
    st.markdown(f"### {movie_title}")
    st.caption("이 영화에 대한 리뷰를 작성하세요.")

    content = st.text_area(
        "리뷰 내용",
        placeholder="리뷰를 작성해주세요",
        height=180
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("취소", use_container_width=True, key=f"cancel_review_{movie_id}"):
            st.rerun()

    with col2:
        if st.button("리뷰 작성", use_container_width=True, key=f"submit_review_{movie_id}", type="primary"):
            if not content.strip():
                st.warning("리뷰 내용을 입력하세요.")
            else:
                headers = {"Authorization": f"Bearer {st.session_state.token}"}
                review_data = {
                    "movie_id": movie_id,
                    "content": content
                }
                response = requests.post(
                    f"{API_URL}/reviews/",
                    json=review_data,
                    headers=headers
                )
                if response.status_code == 200:
                    st.success("✅ 리뷰 작성 완료!")
                    st.rerun()
                else:
                    try:
                        detail = response.json().get("detail", "Unknown error")
                    except Exception:
                        detail = response.text
                    st.error(f"리뷰 작성 실패: {detail}")


# ===== 메인 페이지 =====
st.header("📺 인기 영화")
st.markdown("---")

if not st.session_state.get("token"):
    st.warning("⚠️ 로그인 후 리뷰 기능을 사용하세요.")
    st.stop()

headers = {"Authorization": f"Bearer {st.session_state.token}"}

# 상단 버튼
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("영화 초기화 🔄", use_container_width=True):
        response = requests.post(f"{API_URL}/movies/initialize", headers=headers)
        if response.status_code == 200:
            st.success("✅ 영화 초기화 완료!")
            st.rerun()
        else:
            st.error(f"❌ 초기화 실패: {response.status_code}")

with col2:
    st.empty()

with col3:
    if st.button("최근 리뷰 👀", use_container_width=True):
        recent_reviews_dialog()

# 영화 목록
movies_response = requests.get(f"{API_URL}/movies/", headers=headers)
if movies_response.status_code != 200:
    st.error(f"영화 목록 로드 실패: {movies_response.status_code}")
    st.stop()

movies = movies_response.json()
if not movies:
    st.info("아직 영화가 없습니다. '영화 초기화' 버튼을 클릭하세요.")
    st.stop()

# 영화 그리드 (4열)
for i, movie in enumerate(movies):
    if i % 4 == 0:
        cols = st.columns(4)

    col_idx = i % 4
    with cols[col_idx]:
        title_short = movie["title"]
        if len(title_short) > 20:
            title_short = title_short[:20] + "..."

        st.markdown(
            f'<div class="movie-card-title">{title_short}</div>',
            unsafe_allow_html=True
        )

        if movie["poster_url"]:
            st.markdown(
                f"""
                <div class="movie-poster-wrap">
                    <img src="{movie["poster_url"]}" alt="{movie["title"]}">
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.info("포스터 없음")

        st.markdown(
            f'<div class="movie-meta">출시: {movie["release_date"] or "미정"}</div>',
            unsafe_allow_html=True
        )

        # 출시일 아래에 작은 버튼 배치
        btn_left, btn_mid, btn_right = st.columns([1.8, 1.2, 1.0])
        with btn_left:
            if st.button("리뷰 작성", key=f"open_review_dialog_{movie['id']}"):
                write_review_dialog(movie["id"], movie["title"])

        st.markdown("<div class='movie-bottom-gap'></div>", unsafe_allow_html=True)