#!/bin/bash

# Start Django backend on port 8000
cd django_mongo_project
python manage.py runserver localhost:8000 &
BACKEND_PID=$!
echo "✅ Django backend started on port 8000 (PID: $BACKEND_PID)"

# Wait for backend to start
sleep 3

# Start frontend on port 5000
cd ../frontend
npm run dev
