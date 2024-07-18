# 📝 Todos API


Welcome to the **Todos API** written in FastAPI ! 🎉

## 🚀 Description

The **Todos API** is a RESTful web service built with FastAPI that allows users to manage a list of tasks efficiently. It provides endpoints for creating, reading, updating, and deleting tasks, making it easy to integrate into various applications for task management. The API includes user authentication and an admin role for enhanced task and user management capabilities.

## 📦 Features

- 🆕 **Create Tasks**: Add new tasks to your list.
- 🔍 **Read Tasks**: Retrieve a list of all tasks or a specific task by ID.
- ✏️ **Update Tasks**: Modify the details of an existing task.
- ❌ **Delete Tasks**: Remove tasks from your list.
- 🔐 **Authentication**: Secure endpoints with JWT-based authentication.
- 👤 **Admin Role**: Assign admin privileges to users for additional capabilities.


## 🛠 Installation

To get started with the **Todos API**, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/HosseinTahami/Todos-API.git
    cd Todos-API
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run database migrations**:
    ```bash
    alembic upgrade head
    ```

5. **Start the server**:
    ```bash
    uvicorn main:app --reload
    ```

6. **Access the API**: The API will be running at `http://localhost:8000`.

## 🔑 Authorization

The API uses JSON Web Tokens (JWT) for authentication. To access protected endpoints, you need to:

1. **Register a new user**:
    ```bash
    curl -X POST http://localhost:8000/users/register -H "Content-Type: application/json" -d '{"username": "your_username", "password": "your_password"}'
    ```

2. **Authenticate and get a token**:
    ```bash
    curl -X POST http://localhost:8000/token -H "Content-Type: application/x-www-form-urlencoded" -d 'username=your_username&password=your_password'
    ```

   The response will include an `access_token` you can use for authorized requests.

3. **Use the token to access protected endpoints**:
    ```bash
    curl http://localhost:8000/todos -H "Authorization: Bearer your_access_token"
    ```

4. **Admin Role**: Users with the admin role have additional privileges. Admins can manage all users and tasks, providing them the ability to oversee the entire application.

## 🧑‍💻 Usage

Here's an example of how to use the Todos API:

- **Create a new task**:
    ```bash
    curl -X POST http://localhost:8000/todos -H "Content-Type: application/json" -H "Authorization: Bearer your_access_token" -d '{"title": "New Task", "completed": false}'
    ```

- **Get all tasks**:
    ```bash
    curl http://localhost:8000/todos -H "Authorization: Bearer your_access_token"
    ```

- **Update a task**:
    ```bash
    curl -X PUT http://localhost:8000/todos/1 -H "Content-Type: application/json" -H "Authorization: Bearer your_access_token" -d '{"title": "Updated Task", "completed": true}'
    ```

- **Delete a task**:
    ```bash
    curl -X DELETE http://localhost:8000/todos/1 -H "Authorization: Bearer your_access_token"
    ```

## 🧪 Testing

To run tests, use `pytest`:

1. **Ensure all dependencies are installed**:
    ```bash
    pip install pytest
    ```

2. **Run the tests**:
    ```bash
    pytest
    ```

Tests are located in the `tests` directory and cover all API endpoints, ensuring reliable and correct functionality.

## 🤝 Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature (`git checkout -b feature-name`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push your changes to the branch (`git push origin feature-name`).
5. Create a pull request.

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 📞 Contact

For questions or support, please contact [Hossein Tahami](mailto:your-email@example.com).

---

Enjoy using the Todos API! 🌟
