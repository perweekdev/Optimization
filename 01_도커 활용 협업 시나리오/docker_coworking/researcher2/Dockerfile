FROM python:3.10-slim

WORKDIR /work

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /artifacts

EXPOSE 8888

# --allow-root 추가 (root 사용자 허용)
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--ServerApp.token=''", "--allow-root"]
