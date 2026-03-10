import argparse
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import Ridge  # v2: LinearRegression → Ridge
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score  # v2: 교차검증 추가
from sklearn.metrics import mean_squared_error
import joblib
import os
import numpy as np
import shutil
import warnings
warnings.filterwarnings('ignore')

def main(args):
    # 데이터 로드
    train = pd.read_csv(args.train)
    test = pd.read_csv(args.test)
    
    print("Train shape:", train.shape)
    print("EDA 요약: 이상치 0%, Previous Scores r=0.91 강한 선형성")
    
    # 특징량 정의 (EDA 기반)
    num_cols = ["Hours Studied", "Previous Scores", "Sleep Hours", "Sample Question Papers Practiced"]
    cat_cols = ["Extracurricular Activities"]  # Yes/No → OneHot (중앙값 71 vs 69)
    
    # 전처리 파이프라인 (전략 1~4 반영)
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), num_cols),      # 숫자형 스케일링
            ("cat", OneHotEncoder(handle_unknown="ignore", drop='first'), cat_cols),  # 범주형
        ],
        remainder='passthrough'  # 자동화
    )
    
    # 모델 파이프라인 (Ridge)
    model = Pipeline([
        ("preprocessor", preprocessor),  # ColumnTransformer
        ("regressor", Ridge(alpha=1.0, random_state=42))  # Ridge(과적합 방지)
    ])
    
    # 입력/타겟 분리
    X_train = train[num_cols + cat_cols]
    y_train = train["Performance Index"]
    
    # 교차검증 RMSE
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='neg_root_mean_squared_error')
    cv_rmse = -cv_scores.mean()
    print(f"5-Fold CV RMSE: {cv_rmse:.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    # 모델 학습
    model.fit(X_train, y_train)
    
    # Train RMSE (기존 + CV 비교용)
    y_pred_train = model.predict(X_train)
    train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
    print(f"Train RMSE: {train_rmse:.4f}")
    print(f"개선 효과: CV 대비 {train_rmse - cv_rmse:.4f} (낮을수록 좋음)")
    
    # 산출물 저장
    os.makedirs(args.outdir, exist_ok=True)
    joblib.dump(model, os.path.join(args.outdir, "model.pkl"))
    
    # test.csv 복사
    shutil.copy(args.test, os.path.join(args.outdir, "mission15_test.csv"))
    
    # 모델 정보 저장(재사용성)
    model_info = {
        'num_features': len(num_cols),
        'cat_features': len(cat_cols),
        'cv_rmse': float(cv_rmse),
        'train_rmse': float(train_rmse),
        'preprocessing': 'ColumnTransformer(StandardScaler + OneHotEncoder)'
    }
    import json
    with open(os.path.join(args.outdir, "model_info.json"), 'w') as f:
        json.dump(model_info, f, indent=2)
    
    print(f"✅ v2 모델 저장 완료: {args.outdir}")
    print("EDA 기반 개선사항:")
    print("- Ridge 회귀 (과적합 방지)")
    print("- 5-Fold 교차검증")
    print("- ColumnTransformer 자동화")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="학생 성적 예측 v2 (EDA 기반 개선)")
    parser.add_argument("--train", required=True, help="Train CSV path")
    parser.add_argument("--test", required=True, help="Test CSV path")
    parser.add_argument("--outdir", required=True, help="Output directory")
    args = parser.parse_args()
    main(args)