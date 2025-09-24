#!/bin/bash

echo "Starting Quiz App Setup..."

echo ""
echo "1. Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "2. Installing Node.js dependencies..."
npm install

echo ""
echo "3. Generating Prisma client..."
npx prisma generate

echo ""
echo "4. Running database migrations..."
npx prisma migrate deploy

echo ""
echo "5. Seeding database with sample questions..."
python seed_database.py

echo ""
echo "6. Starting application with PM2..."
npm run dev

echo ""
echo "Quiz App is now running!"
echo "API: http://localhost:8000"
echo "Web App: http://localhost:8000"
echo ""
echo "To stop the application, run: npm run stop"
echo "To view logs, run: npm run logs"