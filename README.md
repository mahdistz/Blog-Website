# Django Blog Site

#### Description:
📝 This is a Django project that provides a simple blog website with various features. Let's dive into the details!

## Features

⚙️ The blog website offers the following features:

- User Registration and Login ✅
- Post Creation ✏️
- Post Editing 🖊️
- Post Deletion 🗑️
- Commenting 💬
- Liking Posts ❤️
- Search 🔍
- Custom 404 Page 🚫
- Profile Page for Users 👤
- Social Login with Google and GitHub Providers 🌐
- Show Visit Count for Each Post 📈

## Prerequisites

🛠️ Before you begin, make sure you have the following installed on your system:

- Python 3.8 or higher 
- Django 3.2 or higher 

## Installation

🚀 Let's get started with the installation process.

- Update the .env.example file (Required):

    Rename the `.env.example` file to `.env` and update the values with your project's specific information:
    
    ```bash
    SECRET_KEY=Your-Django-Project-Secret-Key
    ALLOWED_HOSTS=127.0.0.1,localhost,Your-domain.com
    GOOGLE_APP_CLIENT_ID=Your-GOOGLE-APP-CLIENT-ID
    GOOGLE_APP_CLIENT_SECRET=Your-GOOGLE-APP-CLIENT-SECRET
    GITHUB_APP_CLIENT_ID=Your-GITHUB-APP-CLIENT-ID
    GITHUB_APP_CLIENT_SECRET=Your-GITHUB-APP-CLIENT-SECRET
    ```

- Create a virtual environment:

    **Windows**:
    
    ```Bash
    python -m venv venv
    ```
    
    **Linux**:
    
    ```Bash
    python3 -m venv venv
    ```

- Activate the virtual environment:
    
    **Windows**:
    
    ```Bash
    venv\Scripts\activate
    ```
    
    **Linux**:
    
    ```Bash
    source venv/bin/activate
    ```

- Install the project dependencies:
    
    ```Bash
    pip install -r requirements.txt
    ```
    
- Apply the database migrations:
        
    ```Bash
    python manage.py makemigrations
    python manage.py migrate
    ```

- Collect static files: 
    
    Collect static files, such as images, CSS, and JavaScript, to make them accessible to the web server:
    
    ```Bash
    python manage.py collectstatic
    ```

- Create a superuser account:
    
    ```Bash
    python manage.py createsuperuser
    ```

- Run the development server:
    
    ```Bash
    python manage.py runserver
    ```

## Configuring Social Login with Google and GitHub

🔒 To enable social login with Google and GitHub, follow these steps:

### Creating a Google OAuth Client ID and Secret

1. Go to the [Google Cloud Platform Console]( https://console.cloud.google.com).

2. Create a new project or select an existing one.

3. In the sidebar, select `APIs & Services` > `Credentials`.

4. Click Create Credentials > `OAuth client ID`.

5. Select `Web application` as the application type.

6. Enter a name for your project, such as "Django Blog Project".

7. Click Create to generate the Client ID and Client Secret.

8. Copy the Client ID and Client Secret for later use.

### Creating a GitHub OAuth Client ID and Secret

1. Go to the [GitHub Developer settings](https://github.com/settings/developers).

2. Click New OAuth application.

3. Enter a name for your project, such as "Django Blog Project".

4. Provide a brief description of your project.

5. Enter your homepage URL, which is the URL of your Django blog website.

6. Click Register application to generate the Client ID and Client Secret.

7. Copy the Client ID and Client Secret for later use.

## Conclusion

🎉 Congratulations! You have successfully set up the Django Blog Project. Enjoy blogging and exploring the various features of the website! If you have any issues or questions, feel free to reach out. Happy coding! 