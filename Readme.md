## Overview
This Multiple-Choice Questionnaire (MCQ) application is designed for computer science students, offering an interactive way to test their knowledge across various subjects. Built with Python and CustomTkinter, it features a modern, user-friendly interface with multiple quiz modes and comprehensive user tracking.

## Features

### User Management
- User registration and login system
- Secure password authentication
- Persistent user data storage using JSON
- Comprehensive quiz history tracking

### Quiz Features
- Multiple quiz categories support
- Real-time feedback on answers
- Detailed score evaluation
- Performance tracking and history

### User Interface
- Modern, responsive GUI using CustomTkinter
- Intuitive navigation between screens
- Progress tracking during quizzes
- Color-coded feedback for incorrect answers
- Comprehensive score reports

## Installation

### Prerequisites
- Python 3.x
- CustomTkinter library
- bcrypt library

### Setup
1. Clone the repository:
```bash
git clone https://github.com/NabilKara/MCQ_APP.git
```

2. Create and activate a virtual environment:

On all platforms:
```bash
python3 -m venv venv
```

For Linux & Mac OS:
```bash
source venv/bin/activate
```

For Windows (command prompt):
```bash
venv\Scripts\activate
```

3. Install required dependencies:
```bash
pip install customtkinter
pip install bcrypt
```

4. Run the application:
```bash
python3 main.py
```

## Usage

### Getting Started
1. Launch the application
2. Choose either "Login" or "Sign Up"
3. Enter your credentials
4. Press the  start quiz button
5. Choose your preferred categories
6. Start the quiz

### Taking a Quiz
- Read each question carefully
- Select your answer from the provided options
- Make sure that time doesn't run out
- Submit your answer to proceed
- Receive immediate feedback on your response
- View your final score and performance evaluation
- Access your quiz history at any time

### Viewing History
- Access your quiz history from the welcome screen
- View detailed performance metrics for each attempt
- Track your progress over time
- Export your history to a CSV file.

## Project Structure

```
.
├── backend/
│   ├── __init__.py
│   ├── question_management.py
│   ├── score_evaluation.py
│   └── user_management.py
├── data/
│   ├── questions.json
│   └── users.json
├── gui/
│   ├── __init__.py
│   └── front.py
├── .gitignore
├── LICENSE
├── main.py
└── README.md
```

## Features in Detail

### Question Management
- Questions stored in JSON format
- Support for multiple categories
- Each question includes:
  - Question text
  - Multiple choice options
  - Correct answer
  - Category

### Score Evaluation
- Real-time score tracking
- Category-wise performance analysis
- Percentage calculation
- Performance feedback based on score

### History Tracking
- Date and time of each attempt
- Category-wise scores
- Overall performance metrics
- Historical trend analysis
- Export History to a CSV file

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Credits
Developed by KARA Nabil, MEDJBER Abderrahim and KAMIRI Wassim as part of the Python Programming course at the University of Science and Technology Houari Boumediene, under the guidance of Professor MOUHOUN SAID.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
