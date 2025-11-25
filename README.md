UNIBAAZAR - The College Nexus 🎓

UNIBAAZAR is a comprehensive Student Resource Management System designed to bridge the gap between Students, Professors, and Campus Societies. It creates a centralized digital ecosystem for academic collaboration and peer-to-peer commerce.

🚀 Key Features

1. 🛒 Student Marketplace

Peer-to-Peer Trading: Students can list old books, electronics, and gear.

Transaction Logic: Integrated "Buy Now" functionality that instantly updates inventory status from 'Available' to 'Sold'.

Rich Descriptions: Multi-line text support for detailed item conditions.

2. 🏛️ Campus Societies Hub

Event Tracking: View upcoming events and dates for Tech Clubs, Dance Crews, and Debate Societies.

Card & Row Layouts: Optimized UI for easy browsing of society information.

3. 🔬 Research Project Portal

Professor Dashboard: Faculty can post research opportunities and required skill sets.

Student Applications: Students can apply directly to projects with their resume/skills.

🛠️ System Architecture (OOP)

This project is not just a script; it is engineered using a robust 16-Class Object-Oriented Architecture to ensure modularity and scalability.

Core OOP Principles Implemented:

Inheritance: Student and Professor classes inherit from a secure abstract User class.

Polymorphism: The PaymentProcessor interface allows for flexible payment methods (e.g., WalletPayment).

Encapsulation: Sensitive data (like user sessions) is managed via a Singleton SessionManager, and direct attribute access is restricted.

Abstraction: Abstract Base Classes (ABC) define strict contracts for MarketItem and User types.

Database Design (SQLite)

The system uses a relational database to ensure Data Persistence.

Users: Stores credentials and roles.

Items: Links products to Student Sellers.

Applications: Links Students to Projects (Foreign Keys).


💻 Installation & Usage

Clone the Repository

git clone [https://github.com/yourusername/unibaazar.git](https://github.com/yourusername/unibaazar.git)
cd unibaazar


Run the Application

python main.py


Default Login Credentials (for Testing)

Professor: professoroops@gmail.com | Pass: professoroops

Student: amitbishnoi@gmail.com | Pass: amitbishnoi

(Or register a new account on the Login Screen)

📂 Project Structure

├── main.py           # The GUI Controller (Tkinter)
├── models.py         # The Logic Layer (16 OOP Classes)
├── db_manager.py     # Database Connectivity & Table Creation
└── README.md         # Documentation


👨‍💻 Author
Amit Bishnoi
LinkedIn Profile - https://www.linkedin.com/in/amit-bishnoi-1a928531a/
