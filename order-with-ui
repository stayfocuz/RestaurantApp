import tkinter as tk
from tkinter import messagebox
from error_handling import is_positive_integer, is_non_negative_integer

viand = [
    ("Mechado", 30),
    ("Adobo", 35),
    ("Sinigang", 30),
    ("Paksiw", 25),
    ("Inihaw", 25),
    ("Ginataan", 30),
    ("Scabitchi", 35),
    ("Prito", 25),
    ("Kalderita", 35),
    ("Soup", 35),
    ("Ginisa", 30)
]

rice_price = 15

def money_fmt(amount):
    return f"{amount:,.2f}"

class RestaurantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Ordering System")
        self.order = []
        self.quantity = []
        self.cups = 0
        self.selected_indices = []
        self.menu_vars = []
        self.prev_selected = []
        self.show_main_page()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_main_page(self):
        self.clear_window()
        self.root.configure(bg="#e3f2fd")
        # Create a frame to help with placement
        logo_frame = tk.Frame(self.root, bg="#e3f2fd", width=200, height=150)
        logo_frame.pack(pady=(20, 0))
        logo_frame.update_idletasks()

        chef_label = tk.Label(logo_frame, text="👨‍🍳", font=("Arial", 80), bg="#e3f2fd")
        chef_label.place(x=50, y=40)
        chef_label.update_idletasks()

        # Place the crown above the chef's head, centered
        crown_label = tk.Label(logo_frame, text="👑", font=("Arial", 32), bg="#e3f2fd")
        # Calculate center based on chef_label width
        chef_width = chef_label.winfo_width()
        crown_width = crown_label.winfo_reqwidth()
        # Place crown at the center top of chef
        crown_x = 50 + (chef_width // 2) - (crown_width // 2)
        crown_label.place(x=crown_x, y=10)

        tk.Label(
            self.root,
            text="Welcome to Kings Delight!",
            font=("Arial", 22, "bold"),
            bg="#e3f2fd",
            fg="#0d47a1"
        ).pack(pady=(0, 10))
        tk.Label(
            self.root,
            text='"Where every meal is a masterpiece!"',
            font=("Arial", 14, "italic"),
            bg="#e3f2fd",
            fg="#1976d2"
        ).pack(pady=(0, 30))
        tk.Label(
            self.root,
            text="Click anywhere to start your order",
            font=("Arial", 14, "bold"),
            bg="#e3f2fd",
            fg="#263238"
        ).pack(pady=(0, 30))
        self.root.bind("<Button-1>", self._main_page_click)

    def _main_page_click(self, event):
        self.root.unbind("<Button-1>")
        self.create_menu_ui()

    def create_menu_ui(self):
        self.clear_window()
        self.root.configure(bg="#e3f2fd")
        tk.Label(self.root, text="Welcome to our restaurant!", font=("Arial", 18, "bold"), bg="#e3f2fd", fg="#0d47a1").pack(pady=(20, 5))
        tk.Label(self.root, text="MENU", font=("Arial", 14, "bold"), bg="#e3f2fd", fg="#1976d2").pack()
        self.menu_frame = tk.Frame(self.root, bg="#ffffff", bd=2, relief="groove")
        self.menu_frame.pack(pady=15, padx=30)
        self.menu_vars = []
        char = ord('A')
        for idx, (dish, price) in enumerate(viand):
            var = tk.IntVar()
            if self.prev_selected and idx in self.prev_selected:
                var.set(1)
            cb = tk.Checkbutton(
                self.menu_frame,
                text=f"{chr(char+idx)}. {dish.ljust(15)} Php {money_fmt(price):>9}",
                variable=var,
                font=("Consolas", 11),
                anchor='w',
                bg="#ffffff",
                activebackground="#e3f2fd",
                selectcolor="#bbdefb",
                fg="#263238"
            )
            cb.grid(row=idx, column=0, sticky='w', padx=10, pady=2)
            self.menu_vars.append(var)
        button_frame = tk.Frame(self.root, bg="#e3f2fd")
        button_frame.pack(pady=18)
        tk.Button(
            button_frame, text="Back", command=self.show_main_page,
            bg="#b0bec5", fg="#263238", activebackground="#90a4ae", activeforeground="#263238",
            font=("Arial", 12, "bold"), bd=0, relief="ridge", padx=20, pady=5
        ).pack(side="left", padx=10)
        tk.Button(
            button_frame, text="Next", command=self.get_order_quantities,
            bg="#1976d2", fg="#fff", activebackground="#1565c0", activeforeground="#fff",
            font=("Arial", 12, "bold"), bd=0, relief="ridge", padx=20, pady=5
        ).pack(side="left", padx=10)

    def get_order_quantities(self):
        self.selected_indices = [i for i, v in enumerate(self.menu_vars) if v.get()]
        self.prev_selected = self.selected_indices.copy()
        if not self.selected_indices:
            messagebox.showerror("Error", "Please select at least one dish.")
            return

        # --- Preserve previous quantities for still-selected dishes ---
        old_quantity_vars = getattr(self, 'quantity_vars', [])
        old_indices = getattr(self, 'quantity_indices', [])
        new_quantity_vars = []
        new_indices = []
        for idx in self.selected_indices:
            if idx in old_indices:
                # Keep previous value for this dish
                prev_var = old_quantity_vars[old_indices.index(idx)]
                new_quantity_vars.append(prev_var)
            else:
                # New dish, default to 1
                new_quantity_vars.append(tk.StringVar(value="1"))
            new_indices.append(idx)
        self.quantity_vars = new_quantity_vars
        self.quantity_indices = new_indices
        # -------------------------------------------------------------

        self.order = []
        self.clear_window()
        self.root.configure(bg="#e3f2fd")
        tk.Label(self.root, text="Enter quantity for each selected dish:", font=("Arial", 16, "bold"), bg="#e3f2fd", fg="#1976d2").pack(pady=15)
        self.qty_frame = tk.Frame(self.root, bg="#ffffff", bd=2, relief="groove")
        self.qty_frame.pack(pady=10, padx=30)
        for idx, i in enumerate(self.selected_indices):
            dish, price = viand[i]
            label = tk.Label(self.qty_frame, bg="#ffffff")
            label.grid(row=idx, column=0, sticky='w', padx=10, pady=2)
            label_text = f"{dish.ljust(15)} Php "
            label.config(text=label_text, font=("Consolas", 13), fg="#263238")
            price_label = tk.Label(self.qty_frame, text=money_fmt(price), font=("Consolas", 13, "bold"), bg="#ffffff", fg="#263238")
            price_label.grid(row=idx, column=1, sticky='w')
            entry = tk.Entry(self.qty_frame, textvariable=self.quantity_vars[idx], width=5, font=("Consolas", 13, "bold"))
            entry.grid(row=idx, column=2, padx=5)
        button_frame = tk.Frame(self.root, bg="#e3f2fd")
        button_frame.pack(pady=18)
        tk.Button(
            button_frame, text="Back", command=self.create_menu_ui,
            bg="#b0bec5", fg="#263238", activebackground="#90a4ae", activeforeground="#263238",
            font=("Arial", 12, "bold"), bd=0, relief="ridge", padx=20, pady=5
        ).pack(side="left", padx=10)
        tk.Button(
            button_frame, text="Next", command=self.ask_rice,
            bg="#1976d2", fg="#fff", activebackground="#1565c0", activeforeground="#fff",
            font=("Arial", 12, "bold"), bd=0, relief="ridge", padx=20, pady=5
        ).pack(side="left", padx=10)

    def ask_rice(self):
        self.quantity = []
        for var in self.quantity_vars:
            qty_str = var.get()
            if not is_positive_integer(qty_str) or len(qty_str) > 2 or int(qty_str) > 99:
                messagebox.showerror("Error", "Please enter a valid positive integer quantity (1-99) for all dishes.")
                return
            self.quantity.append(int(qty_str))
        self.clear_window()
        self.root.configure(bg="#e3f2fd")
        rice_frame = tk.Frame(self.root, bg="#ffffff", bd=2, relief="groove")
        rice_frame.pack(pady=30, padx=30)
        rice_label = tk.Label(rice_frame, text=f"{'Rice'.ljust(15)} Php ", font=("Consolas", 13), bg="#ffffff", fg="#263238")
        rice_label.grid(row=0, column=0, sticky='w', padx=10, pady=2)
        rice_price_label = tk.Label(rice_frame, text=money_fmt(rice_price), font=("Consolas", 13, "bold"), bg="#ffffff", fg="#263238")
        rice_price_label.grid(row=0, column=1, sticky='w')
        # Keep rice_var if it exists, else create
        if not hasattr(self, 'rice_var'):
            self.rice_var = tk.StringVar(value="0")
        rice_entry = tk.Entry(rice_frame, textvariable=self.rice_var, width=5, font=("Consolas", 13, "bold"))
        rice_entry.grid(row=0, column=2, padx=5)
        tk.Label(self.root, text="Enter 0 if you don't want rice with your order.", font=("Arial", 12, "italic"), bg="#e3f2fd", fg="#1976d2").pack(pady=(0, 10))
        button_frame = tk.Frame(self.root, bg="#e3f2fd")
        button_frame.pack(pady=18)
        tk.Button(
            button_frame, text="Back", command=self.get_order_quantities,
            bg="#b0bec5", fg="#263238", activebackground="#90a4ae", activeforeground="#263238",
            font=("Arial", 12, "bold"), bd=0, relief="ridge", padx=20, pady=5
        ).pack(side="left", padx=10)
        tk.Button(
            button_frame, text="Show Summary", command=self.show_summary,
            bg="#1976d2", fg="#fff", activebackground="#1565c0", activeforeground="#fff",
            font=("Arial", 12, "bold"), bd=0, relief="ridge", padx=20, pady=5
        ).pack(side="left", padx=10)

    def show_summary(self):
        rice_str = self.rice_var.get()
        if not is_non_negative_integer(rice_str) or len(rice_str) > 2 or int(rice_str) > 99:
            messagebox.showerror("Error", "Please enter a valid rice quantity (0-99).")
            return
        self.cups = int(rice_str)
        self.clear_window()
        self.root.configure(bg="#e3f2fd")
        summary = "SUMMARY\n\n"
        total_price = 0
        summary_lines = []
        for idx, i in enumerate(self.selected_indices):
            dish, price = viand[i]
            qty = self.quantity[idx]
            line = f"{dish.ljust(15)} x{qty} = Php {money_fmt(qty*price)}"
            summary_lines.append(line)
            total_price += qty * price
        rice_line = f"{'Rice'.ljust(15)} x{self.cups} = Php {money_fmt(self.cups * rice_price)}"
        summary_lines.append(rice_line)
        summary += "\n".join([f"\u2022 {l}" for l in summary_lines]) + "\n"
        summary += "-"*30 + "\n"
        total_line = f"Total: Php {money_fmt(total_price + self.cups * rice_price)}"
        tk.Label(
            self.root,
            text=summary,
            font=("Consolas", 15, "bold"),
            justify='center',
            bg="#e3f2fd",
            fg="#263238"
        ).pack(pady=(10, 0))
        tk.Label(
            self.root,
            text=total_line,
            font=("Arial", 22, "bold"),
            bg="#e3f2fd",
            fg="#1976d2"
        ).pack(pady=(0, 20))
        button_frame = tk.Frame(self.root, bg="#e3f2fd")
        button_frame.pack(pady=18)
        tk.Button(
            button_frame, text="Back", command=self._back_to_rice_with_value,
            bg="#b0bec5", fg="#263238", activebackground="#90a4ae", activeforeground="#263238",
            font=("Arial", 12, "bold"), bd=0, relief="ridge", padx=20, pady=5
        ).pack(side="left", padx=10)
        tk.Button(
            button_frame, text="Proceed to Payment", command=self.pay_order,
            bg="#1976d2", fg="#fff", activebackground="#1565c0", activeforeground="#fff",
            font=("Arial", 14, "bold"), bd=0, relief="ridge", padx=24, pady=8
        ).pack(side="left", padx=10)

    def _back_to_rice_with_value(self):
        # Go back to ask_rice but keep the previously entered rice value
        self.clear_window()
        self.root.configure(bg="#e3f2fd")
        rice_frame = tk.Frame(self.root, bg="#ffffff", bd=2, relief="groove")
        rice_frame.pack(pady=30, padx=30)
        rice_label = tk.Label(rice_frame, text=f"{'Rice'.ljust(15)} Php ", font=("Consolas", 13), bg="#ffffff", fg="#263238")
        rice_label.grid(row=0, column=0, sticky='w', padx=10, pady=2)
        rice_price_label = tk.Label(rice_frame, text=money_fmt(rice_price), font=("Consolas", 13, "bold"), bg="#ffffff", fg="#263238")
        rice_price_label.grid(row=0, column=1, sticky='w')
        # Use the last entered value for rice
        self.rice_var = tk.StringVar(value=str(self.cups))
        rice_entry = tk.Entry(rice_frame, textvariable=self.rice_var, width=5, font=("Consolas", 13, "bold"))
        rice_entry.grid(row=0, column=2, padx=5)
        tk.Label(self.root, text="Enter 0 if you don't want rice with your order.", font=("Arial", 12, "italic"), bg="#e3f2fd", fg="#1976d2").pack(pady=(0, 10))
        button_frame = tk.Frame(self.root, bg="#e3f2fd")
        button_frame.pack(pady=18)
        tk.Button(
            button_frame, text="Back", command=self.get_order_quantities,
            bg="#b0bec5", fg="#263238", activebackground="#90a4ae", activeforeground="#263238",
            font=("Arial", 12, "bold"), bd=0, relief="ridge", padx=20, pady=5
        ).pack(side="left", padx=10)
        tk.Button(
            button_frame, text="Show Summary", command=self.show_summary,
            bg="#1976d2", fg="#fff", activebackground="#1565c0", activeforeground="#fff",
            font=("Arial", 12, "bold"), bd=0, relief="ridge", padx=20, pady=5
        ).pack(side="left", padx=10)

    def pay_order(self):
        self.clear_window()
        self.root.configure(bg="#e3f2fd")
        tk.Label(self.root, text="Thank you and enjoy eating!", font=("Arial", 18, "bold"), fg="#388e3c", bg="#e3f2fd").pack(pady=40)
        tk.Button(
            self.root, text="Next Order", command=self.show_main_page,
            bg="#1976d2", fg="#fff", activebackground="#1565c0", activeforeground="#fff",
            font=("Arial", 13, "bold"), bd=0, relief="ridge", padx=20, pady=5
        ).pack(pady=18)

if __name__ == "__main__":
    root = tk.Tk()
    app = RestaurantApp(root)
    root.mainloop()