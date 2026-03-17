import streamlit as st
from datetime import datetime
import pandas as pd
import numpy as np
import model_utils
import image_utils
import os

st.set_page_config(
    page_title="MNIST 손글씨 인식",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
:root { --punctuation-color: #000000; }
.stMarkdown h1, h2, h3, h4, h5, h6 { color: #000000 !important; }
.stText { color: #333333 !important; }
.stCaption { color: #666666 !important; }
</style>
""", unsafe_allow_html=True)

st.title("MNIST 손글씨 숫자 인식기")
st.markdown("---")

# 세션 상태 초기화
if 'drawing' not in st.session_state:
    st.session_state.drawing = None
if 'saved_images' not in st.session_state:
    st.session_state.saved_images = []
if 'canvas_reset_key' not in st.session_state:
    st.session_state.canvas_reset_key = 0

# 저장 폴더 생성
os.makedirs("saved_images/images", exist_ok=True)

# 모델 로딩
session, input_name, output_name = model_utils.load_model()

col1, col2 = st.columns(2)

# ===================== 왼쪽: 입력 + 예측 =====================
with col1:
    st.subheader("📝 숫자 그리기(0-9)")
    from streamlit_drawable_canvas import st_canvas

    canvas_key = f"canvas_v{st.session_state.canvas_reset_key}"
    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 0.3)",
        stroke_width=20,
        stroke_color="black",
        background_color="white",
        update_streamlit=True,
        height=280,
        width=280,
        drawing_mode="freedraw",
        key=canvas_key,
        point_display_radius=0
    )

    if canvas_result.image_data is not None:
        st.session_state.drawing = canvas_result.image_data

    if st.button("숫자 인식", use_container_width=True,
                 disabled=st.session_state.drawing is None,
                 type="primary"):
        with st.spinner("분석 중..."):
            input_tensor, viz_img = image_utils.preprocess(st.session_state.drawing)
            if input_tensor is not None:
                pred_label, probs = model_utils.predict(session, input_name, output_name, input_tensor)
                st.session_state.pred_label = pred_label
                st.session_state.probs = probs
                st.session_state.viz_img = viz_img
                st.success(f"✅ 인식된 숫자: {pred_label}")
            else:
                st.error("이미지 전처리에 실패했습니다.")

    if 'pred_label' in st.session_state:
        st.markdown("### 🎯 인식 결과")

        # 소수점 5자리 확률 테이블
        probs_5digit = [f"{p:.5f}" for p in st.session_state.probs]
        prob_df = pd.DataFrame({'숫자': range(10), '확률': probs_5digit})
        st.dataframe(prob_df.set_index('숫자'), use_container_width=True)

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("초기화", use_container_width=True):
                st.session_state.canvas_reset_key += 1
                for key in ['pred_label', 'probs', 'viz_img', 'drawing']:
                    st.session_state.pop(key, None)
                st.rerun()

        # 🔁 변경: “결과 저장(미리보기)” → 즉시 저장 버튼
        with col_btn2:
            if st.button("결과 저장", use_container_width=True):
                # 이미지 PNG 저장
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                img_path = f"saved_images/images/pred_{int(st.session_state.pred_label)}_{timestamp}.png"
                st.session_state.viz_img.save(img_path)

                # 전체 확률 기록
                all_probs = [f"{p:.5f}" for p in st.session_state.probs]
                record = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "predicted_label": int(st.session_state.pred_label),
                    "confidence": all_probs[st.session_state.pred_label],
                    "image_path": img_path,
                    **{f"prob_{i}": all_probs[i] for i in range(10)}
                }
                st.session_state.saved_images.append(record)

                # 로컬 CSV 즉시 업데이트
                csv_path = "saved_images/predictions.csv"
                df_all = pd.DataFrame(st.session_state.saved_images)
                df_all.to_csv(csv_path, index=False)

                st.success(f"✅ 인식 결과 저장 완료(saved_images)")

# ===================== 오른쪽: 전처리 + 저장소 =====================
with col2:
    st.subheader("🔍 전처리 결과")

    if st.session_state.drawing is not None:
        _, viz_img = image_utils.preprocess(st.session_state.drawing)
        st.image(viz_img, caption="28x28 입력 이미지", width=280)

    with st.expander(f"📊 저장 내역 ({len(st.session_state.saved_images)}건)", expanded=True):
        if st.session_state.saved_images:
            df_saved = pd.DataFrame(st.session_state.saved_images)

            # 데이터프레임 표시
            if st.session_state.get('view_mode', 'simple') == 'full':
                st.dataframe(df_saved, height=300, use_container_width=True)
            else:
                st.dataframe(
                    df_saved[['timestamp', 'predicted_label', 'confidence', 'image_path']],
                    height=250,
                    use_container_width=True
                )

            # 다운로드 버튼만 남김 (로컬 저장 버튼 삭제)
            csv_content = df_saved.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 CSV 다운로드",
                data=csv_content,
                file_name="predictions_full.csv",
                mime="text/csv",
                use_container_width=True
            )

            # 이미지 폴더 정보
            if os.path.exists("saved_images/images"):
                img_count = len(os.listdir('saved_images/images'))
                st.caption(f"저장된 이미지: saved_images/images/({img_count}개)")

        else:
            st.info("결과를 저장해보세요")

