cd server-a
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt

you can run this localy 

# one terminal
cd server-a
uvicorn app.main:app --reload --port 8000

# seconed terminal
cd server-b
uvicorn app.main:app --reload --port 8080

# run container of redis

docker build -f Dockerfile.redis -t redis-local .

docker run -d --name redis -p 6379:6379 redis-local

## now all works 