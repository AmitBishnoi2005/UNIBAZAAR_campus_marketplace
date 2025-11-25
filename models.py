from abc import ABC, abstractmethod
from datetime import datetime
from db_manager import DBManager

db = DBManager()

# MODULE 1: UTILITIES (this is a kind of helper in our app)

class Logger:
    @staticmethod
    def log_action(message):
        with open("app_log.txt", "a") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {message}\n")

class Validator:
    @staticmethod
    def validate_email(email):
        return "@" in email and "." in email

    @staticmethod
    def validate_non_empty(text):
        return len(text.strip()) > 0

class SessionManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
            cls._instance.current_user = None
        return cls._instance

    def set_user(self, user):
        self.current_user = user
        Logger.log_action(f"User Logged In: {user.email}")

    def get_user(self):
        return self.current_user

    def logout(self):
        if self.current_user:
            Logger.log_action(f"User Logged Out: {self.current_user.email}")
        self.current_user = None

# MODULE 2: USER HIERARCHY

class User(ABC):
    def __init__(self, name, email, password, role):
        self._name = name
        self._email = email
        self._password = password
        self.role = role

    @property
    def name(self): # this is a getter 
        return self._name

    @property   # this is also a getter 
    def email(self):
        return self._email

    def save_to_db(self):
        try:
            db.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
                       (self._name, self._email, self._password, self.role))
            Logger.log_action(f"New User Registered: {self.email}")
            return True
        except:
            return False

class Student(User):
    def __init__(self, name, email, password, student_id=None):
        super().__init__(name, email, password, "Student")
        self.student_id = student_id

class Professor(User):
    def __init__(self, name, email, password, prof_id=None):
        super().__init__(name, email, password, "Professor")
        self.prof_id = prof_id

# MODULE 3: MARKETPLACE

class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass

class WalletPayment(PaymentProcessor):
    def process_payment(self, amount):
        Logger.log_action(f"Payment Processed: ${amount} via Wallet")
        return True

class MarketItem(ABC):
    def __init__(self, title, description, price, owner_id):
        self.title = title
        self.description = description
        self.price = price
        self.owner_id = owner_id

    @abstractmethod
    def post(self):
        pass

    def save_item(self, type_item):
        db.execute("INSERT INTO items (title, description, price, type, owner_id, status) VALUES (?, ?, ?, ?, ?, ?)",
                   (self.title, self.description, self.price, type_item, self.owner_id, "Available"))
        Logger.log_action(f"Item Posted: {self.title}")

class SaleItem(MarketItem):
    def post(self):
        self.save_item("SALE")

class Transaction:
    def __init__(self, item_id, buyer_id, price):
        self.item_id = item_id
        self.buyer_id = buyer_id
        self.price = price
        self.payment_gateway = WalletPayment()

    def execute(self):
        if self.payment_gateway.process_payment(self.price):
            db.execute("UPDATE items SET status='Sold' WHERE item_id=?", (self.item_id,))
            Logger.log_action(f"Item {self.item_id} sold to User {self.buyer_id}")
            return True
        return False

# MODULE 4: ACADEMIC SYSTEM

class Event:
    def __init__(self, name, date):
        self.name = name
        self.date = date

class Society:
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.events = [] 

    def load_events(self):
        if self.category == "tech":
            self.events = [Event("Hackathon 2025", "Jan 15"), Event("AI Seminar", "Jan 20")]
        elif self.category == "dance":
            self.events = [Event("Salsa Night", "Dec 12")]
        else:
            self.events = [Event("General Meetup", "Friday")]
        return self.events

class ResearchProject:
    @staticmethod
    def get_all():
        return db.fetch_all("SELECT * FROM projects")

    @staticmethod
    def create(title, desc, prof_id):
        db.execute("INSERT INTO projects (title, description, prof_id) VALUES (?, ?, ?)",
                   (title, desc, prof_id))
        Logger.log_action(f"Project Created: {title}")

class ProjectApplication:
    def __init__(self, project_id, student_id, student_name):
        self.project_id = project_id
        self.student_id = student_id
        self.student_name = student_name

    def submit(self):
        db.execute("INSERT INTO applications (project_id, student_id, student_name, status) VALUES (?, ?, ?, ?)",
                   (self.project_id, self.student_id, self.student_name, "Pending"))
        Logger.log_action(f"Application Submitted by {self.student_name}")