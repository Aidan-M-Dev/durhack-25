cd frontend

# Load environment variables from .env file
export $(grep -v '^#' ./.env | xargs)

npm install
npm run dev