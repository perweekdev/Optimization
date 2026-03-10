import argparse
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
import joblib
import os
import numpy as np
import shutil

def main(args):
    train = pd.read_csv(args.train)
    test = pd.read_csv(args.test)

    num_cols = ["Hours Studied", "Previous Scores", "Sleep Hours", "Sample Question Papers Practiced"]
    cat_cols = ["Extracurricular Activities"]

    preproc = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), num_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
        ]
    )

    model = Pipeline([
        ("preproc", preproc),
        ("reg", LinearRegression())
    ])

    X_train = train[num_cols + cat_cols]
    y_train = train["Performance Index"]

    model.fit(X_train, y_train)

    # 간단한 성능 확인 (train 기준)
    y_pred = model.predict(X_train)
    rmse = np.sqrt(mean_squared_error(y_train, y_pred))
    print("Train RMSE:", rmse)

    os.makedirs(args.outdir, exist_ok=True)
    joblib.dump(model, os.path.join(args.outdir, "model.pkl"))

    # test.csv도 outdir로 복사
    shutil.copy(args.test, os.path.join(args.outdir, "mission15_test.csv"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", required=True)
    parser.add_argument("--test", required=True)
    parser.add_argument("--outdir", required=True)
    args = parser.parse_args()
    main(args)