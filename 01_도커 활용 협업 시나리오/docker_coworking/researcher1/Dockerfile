FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY train.py .
COPY data/ /data/

RUN mkdir -p /artifacts

CMD ["python", "train.py", "--train", "/data/mission15_train.csv", "--test", "/data/mission15_test.csv", "--outdir", "/artifacts"]