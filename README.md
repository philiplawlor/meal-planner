# Meal Planner

A meal planning application that allows users to plan their meals for the week. Meal ideas are fetched from MongoDB Atlas and displayed in a Flutter app.

## Tech Stack

- Backend: Python
- Database: MongoDB Atlas
- Frontend: Flutter
- Protocol: Model Context Protocol (MCP)

## Version

1.0.0

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Update MongoDB Atlas connection string in `.env`

3. Run the database setup:
   ```bash
   python database_setup.py
   ```

4. Start the MCP server:
   ```bash
   python server.py
   ```

## Features

- View meal ideas from MongoDB Atlas
- Plan meals for the week
- Save meal plans
- Rate and comment on meals
- Filter meals by cuisine, difficulty, and dietary preferences
