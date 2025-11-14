# Weather Application - Module 6 Lab

## Student Information
- **Name**: Jasmin Francisco
- **Student ID**: 231004627
- **Course**: CCCS 106
- **Section**: BSCS 3B

## Project Overview
This Weather App allows users to quickly check the current weather of any city by entering its name. It displays detailed information such as temperature, “feels like” temperature, humidity, wind speed, and a weather description with an icon. The app also keeps a recent search history, letting users easily revisit previously searched cities and toggle between light and dark themes for better usability.

## Features Implemented

### Base Features
- [/] City search functionality
- [/] Current weather display
- [/] Temperature, humidity, wind speed
- [/] Weather icons
- [/] Error handling
- [/] Modern UI with Material Design

### Enhanced Features
1. **[Light/Dark Theme Toggle]**
   - This allows the system to switch between light or dark mode
   - So that it can be more visual appealing to the users depending to the mode wanted
   - The challenge was where to put theme and I didn't properly noticed the proper implementation f the code and I solved it with the help of flet.

2. **[Search History]**
   - This can store last 5-10 searched cities that display them in a dropdown type
   - Aside that this is one of the easiest to implement, it iskind of essential for searching in order to have easy access to the previous searched city.
   - Although this was one of the easiest features to implement, I initially struggled with placing it below the input bar because the UI kept breaking. I was able to overcome this by exploring different ways to fix it

## Screenshots for this task

### LIGHTMODE
![alt text](lightmode.png)

### DARKMODE
![alt text](darkmode.png)

### HISTORY
![alt text](history.png)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions
```bash
# Clone the repository
git clone https://github.com/<jasscs>/cccs106-projects.git
cd cccs106-projects/mod6_labs

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Add your OpenWeatherMap API key to .env
