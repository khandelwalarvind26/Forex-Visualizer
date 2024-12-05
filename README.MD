
# Forex exchange visualizer

Web application that provides real-time Forex data visualization using dynamic line charts. It allows users to visualize the exchange rate trends between selected currencies over various periods.
Built Using **FastAPI, Selenium, SQLAlchemy, sqlite, chart.js**.

---

## Requirements

- **Python 3.8** or higher
- **pip** package manager

---

## Setup Instructions

Follow these steps to set up and run the project locally:

### 1. Clone the Repository
Clone the project repository to your local machine:

```bash
git clone https://github.com/khandelwalarvind26/Vance.git
```

Navigate into the project folder:

```bash
cd Vance
```

### 2. Local environment setup
Install aiocron in local environment:

```bash
pip install aiocron
```

### 3. Set Up a Virtual Environment
Create a new virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

- On **Windows**:
  ```bash
  .\env\Scripts\ctivate
  ```

- On **macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

### 4. Install Dependencies
Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Create a `.env` file in the root of the project (if it doesn’t already exist) and add your database URL:

For in-memory DB
```bash
DATABASE_URL="sqlite+aiosqlite:///:memory:"
```

For persisitent DB
```bash
DATABASE_URL="sqlite+aiosqlite:///./db_name.db"
```

Add country pairs on which the indexes are to be fetched
```bash
COUNTRY_COMBINATIONS=[["GBP", "INR"],["AED","INR"]]
```

### 6. Start the Application
Start the FastAPI server:

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

---

## How to Use

1. After starting the server, access the API documentation at:

   [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

2. Use the interactive **Swagger UI** to explore and test the endpoints.

3. Frontend with the rendered chats available at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

### Additional Notes:
- Make sure you have `sqlite3` installed on your local machine.
- The server automatically reloads on code changes when running with the `--reload` option, useful during development.
