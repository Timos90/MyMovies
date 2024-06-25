# Movie Database Application

Welcome to the MyMovies Database Application! This application allows users to manage and explore a collection of movies, including adding, deleting, rating, reviewing, and discovering movies based on various criteria.

## Mission Statement

Our mission is to provide a comprehensive platform for movie enthusiasts to efficiently manage their movie collections, discover new movies, and engage with the community through ratings and reviews. We aim to enhance the movie-watching experience by leveraging data-driven recommendations and user interactions.

## Objectives

1. **Manage Movie Collection**
   - Allow users to add new movies with detailed information such as title, genre, director, release year, ratings, and more.
   - Enable users to delete movies from their collection if they no longer wish to keep them.

2. **Interact with Movies**
   - Allow users to view details of a specific movie including its synopsis, ratings, cast, production details, and more.
   - Enable users to rate movies on a scale of 1 to 10, contributing to the overall rating database.

3. **Engage with Reviews and Recommendations**
   - Provide functionality for users to write reviews for movies they have watched, sharing their thoughts and opinions.
   - Offer personalized movie recommendations based on user preferences, including genre, release year, director, and more.

4. **User Management**
   - Allow users to register accounts securely and log in to manage their personalized movie collections and interactions.
   - Ensure user privacy and data security through robust authentication and database management practices.

5. **Enhance User Experience**
   - Create an intuitive and user-friendly interface that facilitates seamless navigation and interaction with the application.
   - Continuously improve the application based on user feedback and evolving movie industry trends.

## Getting Started

To start using the Movie Database Application, follow these steps:

1. **Clone the Repository:**
   ```sh
   git clone https://github.com/Timos90/MyMovies.git
   cd MyMovies

2. Set up database

**NB**: Open a terminal from the `MyMovies` folder in the working directory

```sql
-- Start psql shell from any database and superuser. Preferably postgres
psql -U postgres

-- Create the database
CREATE DATABASE my_movies;

-- Connect to the database
\c my_movies;

-- Create the user
CREATE USER dci_user LOGIN SUPERUSER WITH PASSWORD 'dci_user';
```

4. Create a `.env` file in the root directory of the project and add your database configuration:

    ```plaintext
    DB_USER=dci_user
    DB_PASSWORD=dci_user
    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=my_movies
    ```

### Set up Virtual Environment
In the working directory, open a terminal and run the following command

```bash
$ python3 -m venv .venv --prompt my_movies
```
Source the virtual environment

```bash
$ source .venv/bin/activate
```
Install all packages

```bash
$ pip install -r requirements.txt
```

### Start App
From the working directly, run the following command
```bash
$ python3 -m main
```
You will be presented with a menu. Continue by selecting the options you want.

### Suggestion
For better user experience, after starting the application for the first time, i suggest to insert some movies directly to the database, running the file 'ins_movies.sql' which is located inside the 'insert_movies' folder.

Open a terminal from the `Personal_Database_Mini_Project` folder in the working directory.
```sql
-- Start psql shell from database 
psql -U dci_user -d my_movies;   --provide the password 'dci_user' if necessary

-- run the script to insert the movies
\i insert_movies/ins_movies.sql
```
After that you can run again the application and enjoy!!!