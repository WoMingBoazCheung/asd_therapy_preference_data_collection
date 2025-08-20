# ASD Therapy Preference Data Collection

This project is a web application for collecting data on preferences between different ASD (Autism Spectrum Disorder) therapy sessions. The application presents users with pairs of therapy sessions and records their preferences.

## Project Structure

The project is divided into two main parts:

-   **Backend**: A Django application that manages the therapy session data and user preferences.
-   **Frontend**: A React application that provides the user interface for comparing and selecting therapy sessions.

## Features

-   **Backend (Django)**:
    -   Serves pairs of therapy sessions for comparison.
    -   Stores user preferences in a database.
    -   Provides API endpoints for the frontend to fetch session data and submit preferences.
    -   Includes management commands to populate the database with session data and export the collected preference data to a CSV file.
-   **Frontend (React)**:
    -   Displays pairs of therapy sessions to the user.
    -   Allows users to select their preferred session.
    -   Communicates with the backend to fetch session pairs and submit preferences.

## Getting Started

### Prerequisites

-   Python 3.x
-   Node.js and npm

### Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

4.  **Populate the database with therapy session data:**
    ```bash
    python manage.py populate_sessions
    ```

5.  **Run the Django development server:**
    ```bash
    python manage.py runserver
    ```

### Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install Node.js dependencies:**
    ```bash
    npm install
    ```

3.  **Run the React development server:**
    ```bash
    npm run dev
    ```

## Usage

1.  Once both the backend and frontend servers are running, open your web browser and navigate to the address provided by the React development server (usually `http://localhost:5173`).
2.  You will be presented with two therapy sessions. Click on the session you prefer.
3.  Your preference will be recorded, and a new pair of sessions will be displayed.

## API Endpoints

-   `GET /get_session_pair/`: Fetches a random pair of therapy sessions from the database.
-   `POST /add_comparison/`: Adds a new comparison record to the database.

    **Request Body:**
    ```json
    {
        "session_id_1": "session_name_1",
        "session_id_2": "session_name_2",
        "preferred": 1
    }
    ```
    -   `preferred`: `1` if `session_id_1` is preferred, `2` if `session_id_2` is preferred.

## Management Commands

-   `python manage.py populate_sessions`: Populates the database with sample therapy session data.
-   `python manage.py export_comparisons`: Exports the session comparison data to a CSV file located in `backend/csv_output/`.
