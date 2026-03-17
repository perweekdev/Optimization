import streamlit as st
import onnxruntime as ort
import numpy as np
import os
import requests

MODEL_URL = "https://github.com/onnx/models/raw/main/validated/vision/classification/mnist/model/mnist-8.onnx"
MODEL_PATH = "models/mnist-8.onnx"

@st.cache_resource
def load_model():
    """모델 자동 다운로드 및 캐싱 로딩"""
    if not os.path.exists(MODEL_PATH):
        st.info("🔄 MNIST 모델 다운로드 중...")
        os.makedirs("models", exist_ok=True)
        response = requests.get(MODEL_URL)
        with open(MODEL_PATH, "wb") as f:
            f.write(response.content)
        st.success("✅ 모델 다운로드 완료!")
    
    session = ort.InferenceSession(MODEL_PATH)
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    return session, input_name, output_name

def softmax(x):
    """소프트맥스 함수"""
    e_x = np.exp(x - np.max(x, axis=1, keepdims=True))
    return e_x / e_x.sum(axis=1, keepdims=True)

def predict(session, input_name, output_name, input_tensor):
    """추론 수행"""
    logits = session.run([output_name], {input_name: input_tensor})[0]
    probs = softmax(logits)[0]
    pred_label = int(np.argmax(probs))
    return pred_label, probs