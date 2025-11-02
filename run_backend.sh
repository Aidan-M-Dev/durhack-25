cd backend

# Load environment variables from .env file
export $(grep -v '^#' ../.env | xargs)

pip install -r requirements.txt
python3 app.py