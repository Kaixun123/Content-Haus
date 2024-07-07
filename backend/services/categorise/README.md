# Categorise function🚀

## 1. Prerequisites
### 1.1 .env file
Ensure that you have placed in app a .env file for the crawling
```
ms_token=<ms_token_value> # Get this from tiktok.com cookies after logging in
DATABASE_URL=<database_url> # E.g. "mysql+aiomysql://username:password@host/database"
GOOGLE_APPLICATION_CREDENTIALS=<your_google_credentials_json_file>
GCP_BUCKET=<your_gcp_bucket>
```
### 1.2 Install prerequisites
```
pip install requirements.txt
playwright install
```

## 2. Running the function
### 2.1 Running without docker
```
cd app/
uvicorn main:app
```
### 2.2 Running with docker
```
docker build -t tiktok-scraper .
docker run -p 8000:8000 tiktok-scraper
```

## 3. Test/access the API docs
Access the application documentation generated at:
```
http://127.0.0.1:8000/docs#/
```
