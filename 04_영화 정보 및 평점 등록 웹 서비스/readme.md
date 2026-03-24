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
`.env` 파일에 TMDB API KEY 는 직접 작성해야합니다.

#### docker compose 삭제 및 다시 빌드할 때
```
docker compose down --volumes --rmi all
docker compose up --build -d

```

</br>

#### 3. Alembic 마이그레이션 실행 (최초 1회)
```bash
# 로그 확인
docker compose logs -f api

# 초기 마이그레이션 파일 생성
docker compose run api alembic revision --autogenerate -m "initial create tables"

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
DATABASE_URL=postgresql+asyncpg://postgres:password123@db:5432/movie_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
TMDB_API_KEY=your_tmdb_api_key_here  # https://www.themoviedb.org/settings/api 에서 발급
```
`SECRET_KEY` 자리는 **JWT 서명용 비밀키**를 넣는 곳입니다.(충분히 긴 랜덤 문자열)

가장 간단한 방법은 터미널에서 아래 명령으로 생성하는 것입니다.(약 64자리 안전한 16진수 문자열 생성)

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

생성된 랜덤 문자열을 `.env`에 적용합니다.

```env
# 예시(해당 문자열을 .env 파일에 삽입)
SECRET_KEY=4d8d7d2c6d7e2f1e5e9d0a0d3b0d4c2f8a9b7c6d5e4f3a2b1c0d9e8f7a6b5c4d
```

\*보고서나 깃허브에 실제 키를 그대로 올리면 안 됩니다.

</br>

`frontend/.env.example`:
```
API_URL=http://localhost:8000
```

</br>

---

</br>

### Swagger API 테스트 순서
백엔드 실행, DB 연결, Alembic 마이그레이션, TMDB 영화 초기화 준비가 끝났다면 아래 순서로 테스트합니다. `POST /auth/login`은 보통 Swagger에서 `application/x-www-form-urlencoded` 형식으로 입력하고, 인증이 필요한 API는 `Authorize`에 Bearer 토큰을 넣어 호출합니다.
#### 1. Swagger 접속
- 브라우저에서 `http://localhost:8000/docs` 접속
#### 2. 회원가입
- `POST /auth/register`
- 예시 요청:
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}
```
#### 3. 로그인
- `POST /auth/login`
- 입력값 예시:
```text
username: testuser
password: password123
```
- 응답으로 받은 `access_token` 값을 복사
#### 4. 인증 적용
- 우측 상단 `Authorize` 클릭
- 아래 형식으로 입력 후 인증(또는 위에서 가입한 계정으로 로그인)
```text
Bearer {access_token}
```
- 예시:
```text
Bearer eyJhbGciOiJIUzI1NiIs...
```
#### 5. 영화 초기화
- `POST /movies/initialize`
- Execute 클릭
- TMDB 인기 영화가 DB에 저장되면 성공
#### 6. 영화 목록 조회
- `GET /movies/`
- 저장된 영화 목록 확인
- 이후 리뷰 작성에 사용할 `movie_id` 확인
#### 7. 영화 상세 조회
- `GET /movies/{movie_id}`
- 예: `movie_id = 1`
#### 8. 리뷰 작성
- `POST /reviews/`
- 로그인 + Authorize 적용 후 호출
- 예시 요청:
```json
{
  "movie_id": 1,
  "content": "스토리와 연출이 인상적이었습니다."
}
```
#### 9. 최근 리뷰 조회
- `GET /reviews/latest`
- 최근 등록된 리뷰 목록 확인
#### 10. 특정 영화 리뷰 조회
- `GET /reviews/movie/{movie_id}`
- 예: `movie_id = 1`

</br>

### 권장 테스트 순서 요약
1. `POST /auth/register`  
2. `POST /auth/login`  
3. `Authorize`에 `Bearer {access_token}` 입력  
4. `POST /movies/initialize`  
5. `GET /movies/`  
6. `GET /movies/{movie_id}`  
7. `POST /reviews/`  
8. `GET /reviews/latest`  
9. `GET /reviews/movie/{movie_id}`  

</br>

### 테스트용 예시 데이터
#### 회원가입
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}
```
#### 리뷰 작성
```json
{
  "movie_id": 1,
  "content": "정말 재미있게 봤습니다."
}
```

</br>

### 테스트 성공 기준
- 회원가입 성공
- 로그인 후 JWT 토큰 발급 성공
- Swagger Authorize 성공
- 영화 초기화 성공
- 영화 목록 조회 성공
- 리뷰 작성 성공
- 최근 리뷰 조회 성공