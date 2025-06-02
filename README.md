# 50 State Test Application

A web application for administering and tracking 50 state tests. Built with Python (Flask) and MongoDB.

## Features

- Administer 50 state tests
- Track student progress
- Store test results
- Manage homeroom teachers and student codes

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   - Create a `.env` file
   - Add your MongoDB connection string:
     ```
     MONGODB_URI=your_mongodb_connection_string
     ```

## Development

Run the server locally:
```bash
python server.py
```

The server will start at `http://localhost:5000`

## Deployment

This application is configured for deployment on Vercel. Simply connect your GitHub repository to Vercel for automatic deployments.

## Environment Variables

- `MONGODB_URI`: MongoDB connection string
- `PORT`: Server port (default: 5000) 