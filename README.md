# Project Setup Guide

Follow these steps to get your project up and running.

## Steps to Get Started

### Step 1: Clone the Project
Clone the repository to your local machine and move into the project directory:
```bash
git clone https://github.com/MeetMRP/socialmedia.git
cd socialmedia
```

### Step 2: Create a Virtual Environment
Create a Python virtual environment for managing dependencies:
```bash
python -m venv env
```

### Step 3: Activate the Virtual Environment
Activate the virtual environment. On Windows (cmd.exe), use:
```bash
env\Scripts\activate.bat
```

### Step 4: Install Dependencies
Install the project dependencies from `requirements.txt`:
```bash
pip install -r requirements.txt
```

### Step 5: Make Migrations
Prepare the database migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Run the Project
Start the project with Django's development server:
```bash
python manage.py runserver
```

Follow these steps to configure your development environment. Happy coding!

## Project Demo
View the project demo [here](https://drive.google.com/file/d/1zp4FXTGFmApC1vkcIapPi_AHEYZO5yM9/view?usp=sharing).