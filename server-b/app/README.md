# docker compose build 
docker compose up --build

# server-b init 

cd server-b
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt

uvicorn app.main:app --reload --port 8000

2. **Service B** – Coordinate storage and retrieval.
    HTTP `GET` request to **Service A** for new IP
    HTTP `GET` request to **USER** for saved IP
    HTTP `POST` request to **Redis** to save IP

# gets fro server a 
[
  { "ip": "2.2.2.2", "coordinates": { "latitude": 40.22228, "longitude": -74.2222 } },
  { "ip": "2.2.2.2", "coordinates": { "latitude": 40.22228, "longitude": -74.2222 } }
]

#### Service B – Coordinates Storage (`service-b/`)

```text
service-b/
└── app/
    ├── main.py
    ├── routes.py
    ├── storage.py
    ├── Dockerfile
    └── schemas.py
```

Responsibilities per file:

- `main.py`  
  - Creates the FastAPI application and wires routes.
- `routes.py`  
  - Endpoints for:
    - Receiving coordinates.
    - Retrieving stored data.
- `storage.py`  
  - Work with Redis:
    - Connection.
    - Writing.
    - Reading.
- `schemas.py`  
  - Pydantic data models.
- `Dockerfile`  
  - Container definition for Service B.






for runing tha app local and redis in container
##  Build & start Redis container
```bash
docker build -f Dockerfile.redis -t redis-local .
```
- Run the container:
```bash
docker run -d \
  --name redis \
  -p 6379:6379 \
  redis-local
```
- Redis is now running on:
    localhost:6379

## Verify Redis is running

```bash
docker ps
```
Optional test:
```bash
docker exec -it redis redis-cli ping
```

## 3️⃣ Connect FastAPI (Python) to Redis

### Python connection (your code is already correct)

## 4️⃣ Test Redis from FastAPI

```python
@router.get("/redis-test")
def redis_test():
    redis_client.set("ping", "pong")
    return {"value": redis_client.get("ping")}
```

Visit:

```
GET /health/redis-test
```

# local redis container cli build & communication
##  Build & start Redis container
```bash
docker build -f Dockerfile.redis -t redis-local .
```
- Run the container:
```bash
docker run -d \
  --name redis \
  -p 6379:6379 \
  redis-local
```
- Redis is now running on:
    localhost:6379

## Verify Redis is running

```bash
docker ps
```
Optional test:
```bash
docker exec -it redis redis-cli ping
```

```bash
# open redis-cli inside the container
docker exec -it redis redis-cli
# inside redis-cli: 127.0.0.1:6379>
KEYS *
GET 1.1.1.1
EXIT
```