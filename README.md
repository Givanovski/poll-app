# Poll App

#### Video Demo: [Poll App Demonstration](https://www.youtube.com/watch?v=1O1e5ODlPTE)

#### Check out the App: [Poll App on Render](https://poll-app-uubz.onrender.com/)

#### Description:

The **Poll App** is a web-based application developed using Python and Flask, designed to allow users to create, share, and participate in polls with ease. The application is user-friendly, offering a straightforward way to engage with polls, whether you're looking to gather opinions or cast your vote.

### Features

-   **User Authentication**: Users can register, log in, and manage their polls in a secure environment.
-   **Poll Creation**: Registered users can create polls by providing a question and multiple answer options. This feature enables the user to collect responses from others easily.
-   **Voting**: Each user can vote only once per poll per device, ensuring the integrity of the poll results.
-   **Sharing**: Polls can be shared with others via a URL, allowing anyone to participate in the poll.
-   **Dynamic Option Addition**: While creating a poll, users can dynamically add more options to accommodate a wide range of possible answers.
-   **Real-Time Vote Counting**: As users cast their votes, the poll displays the total votes in real-time, giving immediate feedback on how participants are responding.

### Project Structure

The main components of the Poll App include:

1. **`app.py`**: This is the main entry point of the application. It handles the routing, user authentication, poll creation, voting, and session management. Key functionalities include:

    - **User Registration and Login**: Users can register for an account, and their passwords are hashed for security. Upon login, the user’s session is managed using Flask's session system.
    - **Poll Creation**: Users can create new polls with multiple options. A unique URL is generated for each poll, allowing easy sharing.
    - **Voting**: Users can cast their vote on any poll, with the application ensuring that votes are recorded accurately using cookies.
    - **Viewing Polls**: Both individual polls and all polls created by the user can be viewed, with vote counts updated dynamically.

2. **`models.py`**: This file contains the SQLAlchemy models that define the structure of the database tables. The key models include:

    - **`User`**: Represents a registered user, storing the username and hashed password.
    - **`Poll`**: Represents each poll created by users, containing attributes like the question, creator, and unique ID.
    - **`Option`**: Stores each option for a poll, linking it to its corresponding poll.
    - **`Vote`**: Represents individual votes cast by users, linking them to specific options.

3. **`templates` folder**: This folder contains all the HTML templates used to render the front-end of the application. Each template is built using Jinja2 syntax and includes:

    - **`index.html`**: The homepage of the app.
    - **`login.html`**: The login form for users.
    - **`register.html`**: The registration form for new users.
    - **`create_poll.html`**: The form for creating new polls.
    - **`view_poll.html`**: Displays a specific poll, showing all the options and allowing voting.
    - **`view_all_polls.html`**: Displays a list of all polls created by the logged-in user.

4. **`static` folder**: This folder contains static assets like CSS files and JavaScript files.

    - **`style.css`**: Contains custom styling for the application's front-end, ensuring a consistent and user-friendly design.
    - **`script.js`**: Handles front-end interactivity, such as adding dynamic options when creating a poll.

5. **`utils.py`**: Contains utility functions like `get_color()` and `get_real_ip()` that enhance functionality and modularity, making the codebase easier to maintain.

6. **`.env` file**: This file contains environment variables, such as `SECRET_KEY` and database URIs. It is loaded using the `python-dotenv` package to manage sensitive configuration details securely.
7. **`Procfile`**: Used for deployment on Render.com, specifying how the app should be run.
8. **`README.md`**: This file, which provides a detailed explanation of the project.

### Technologies Used

-   **Python**: The core programming language used to develop the application.
-   **Flask**: A micro web framework used for handling routing, session management, and database interactions.
-   **SQLite**: The database used during the development phase.
-   **PostgreSQL**: The database used for deployment, offering a robust and scalable solution for handling larger datasets.
-   **HTML, CSS, JavaScript**: Used to create the front-end interface.
-   **SQLAlchemy**: An Object-Relational Mapping (ORM) tool that manages the database.
-   **Flask-Session**: Used for session management.
-   **Bootstrap**: Provides a responsive and user-friendly frontend, ensuring the app looks good on different devices.

### Design Choices

-   **Cookie-Based Voting**: One of the significant design decisions was to limit voting to once per device per poll using cookies. This ensures that users can't repeatedly vote, helping maintain poll integrity without requiring user authentication for voting.
-   **Database Selection**: The application was developed with SQLite for simplicity during the development phase but deployed with PostgreSQL for better performance and scalability in a production environment.
-   **Separation of Concerns**: The project follows a modular structure, separating routes, models, and utility functions, making the code easier to maintain and extend in the future.
-   **Dynamic Option Addition**: This feature was implemented using JavaScript, providing a more interactive user experience by allowing users to add as many poll options as needed without reloading the page.

### Deployment

The Poll App is deployed on Render.com, using PostgreSQL as the backend database for data storage. It is accessible via a web browser, making it easy for users to interact with polls from any device.

### How to Run Locally

1. Clone the repository from GitHub:
   `git clone https://github.com/Givanovski/poll-app.git`
2. Install the required dependencies using:
   `pip install -r requirements.txt`
3. Set up your environment variables in a `.env` file:
   `SECRET_KEY=your_secret_key DATABASE_URI=sqlite:///polls.db` # For local development
4. Run the Flask application:
   `flask run`
5. Visit `http://127.0.0.1:5000` in your browser to use the Poll App.

### Future Enhancements

-   **User Profiles**: Allow users to customize their profiles and manage their created polls more effectively.
-   **Advanced Analytics**: Provide poll creators with detailed analytics about voter demographics and trends.
-   **Email Notifications**: Notify poll creators when a vote is cast on their poll.

### Conclusion

The Poll App is a comprehensive polling application that allows users to create, share, and participate in polls easily. It combines the power of Python, Flask, and PostgreSQL to deliver a robust and scalable solution. I hope you find it as enjoyable to use as it was to build!

Feel free to try out the app yourself at the link above and watch the video demo to see how it works!
