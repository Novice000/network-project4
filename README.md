# CS50W Project 4: Social Network

This is a web-based social networking application developed as part of the CS50 Web Programming with Python and JavaScript course (Harvard University). The app allows users to create an account, post messages, follow/unfollow other users, and like/unlike posts.

## Features

- **User Authentication**: Sign up, login, and logout functionality with form validation.
- **User Profile**: Users can view their own profile, edit posts, and see their followers and followed users.
- **Post Creation**: Users can create posts, which are displayed on the main feed.
- **Follow/Unfollow**: Users can follow or unfollow other users to personalize their feed.
- **Like/Unlike**: Users can like or unlike posts on the feed.
- **Pagination**: Posts and followers are paginated for efficient browsing.

## Improvements

### 1. **Performance Enhancements**
   - Optimized database queries using `select_related`, `prefetch_related`, and query annotations (`Exists` with `OuterRef`), which reduced the number of database hits, especially on pages displaying posts and user profiles.
   - Reduced the need for unnecessary loops by fetching and annotating all necessary data in one query (e.g., whether the current user has liked a post).

### 2. **Custom Styling**
   - Developed a unique design using CSS, ensuring an intuitive user interface with improved visual aesthetics. 
   - The layout is responsive and designed for optimal viewing on both mobile and desktop devices.

## Technologies Used

- **Python**: Backend logic implemented using Python with Django.
- **Django**: The framework used for building the application, handling user authentication, models, views, and templates.
- **HTML/CSS**: For building and styling the front-end templates.
- **JavaScript**: Optional for handling dynamic features (e.g., liking/unliking posts).
- **SQLite**: Default database used for development.

## Setup and Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/cs50w-project4.git
   cd cs50w-project4
   ```

2. **Install Dependencies**:
   Create a virtual environment and activate it.
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

   Install required packages using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

3. **Apply Migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

   Now, you can access the application at `http://127.0.0.1:8000/`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
