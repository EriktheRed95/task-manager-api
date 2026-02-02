# Python Task Manager API

A robust REST API built with **FastAPI** and **SQLAlchemy**. This project demonstrates backend engineering skills including CRUD operations, data validation, and database persistence.

## 🚀 Features
* **Create Tasks:** Add new to-do items to the database.
* **Read & Search:** View all tasks or filter them by title.
* **Update:** Mark tasks as completed or edit their details.
* **Delete:** Remove tasks permanently.
* **Persistance:** Uses SQLite to save data so it survives server restarts.
* **Documentation:** Automatic interactive API docs via Swagger UI.

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Framework:** FastAPI
* **Database:** SQLite & SQLAlchemy
* **Validation:** Pydantic V2

## ⚙️ How to Run Locally

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/task-manager-api.git](https://github.com/YOUR_USERNAME/task-manager-api.git)
    cd task-manager-api
    ```

2.  **Set up the Virtual Environment**
    ```bash
    python -m venv venv
    
    # Windows:
    .\venv\Scripts\activate
    
    # Mac/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    cd backend
    pip install -r requirements.txt
    ```

4.  **Run the Server**
    ```bash
    uvicorn main:app --reload
    ```

5.  **View the API**
    Open your browser to: `http://127.0.0.1:8000/docs`