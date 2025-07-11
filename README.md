# 🎬 Blockbuster Rental System - OOP (Object-Oriented Programming)

## 🧾 Overview

This project simulates a simplified Blockbuster-style video rental system using Python and Object-Oriented Programming (OOP) principles. It allows customers to rent and return videos, while tracking due dates and fines based on return time and video release year. 

It models real-world interactions between customers, videos (DVDs), rentals, and a video store. It includes features like age verification, late return fines, and dynamic video rental management.

---

## 🎯 Project Aims

The goal was to reinforce core OOP concepts such as encapsulation, inheritance, polymorphism, and clean code practices through a hands-on mini-system.

- Practice and demonstrate object-oriented design using Python classes.
- Implement real-world business logic like due dates and fines.
- Follow clean coding principles and Python standards.
- Build testable code using `pytest` and TDD methodology.

---

## Key Concepts

- **OOP Design**: Classes include `Customer`, `Video`, `Rental`, `VideoStore`, and more.
- **Inheritance**: Specialized classes like `DVD` and `VendingMachine` inherit from base classes.
- **Data Validation**: Age checks and rental eligibility enforced.
- **Exception Handling**: Graceful error messages for invalid operations.
- **Testing**: All core functionality is tested using Pytest.

---

## Features

- `Video` class: represents a video with title, release year, and daily rental cost.
- `Customer` class: includes name, date of birth, age calculation, and outstanding fines.
- `Rental` class: manages rentals with dates and video associations.
- `VideoStore` class: provides methods to rent and return videos, with late fine logic.
- Fine calculation: based on how late a video is returned and whether it's a new release.

---

## 📁Project Structure

- [blockbuster/]
    - `blockbuster_oop.py`: Core class implementations
    - `test_blockbuster_challenge.py`: Unit tests for foundational features
    - `test_blockbuster_trainee.py`: More advanced scenarios and edge cases

- `requirements.txt`: Project dependencies
- `.gitignore`: Ignore .venv, pycache, etc.

---

## ⚙️ Getting Setup

1. **Clone the repo**
- `git clone https://github.com/yourusername/Blockbuster-Rental-System-OOP.git`
- `cd Blockbuster-Rental-System-OOP`

2. **Create and activate a virtual environment**
- `python -m venv .venv`
- `source .venv/bin/activate` 
  - On Windows: `.venv\Scripts\activate`

3. **Install dependencies**
- `pip install -r requirements.txt`

--- 

## 🧪 Running the Tests

Make sure your virtual environment is active. Then run:
- `pytest test_blockbuster_challenge.py`
- `pytest test_blockbuster_trainee.py`


# Sample Features
✅ Add customers with validated date of birth
✅ Rent and return videos with due date tracking
✅ Calculate fines for late returns
✅ Separate logic for new releases
✅ Unit tests for all major flows

