# Jokes Streamer - 3-Part Application

A simple demonstration app with gRPC backend, React frontend, and PostgreSQL database, deployable to Render.com.

## Architecture

- **Backend**: Python with gRPC + Flask HTTP API
- **Frontend**: React with auto-cycling joke display
- **Database**: PostgreSQL with sample jokes

## Features

- 🎭 Streams jokes from database
- 🔄 Auto-cycles through jokes every second
- 🚀 Easy deployment to Render.com
- 🐳 Docker-based backend
- 💾 PostgreSQL database

## Local Development

### Prerequisites

- Python 3.11+
- Node.js 16+
- PostgreSQL (or use a cloud instance)

### Backend Setup

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Generate gRPC code from proto files
python -m grpc_tools.protoc \
    -I./proto \
    --python_out=./proto \
    --grpc_python_out=./proto \
    ./proto/jokes.proto

# Set database URL (use your local or cloud PostgreSQL)
export DATABASE_URL="postgresql://user:password@localhost/jokes_db"

# Run the server
python server.py
```

The backend will start on:
- HTTP API: `http://localhost:8000`
- gRPC: `localhost:50051`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set backend URL
export REACT_APP_BACKEND_URL="http://localhost:8000"

# Start development server
npm start
```

The frontend will open at `http://localhost:3000`

## Deployment to Render.com

### Option 1: Using render.yaml (Blueprint)

1. Push this repository to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click "New" → "Blueprint"
4. Connect your GitHub repository
5. Render will automatically detect `render.yaml` and create all services

### Option 2: Manual Setup

#### 1. Create PostgreSQL Database

1. Go to Render Dashboard
2. Click "New" → "PostgreSQL"
3. Name: `jokes-database`
4. Database: `jokes_db`
5. User: `jokes_user`
6. Plan: Free
7. Click "Create Database"

#### 2. Deploy Backend

1. Click "New" → "Web Service"
2. Connect your repository
3. Settings:
   - **Name**: `jokes-backend`
   - **Environment**: Docker
   - **Dockerfile Path**: `./backend/Dockerfile`
   - **Plan**: Free
4. Add Environment Variables:
   - `DATABASE_URL`: (link to your PostgreSQL database)
   - `PORT`: `10000` (Render sets this automatically)
5. Click "Create Web Service"

#### 3. Deploy Frontend

1. Click "New" → "Static Site"
2. Connect your repository
3. Settings:
   - **Name**: `jokes-frontend`
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `frontend/build`
4. Add Environment Variable:
   - `REACT_APP_BACKEND_URL`: Your backend URL (e.g., `https://jokes-backend.onrender.com`)
5. Click "Create Static Site"

## API Endpoints

### HTTP API

- `GET /api/jokes` - Get all jokes
- `GET /health` - Health check

### gRPC API

- `StreamJokes(StreamJokesRequest)` - Stream jokes one at a time

## Database Schema

```sql
CREATE TABLE jokes (
    id SERIAL PRIMARY KEY,
    setup TEXT NOT NULL,
    punchline TEXT NOT NULL
);
```

## Project Structure

```
TestRenderCom/
├── backend/
│   ├── proto/
│   │   └── jokes.proto          # gRPC service definition
│   ├── db.py                     # Database operations
│   ├── server.py                 # gRPC + HTTP server
│   ├── requirements.txt          # Python dependencies
│   ├── Dockerfile               # Container configuration
│   └── generate_proto.sh        # Proto code generation script
├── frontend/
│   ├── src/
│   │   ├── App.js               # Main React component
│   │   ├── App.css              # Styling
│   │   ├── index.js             # React entry point
│   │   └── index.css            # Global styles
│   ├── public/
│   │   └── index.html           # HTML template
│   └── package.json             # Node dependencies
└── render.yaml                  # Render.com blueprint
```

## Technologies Used

- **Backend**: Python, gRPC, Flask, psycopg2
- **Frontend**: React, Create React App
- **Database**: PostgreSQL
- **Deployment**: Render.com, Docker

## Notes

- The backend serves both gRPC and HTTP APIs for flexibility
- HTTP API is used by the frontend for simplicity (avoids Envoy proxy)
- gRPC streaming is available on port 50051 for native gRPC clients
- Database is auto-initialized with sample jokes on first run
- Free tier on Render.com may spin down after inactivity

## License

MIT
