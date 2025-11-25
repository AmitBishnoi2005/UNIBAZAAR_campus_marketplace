import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from db_manager import DBManager


from models import (
    SessionManager, Validator, Student, Professor, 
    SaleItem, Transaction, Society, ResearchProject, ProjectApplication
)

db = DBManager()
session = SessionManager()

class CollegeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("UNIBAAZAR - College marketplace")
        self.root.geometry("1920x1080")
        
        self.COLORS = ["#FF1D58", "#F75990", "#FFF685", "#00DDFF", "#0049B7"]
        self.BG_COLOR = "#f4f6f9"
        
        self.create_login_screen()

    def clear_screen(self):
        self.root.unbind('<Return>')
        for widget in self.root.winfo_children():
            widget.destroy()

    #  SCREEN 1: LOGIN

    def create_login_screen(self):
        self.clear_screen()
        self.root.bind('<Return>', lambda event: self.login_logic())

        canvas = tk.Canvas(self.root, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        canvas.bind('<Configure>', lambda e: self.draw_stripes(canvas, e.width, e.height))
        
        login_frame = tk.Frame(self.root, bg="white", bd=0, padx=40, pady=40)
        login_frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=500)
        
        tk.Label(login_frame, text="UNIBAAZAR", font=("Helvetica", 28, "bold"), 
                 fg=self.COLORS[4], bg="white").pack(pady=(10, 5))
        tk.Label(login_frame, text="Campus Marketplace", font=("Arial", 12), 
                 fg="gray", bg="white").pack(pady=(0, 30))

        tk.Label(login_frame, text="Email Address", bg="white", fg="#333", anchor="w").pack(fill="x")
        self.email_entry = tk.Entry(login_frame, font=("Arial", 12), bg="#f0f0f0", relief="flat")
        self.email_entry.pack(fill="x", pady=(5, 15), ipady=8)

        tk.Label(login_frame, text="Password", bg="white", fg="#333", anchor="w").pack(fill="x")
        self.pass_entry = tk.Entry(login_frame, show="*", font=("Arial", 12), bg="#f0f0f0", relief="flat")
        self.pass_entry.pack(fill="x", pady=(5, 25), ipady=8)

        tk.Button(login_frame, text="LOGIN", font=("Arial", 11, "bold"), bg=self.COLORS[0], fg="white", 
                  relief="flat", command=self.login_logic, cursor="hand2").pack(fill="x", pady=10, ipady=8)
        
        tk.Button(login_frame, text="Create New Account", font=("Arial", 10), bg="white", fg=self.COLORS[4], 
                  relief="flat", command=self.create_register_screen, cursor="hand2").pack(fill="x")

    def draw_stripes(self, canvas, w, h):
        canvas.delete("all")
        step = w / 5
        for i, color in enumerate(self.COLORS):
            canvas.create_rectangle(i*step, 0, (i+1)*step, h, fill=color, outline="")

    def create_register_screen(self):
        self.clear_screen()
        frame = tk.Frame(self.root, bg="white", padx=50, pady=50)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(frame, text="Join Unibaazar", font=("Helvetica", 22, "bold"), bg="white", fg=self.COLORS[4]).pack(pady=20)
        
        inputs = {}
        for field in ["Name", "Email", "Password", "Role (Student/Professor)"]:
            tk.Label(frame, text=field, bg="white", anchor="w").pack(fill="x")
            e = tk.Entry(frame, bg="#f0f0f0", relief="flat"); e.pack(fill="x", pady=5, ipady=5)
            inputs[field] = e
            
        def save():
            if not Validator.validate_email(inputs["Email"].get()):
                messagebox.showerror("Error", "Invalid Email Format")
                return

            role = inputs["Role (Student/Professor)"].get().capitalize()
            if role == "Student":
                u = Student(inputs["Name"].get(), inputs["Email"].get(), inputs["Password"].get())
            else:
                u = Professor(inputs["Name"].get(), inputs["Email"].get(), inputs["Password"].get())
            
            if u.save_to_db():
                messagebox.showinfo("Success", "Account Created!")
                self.create_login_screen()
            else:
                messagebox.showerror("Error", "Email already exists or DB Error")

        tk.Button(frame, text="Sign Up", bg=self.COLORS[3], fg="black", relief="flat", command=save).pack(fill="x", pady=20, ipady=5)
        tk.Button(frame, text="Back to Login", bg="white", command=self.create_login_screen, relief="flat").pack()

    def login_logic(self):
        email = self.email_entry.get()
        password = self.pass_entry.get()
        
        if not Validator.validate_non_empty(email) or not Validator.validate_non_empty(password):
            messagebox.showwarning("Input Error", "Fields cannot be empty")
            return

        user_data = db.fetch_one("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        
        if user_data:
            user_id, name, em, pw, role = user_data
            if role == "Student":
                u = Student(name, em, pw, user_id)
            else:
                u = Professor(name, em, pw, user_id)
            session.set_user(u)
            self.setup_main_layout()
        else:
            messagebox.showerror("Error", "Invalid Credentials")

    #  SCREEN 2: MAIN LAYOUT

    def setup_main_layout(self):
        self.clear_screen()
        current_user = session.get_user()
        
        nav_bar = tk.Frame(self.root, bg="white", height=70)
        nav_bar.pack(side="top", fill="x")
        nav_bar.pack_propagate(False)
        
        tk.Label(nav_bar, text="UNIBAAZAR", font=("Helvetica", 20, "bold"), fg=self.COLORS[0], bg="white").pack(side="left", padx=30)
        
        def logout_action():
            session.logout()
            self.create_login_screen()

        tk.Button(nav_bar, text="Logout", bg="#333", fg="white", relief="flat", command=logout_action).pack(side="right", padx=20)
        tk.Label(nav_bar, text=f"Hi, {current_user.name}", font=("Arial", 10, "bold"), bg="white").pack(side="right", padx=10)
        
        menu_frame = tk.Frame(nav_bar, bg="white")
        menu_frame.pack(side="left", padx=50)
        
        def nav_btn(text, cmd):
            return tk.Button(menu_frame, text=text, font=("Arial", 11, "bold"), 
                             bg="white", fg="#333", activeforeground=self.COLORS[1], 
                             relief="flat", command=cmd)

        nav_btn("SOCIETIES", self.render_societies).pack(side="left", padx=15)
        nav_btn("BUY / SELL", self.render_marketplace).pack(side="left", padx=15)
        nav_btn("PROJECTS", self.render_projects).pack(side="left", padx=15)

        self.canvas_container = tk.Frame(self.root, bg=self.BG_COLOR)
        self.canvas_container.pack(fill="both", expand=True)
        
        self.canvas = tk.Canvas(self.canvas_container, bg=self.BG_COLOR, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.canvas_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.BG_COLOR)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        self.scrollbar.pack(side="right", fill="y")
        
        self.render_societies()


    #  CUSTOM POPUP (MULTI-LINE)

    def open_custom_popup(self, title, fields, submit_callback):
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry("400x500")
        win.configure(bg="white")
        
        tk.Label(win, text=title, font=("Helvetica", 16, "bold"), bg="white", fg=self.COLORS[4]).pack(pady=15)
        
        entries = {}
        for label_text, widget_type in fields:
            tk.Label(win, text=label_text, bg="white", font=("Arial", 10, "bold"), anchor="w").pack(fill="x", padx=20, pady=(10,0))
            if widget_type == 'text':
                txt = tk.Text(win, height=6, font=("Arial", 10), bg="#f0f0f0", relief="flat", padx=5, pady=5)
                txt.pack(fill="x", padx=20, pady=5)
                entries[label_text] = txt
            else:
                ent = tk.Entry(win, font=("Arial", 10), bg="#f0f0f0", relief="flat")
                ent.pack(fill="x", padx=20, pady=5, ipady=5)
                entries[label_text] = ent

        def on_submit():
            data = {}
            for lbl, widget in entries.items():
                if isinstance(widget, tk.Text):
                    data[lbl] = widget.get("1.0", tk.END).strip() 
                else:
                    data[lbl] = widget.get().strip()
            submit_callback(data)
            win.destroy()

        tk.Button(win, text="SUBMIT", bg=self.COLORS[0], fg="white", font=("Arial", 11, "bold"), 
                  relief="flat", command=on_submit).pack(fill="x", padx=20, pady=20, ipady=5)


    # HELPER: CARD CREATOR

    def create_card(self, title, subtitle, tag, color, row, col, cmd=None, btn_text="View", cmd2=None, btn_text2=None):
        """Creates a wide card for horizontal layout"""
        card = tk.Frame(self.scrollable_frame, bg="white", bd=1, relief="flat")
        card.grid(row=row, column=col, padx=15, pady=15, ipadx=5, ipady=5, sticky="nsew")
        
        # Wide Header
        header = tk.Frame(card, bg=color, height=120, width=450)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text=tag, bg="#333333", fg="white", font=("Arial", 8, "bold")).place(x=10, y=10)
        
        content = tk.Frame(card, bg="white", padx=15, pady=10)
        content.pack(fill="both", expand=True)
        
        # Wide wraplength for Horizontal look
        tk.Label(content, text=title, font=("Helvetica", 12, "bold"), bg="white", wraplength=420, anchor="w").pack(fill="x")
        tk.Label(content, text=subtitle, font=("Arial", 9), fg="gray", bg="white", wraplength=420, justify="left", anchor="w").pack(fill="x", pady=5)
        
        btn_frame = tk.Frame(card, bg="white")
        btn_frame.pack(fill="x", padx=15, pady=(0, 15))

        if cmd:
            tk.Button(btn_frame, text=btn_text, bg="black", fg="white", relief="flat", command=cmd).pack(side="left", fill="x", expand=True, padx=(0, 2))
        if cmd2:
            tk.Button(btn_frame, text=btn_text2, bg=self.COLORS[0], fg="white", relief="flat", command=cmd2).pack(side="right", fill="x", expand=True, padx=(2, 0))

    def clear_content(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()


    #  PAGE 1: SOCIETIES (CARDS)
    
    def render_societies(self):
        self.clear_content()
        tk.Label(self.scrollable_frame, text="Campus Societies & Events", font=("Helvetica", 20, "bold"), bg=self.BG_COLOR).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0,20))
        
        societies = [Society("Tech Club", "tech"), Society("Dance Crew", "dance"), Society("Debate Soc", "general")]
        
        r, c = 1, 0
        for soc in societies:
            events_objects = soc.load_events()
            next_event = events_objects[0]
            subtitle = f"Category: {soc.category.upper()}\nNext: {next_event.name} ({next_event.date})"
            
            # Using Wide Card Creator
            self.create_card(title=soc.name, subtitle=subtitle, tag="SOCIETY", color=self.COLORS[3],
                             row=r, col=c, cmd=lambda s=soc: self.show_events_popup(s), btn_text="View Events")
            c += 1
            if c > 1: c=0; r+=1 # 2 Column Layout

    def show_events_popup(self, society):
        win = tk.Toplevel(self.root)
        win.title(f"Events: {society.name}")
        win.geometry("400x400")
        win.configure(bg="white")
        
        tk.Label(win, text=f"Events for {society.name}", font=("Helvetica", 16, "bold"), bg="white", fg=self.COLORS[4]).pack(pady=20)
        
        events = society.load_events()
        container = tk.Frame(win, bg="white")
        container.pack(fill="both", expand=True, padx=20)
        
        for e in events:
            e_frame = tk.Frame(container, bg="#f9f9f9", bd=1, relief="solid")
            e_frame.pack(fill="x", pady=5, ipadx=5, ipady=5)
            tk.Label(e_frame, text=e.date, font=("Arial", 10, "bold"), bg=self.COLORS[2], width=12).pack(side="left", padx=10)
            tk.Label(e_frame, text=e.name, font=("Arial", 11), bg="#f9f9f9").pack(side="left", padx=10)

        tk.Button(win, text="Close", command=win.destroy, bg="#333", fg="white", relief="flat").pack(pady=20)


    # PAGE 2: MARKETPLACE

    def render_marketplace(self):
        self.clear_content()
        
        head = tk.Frame(self.scrollable_frame, bg=self.BG_COLOR)
        head.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0,20))
        tk.Label(head, text="Marketplace", font=("Helvetica", 20, "bold"), bg=self.BG_COLOR).pack(side="left")
        tk.Button(head, text="+ SELL ITEM", bg=self.COLORS[0], fg="white", font=("Arial", 10, "bold"), relief="flat", command=self.add_item_popup).pack(side="right")

        items = db.fetch_all("SELECT * FROM items WHERE status='Available'")
        
        r, c = 1, 0
        for item in items:
            i_id, title, desc, price, type_i, oid, status = item
            color = self.COLORS[1]
            display_text = f"Price: ${price}\n{desc[:40]}..."
            
            def buy_action(iid=i_id, p=price):
                if messagebox.askyesno("Confirm", "Do you want to buy this item?"):
                    current_user = session.get_user()
                    if not current_user: return
                    trans = Transaction(iid, current_user.student_id if hasattr(current_user, 'student_id') else 0, p)
                    if trans.execute():
                        messagebox.showinfo("Success", "Item Purchased via Wallet! Log Updated.")
                        self.render_marketplace()

            def view_action(d=desc):
                messagebox.showinfo("Details", f"Full Description:\n{d}")

            self.create_card(title, display_text, "SALE", color, r, c, cmd=view_action, btn_text="View", cmd2=buy_action, btn_text2="Buy Now")
            c += 1
            if c > 1: c=0; r+=1

    def add_item_popup(self):
        def save_item_logic(data):
            title = data["Item Title"]
            price_str = data["Price"]
            desc = data["Description"]
            
            if Validator.validate_non_empty(title) and Validator.validate_non_empty(price_str):
                user = session.get_user()
                sid = user.student_id if hasattr(user, 'student_id') else 0
                item = SaleItem(title, desc, float(price_str), sid)
                item.post()
                self.render_marketplace()

        fields = [("Item Title", "entry"), ("Price", "entry"), ("Description", "text")]
        self.open_custom_popup("Sell Item", fields, save_item_logic)


    #  PAGE 3: PROJECTS

    def render_projects(self):
        self.clear_content()
        
        head = tk.Frame(self.scrollable_frame, bg=self.BG_COLOR)
        head.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0,20))
        tk.Label(head, text="Research Projects", font=("Helvetica", 20, "bold"), bg=self.BG_COLOR).pack(side="left")
        
        current_user = session.get_user()
        if current_user.role == "Professor":
            tk.Button(head, text="+ POST PROJECT", bg=self.COLORS[4], fg="white", font=("Arial", 10, "bold"), relief="flat", command=self.add_project_popup).pack(side="right")

        projects = ResearchProject.get_all()
        
        r, c = 1, 0
        for p in projects:
            p_id, title, desc, prof = p
            display_desc = desc if len(desc) < 60 else desc[:60] + "..."
            
            if current_user.role == "Student":
                def apply_cmd(pid=p_id):
                    app = ProjectApplication(pid, current_user.student_id, current_user.name)
                    app.submit()
                    messagebox.showinfo("Success", "Applied!")
                cmd = apply_cmd
                btn = "Apply Now"
            else:
                cmd = lambda d=desc: messagebox.showinfo("Full Details", d)
                btn = "View Full Details"
            
            self.create_card(title, display_desc, "RESEARCH", self.COLORS[4], r, c, cmd, btn)
            c += 1
            if c > 1: c=0; r+=1

    def add_project_popup(self):
        def save_project_logic(data):
            title = data["Project Title"]
            desc = data["Project Details & Skills"]
            if Validator.validate_non_empty(title):
                user = session.get_user()
                ResearchProject.create(title, desc, user.prof_id)
                self.render_projects()

        fields = [("Project Title", "entry"), ("Project Details & Skills", "text")]
        self.open_custom_popup("Post New Project", fields, save_project_logic)

# Execution
if __name__ == "__main__":
    root = tk.Tk()
    app = CollegeApp(root)
    root.mainloop()