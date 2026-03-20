## 프로젝트 실행 워크플로우(Alembic 포함)


### 로컬 실행 방법

#### 1. TMDB API 키 발급
- https://www.themoviedb.org/settings/api → API 키(v3 auth) 복사
- backend/.env.example → TMDB_API_KEY 설정

#### 2. 백엔드 + DB 실행 (Docker Compose)
```bash
cd backend
cp .env.example .env
docker compose up --build -d
```

</br>

#### 3. Alembic 마이그레이션 실행 (최초 1회)
```bash
# 초기 마이그레이션 파일 생성
docker compose run api alembic revision --autogenerate -m "initial migration"

# 마이그레이션 적용
docker compose run api alembic upgrade head
```

</br>

#### 4. TMDB 영화 초기화 (최초 1회, FastAPI Docs에서 클릭)
```
브라우저에서 http://localhost:8000/docs 열기
→ POST /movies/initialize 클릭 → Execute 버튼
→ 최신 인기 영화 20개 자동 DB 저장 완료!
```

#### FastAPI Docs에서 호출하는 방법

1. [**http://localhost:8000/docs**](http://localhost:8000/docs) 접속  
2. **POST /movies/initialize** 엔드포인트 찾기  
3. **Try it out** 버튼 클릭  
4. **Execute** 버튼 클릭  
5. **Response body**에 `{"message": "20 movies initialized from TMDB!"}` 확인  
*이미 실행했다면 중복 저장 방지 로직이 있으므로 안전함.

</br>

#### 5. 프론트엔드 실행 (별도 터미널)
```bash
cd frontend
cp .env.example .env
pip install -r requirements.txt
streamlit run app.py
```

</br>

#### 6. 테스트
- FastAPI Docs: http://localhost:8000/docs
- Streamlit: http://localhost:8501

**(참고) 개발 중 테이블 변경 시**
```
# 변경사항 감지해서 마이그레이션 파일 새로 생성
docker compose run api alembic revision --autogenerate -m "add rating column"

# 적용
docker compose run api alembic upgrade head
```

</br>

#### 환경변수 예시(.env.example)

`backend/.env.example`:
```
DATABASE_URL=postgresql://postgres:password123@db:5432/movie_db
SECRET_KEY=your-secret-key-here
TMDB_API_KEY=your_tmdb_api_key_here  # https://www.themoviedb.org/settings/api 에서 발급
```
</br>

`frontend/.env.example`:
```
API_URL=http://localhost:8000
```