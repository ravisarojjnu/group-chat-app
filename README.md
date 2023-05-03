# Flask Group Chat Application with SQLite and Swagger Documentation
------------------------------------------------------------------
Online Deployed: [https://ravisaroj.pythonanywhere.com/api/docs/#/](ravisaroj.pythonanywhere.com/api/docs/#/)
# group-chat-app
A simple application which provides web services to facilitate group chat and manage data.
- Admin APIs (only admin can add users)
<br>Manage Users (create user, edit user)
- Any User (normal user, admin user) –
<br> Authentication APIs (login, logout)
- Groups (Normal User) –
<br>Manage groups (create, delete, search and add members, etc). All users are visible to all users.
- Group Messages (Normal User)
<br>Send messages in group
<br>Likes message, etc

This is a Python Flask application that provides web services to facilitate group chat and manage data using SQLite database. The application is also documented using Swagger.

### Requirements

-   Python 3.6+
-   Flask
-   Flask-SQLAlchemy
-   Flask-Swagger-UI
-   SQLite3

### Installation

1.  Clone this repository
2.  Create a virtual environment and activate it
3.  Install the dependencies using `pip install -r requirements.txt`
4.  Start the server using `python app.py`

### Usage

1.  To view the Swagger documentation, go to `http://localhost:5000/api/docs/#/`
2. Use `POST /login`: Authenticate a user API to get the API-KEY, and API-KEY can be used in the header with X-API-Key. 
- In Swagger UI paste the API key in Autherize menu.
3.  Use the following endpoints to manage users:
    -   `POST /users`: Create a new user (admin only)
    -   `PUT /users/{user_id}`: Update a user's information (admin only)
    -   `DELETE /users/{user_id}`: Delete a user (admin only)
    -   `POST /login`: Authenticate a user
    -   `POST /logout`: Logout a user
4.  Use the following endpoints to manage groups:
    -   `POST /groups`: Create a new group
    -   `GET /groups`: Get a list of all groups
    -   `GET /groups/{group_id}`: Get information about a specific group
    -   `PUT /groups/{group_id}`: Update a group's information
    -   `DELETE /groups/{group_id}`: Delete a group
5.  Use the following endpoints to manage group messages:
    -   `POST /groups/{group_id}/messages`: Send a message in a group
    -   `PUT /groups/{group_id}/messages/{message_id}/like`: Like a message in a group

Note: Some of the endpoints are restricted to admin users only.

### License

This project is licensed under the MIT License - see the [LICENSE](https://chat.openai.com/c/LICENSE) file for details.
