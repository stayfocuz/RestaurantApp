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
        # Professional gradient-like background using a solid color (Tkinter limitation)
        self.root.configure(bg="#f5f7fa")  # Light grayish-blue

        # Reset all state for a fresh start
        self.order = []
        self.quantity = []
        self.cups = 0
        self.selected_indices = []
        self.menu_vars = []
        self.prev_selected = []
        if hasattr(self, 'quantity_vars'):
            del self.quantity_vars
        if hasattr(self, 'quantity_indices'):
            del self.quantity_indices
        if hasattr(self, 'rice_var'):
            del self.rice_var

        # --- Improved Logo and Spacing ---
        logo_frame = tk.Frame(self.root, bg="#f5f7fa", width=300, height=200)
        logo_frame.pack(pady=(60, 10))
        logo_frame.update_idletasks()

        chef_label = tk.Label(logo_frame, text="👨‍🍳", font=("Arial", 110), bg="#f5f7fa")
        chef_label.place(x=90, y=60)
        chef_label.update_idletasks()

        crown_label = tk.Label(logo_frame, text="👑", font=("Arial", 44), bg="#f5f7fa")
        chef_width = chef_label.winfo_width()
        crown_width = crown_label.winfo_reqwidth()
        crown_x = 90 + (chef_width // 2) - (crown_width // 2)
        crown_label.place(x=crown_x, y=20)

        tk.Label(
            self.root,
            text="Welcome to Kings Delight!",
            font=("Arial", 28, "bold"),
            bg="#f5f7fa",
            fg="#1a237e"  # Deep blue
        ).pack(pady=(10, 8))
        tk.Label(
            self.root,
            text='"Where every meal is a masterpiece!"',
            font=("Arial", 16, "italic"),
            bg="#f5f7fa",
            fg="#3949ab"  # Lighter blue
        ).pack(pady=(0, 40))
        tk.Label(
            self.root,
            text="Click anywhere to start your order",
            font=("Arial", 16, "bold"),
            bg="#f5f7fa",
            fg="#263238"  # Almost black
        ).pack(pady=(0, 40))
        self.root.bind("<Button-1>", self._main_page_click)

    def _main_page_click(self, event):
        self.root.unbind("<Button-1>")
        self.create_menu_ui()

    def create_menu_ui(self):
        self.clear_window()
        self.root.configure(bg="#f5f7fa")
        tk.Label(self.root, text="Welcome to our restaurant!", font=("Arial", 18, "bold"), bg="#f5f7fa", fg="#1a237e").pack(pady=(20, 5))
        tk.Label(self.root, text="MENU", font=("Arial", 14, "bold"), bg="#f5f7fa", fg="#3949ab").pack()
        self.menu_frame = tk.Frame(self.root, bg="#e8eaf6", bd=2, relief="groove")
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
                bg="#e8eaf6",
                activebackground="#c5cae9",
                selectcolor="#c5cae9",
                fg="#263238"
            )
            cb.grid(row=idx, column=0, sticky='w', padx=10, pady=2)
            self.menu_vars.append(var)
        button_frame = tk.Frame(self.root, bg="#f5f7fa")
        button_frame.pack(pady=18)
        tk.Button(
            button_frame, text="Back", command=self.show_main_page,
            bg="#b0bec5", fg="#263238", activebackground="#90a4ae", activeforeground="#263238",
            font=("Arial", 12, "bold"), bd=0, relief="ridge", padx=20, pady=5, cursor="hand2"
        ).pack(side="left", padx=10)
        tk.Button(
            button_frame, text="Next", command=self.get_order_quantities,
            bg="#3949ab", fg="#fff", activebackground="#1a237e", activeforeground="#fff",
            font=("Arial", 12, "bold"), bd=0, relief="ridge", padx=20, pady=5, cursor="hand2"
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
        self.root.configure(bg="#f5f7fa")
        tk.Label(self.root, text="Enter quantity for each selected dish:", font=("Arial", 16, "bold"), bg="#f5f7fa", fg="#3949ab").pack(pady=15)
        self.qty_frame = tk.Frame(self.root, bg="#e8eaf6", bd=2, relief="groove")
        self.qty_frame.pack(pady=10, padx=30)
        self.selected_entry_idx = 0  # Track which entry is active

        def set_active_entry(idx):
            self.selected_entry_idx = idx

        for idx, i in enumerate(self.selected_indices):
            dish, price = viand[i]
            label = tk.Label(self.qty_frame, bg="#e8eaf6")
            label.grid(row=idx, column=0, sticky='w', padx=10, pady=2)
            label_text = f"{dish.ljust(15)} Php "
            label.config(text=label_text, font=("Consolas", 13), fg="#263238")
            price_label = tk.Label(self.qty_frame, text=money_fmt(price), font=("Consolas", 13, "bold"), bg="#e8eaf6", fg="#263238")
            price_label.grid(row=idx, column=1, sticky='w')
            entry = tk.Entry(self.qty_frame, textvariable=self.quantity_vars[idx], width=5, font=("Consolas", 13, "bold"), justify="center", bg="#fffde7", fg="#1a237e")
            entry.grid(row=idx, column=2, padx=5)
            entry.bind("<FocusIn>", lambda e, idx=idx: set_active_entry(idx))

        # --- Virtual Keyboard ---
        keyboard_frame = tk.Frame(self.root, bg="#f5f7fa")
        keyboard_frame.pack(pady=(10, 0))

        def keyboard_press(num):
            idx = self.selected_entry_idx
            current = self.quantity_vars[idx].get()
            if len(current) < 2:
                self.quantity_vars[idx].set(current + str(num))

        def keyboard_clear():
            idx = self.selected_entry_idx
            self.quantity_vars[idx].set("")

        def keyboard_backspace():
            idx = self.selected_entry_idx
            current = self.quantity_vars[idx].get()
            self.quantity_vars[idx].set(current[:-1])

        btns = [
            ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
            ('0', 3, 1)
        ]
        for (text, r, c) in btns:
            tk.Button(keyboard_frame, text=text, width=5, height=2, font=("Arial", 14, "bold"),
                      bg="#fffde7", fg="#1a237e", activebackground="#ffe082", activeforeground="#1a237e",
                      command=lambda t=text: keyboard_press(t), cursor="hand2").grid(row=r, column=c, padx=2, pady=2)
        tk.Button(keyboard_frame, text="Clear", width=5, height=2, font=("Arial", 12),
                  bg="#b0bec5", fg="#263238", activebackground="#90a4ae", activeforeground="#263238",
                  command=keyboard_clear, cursor="hand2").grid(row=3, column=0, padx=2, pady=2)
        tk.Button(keyboard_frame, text="⌫", width=5, height=2, font=("Arial", 12),
                  bg="#b0bec5", fg="#263238", activebackground="#90a4ae", activeforeground="#263238",
                  command=keyboard_backspace, cursor="hand2").grid(row=3, column=2, padx=2, pady=2)

        button_frame = tk.Frame(self.root, bg="#f5f7fa")
        button_frame.pack(pady=18)
        tk.Button(
            button_frame, text="Back", command=self.create_menu_ui,
            bg="#b0bec5", fg="#263238", activebackground="#90a4ae", activeforeground="#263238",
            font=("Arial", 12, "bold"), bd=0, relief="ridge", padx=20, pady=5, cursor="hand2"
        ).pack(side="left", padx=10)
        tk.Button(
            button_frame, text="Next", command=self.ask_rice,
            bg="#3949ab", fg="#fff", activebackground="#1a237e", activeforeground="#fff",
            font=("Arial", 12, "bold"), bd=0, relief="ridge", padx=20, pady=5, cursor="hand2"
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
        self.root.configure(bg="#f5f7fa")
        rice_frame = tk.Frame(self.root, bg="#e8eaf6", bd=2, relief="groove")
        rice_frame.pack(pady=30, padx=30)
        rice_label = tk.Label(rice_frame, text=f"{'Rice'.ljust(15)} Php ", font=("Consolas", 13), bg="#e8eaf6", fg="#263238")
        rice_label.grid(row=0, column=0, sticky='w', padx=10, pady=2)
        rice_price_label = tk.Label(rice_frame, text=money_fmt(rice_price), font=("Consolas", 13, "bold"), bg="#e8eaf6", fg="#263238")
        rice_price_label.grid(row=0, column=1, sticky='w')
        if not hasattr(self, 'rice_var'):
            self.rice_var = tk.StringVar(value="0")
        rice_entry = tk.Entry(rice_frame, textvariable=self.rice_var, width=5, font=("Consolas", 13, "bold"), justify="center", bg="#fffde7", fg="#1a237e")
        rice_entry.grid(row=0, column=2, padx=5)
        rice_entry.focus_set()

        # --- Virtual Keyboard for Rice ---
        rice_keyboard_frame = tk.Frame(self.root, bg="#f5f7fa")
        rice_keyboard_frame.pack(pady=(10, 0))

        def rice_keyboard_press(num):
            current = self.rice_var.get()
            if len(current) < 2:
                self.rice_var.set(current + str(num))

        def rice_keyboard_clear():
            self.rice_var.set("")

        def rice_keyboard_backspace():
            current = self.rice_var.get()
            self.rice_var.set(current[:-1])

        btns = [
            ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
            ('0', 3, 1)
        ]
        for (text, r, c) in btns:
            tk.Button(rice_keyboard_frame, text=text, width=5, height=2, font=("Arial", 14, "bold"),
                      bg="#fffde7", fg="#1a237e", activebackground="#ffe082", activeforeground="#1a237e",
                      command=lambda t=text: rice_keyboard_press(t), cursor="hand2").grid(row=r, column=c, padx=2, pady=2)
        tk.Button(rice_keyboard_frame, text="Clear", width=5, height=2, font=("Arial", 12),
                  bg="#b0bec5", fg="#263238", activebackground="#90a4ae", activeforeground="#263238",
                  command=rice_keyboard_clear, cursor="hand2").grid(row=3, column=0, padx=2, pady=2)
        tk.Button(rice_keyboard_frame, text="⌫", width=5, height=2, font=("Arial", 12),
                  bg="#b0bec5", fg="#263238", activebackground="#90a4ae", activeforeground="#263238",
                  command=rice_keyboard_backspace, cursor="hand2").grid(row=3, column=2, padx=2, pady=2)

        tk.Label(self.root, text="Enter 0 if you don't want rice with your order.", font=("Arial", 12, "italic"), bg="#f5f7fa", fg="#3949ab").pack(pady=(0, 10))
        button_frame = tk.Frame(self.root, bg="#f5f7fa")
        button_frame.pack(pady=18)
        tk.Button(
            button_frame, text="Back", command=self.get_order_quantities,
            bg="#b0bec5", fg="#263238", activebackground="#90a4ae", activeforeground="#263238",
            font=("Arial", 12, "bold"), bd=0, relief="ridge", padx=20, pady=5, cursor="hand2"
        ).pack(side="left", padx=10)
        tk.Button(
            button_frame, text="Show Summary", command=self.show_summary,
            bg="#3949ab", fg="#fff", activebackground="#1a237e", activeforeground="#fff",
            font=("Arial", 12, "bold"), bd=0, relief="ridge", padx=20, pady=5, cursor="hand2"
        ).pack(side="left", padx=10)

    def show_summary(self):
        rice_str = self.rice_var.get()
        if not is_non_negative_integer(rice_str) or len(rice_str) > 2 or int(rice_str) > 99:
            messagebox.showerror("Error", "Please enter a valid rice quantity (0-99).")
            return
        self.cups = int(rice_str)
        self.clear_window()
        self.root.configure(bg="#f5f7fa")

        # --- Centered and Bigger "SUMMARY" Title ---
        tk.Label(
            self.root,
            text="SUMMARY",
            font=("Arial", 28, "bold"),
            bg="#f5f7fa",
            fg="#0d47a1",
            justify="center"
        ).pack(pady=(10, 0))

        summary = "\n"
        total_price = 0
        summary_lines = []

        # Calculate max lengths for perfect alignment
        all_names = [viand[i][0] for i in self.selected_indices] + ["Rice"]
        max_name_len = max(len(name) for name in all_names)
        all_qtys = [str(self.quantity[idx]) for idx in range(len(self.selected_indices))] + [str(self.cups)]
        max_qty_len = max(len(qty) for qty in all_qtys)
        all_amounts = [money_fmt(self.quantity[idx]*viand[i][1]) for idx, i in enumerate(self.selected_indices)] + [money_fmt(self.cups * rice_price)]
        max_amt_len = max(len(amt) for amt in all_amounts)

        # Build summary lines with perfect alignment
        for idx, i in enumerate(self.selected_indices):
            dish, price = viand[i]
            qty = self.quantity[idx]
            amount = money_fmt(qty * price)
            line = f"{dish.ljust(max_name_len)}  x{str(qty).rjust(max_qty_len)}  = Php {amount.rjust(max_amt_len)}"
            summary_lines.append(line)
            total_price += qty * price
        rice_amount = money_fmt(self.cups * rice_price)
        rice_line = f"{'Rice'.ljust(max_name_len)}  x{str(self.cups).rjust(max_qty_len)}  = Php {rice_amount.rjust(max_amt_len)}"
        summary_lines.append(rice_line)
        summary += "\n".join([f"\u2022 {l}" for l in summary_lines]) + "\n"
        summary += "-" * (max_name_len + max_qty_len + max_amt_len + 13) + "\n"
        total_line = f"Total: Php {money_fmt(total_price + self.cups * rice_price)}"
        tk.Label(
            self.root,
            text=summary,
            font=("Consolas", 15, "bold"),
            justify='left',
            bg="#f5f7fa",
            fg="#263238"
        ).pack(pady=(0, 0))
        tk.Label(
            self.root,
            text=total_line,
            font=("Arial", 22, "bold"),
            bg="#f5f7fa",
            fg="#1976d2"
        ).pack(pady=(0, 20))
        button_frame = tk.Frame(self.root, bg="#f5f7fa")
        button_frame.pack(pady=18)
        tk.Button(
            button_frame, text="Back", command=self._back_to_rice_with_value,
            bg="#b0bec5", fg="#263238", activebackground="#90a4ae", activeforeground="#263238",
            font=("Arial", 12, "bold"), bd=0, relief="ridge", padx=20, pady=5, cursor="hand2"
        ).pack(side="left", padx=10)
        tk.Button(
            button_frame, text="Proceed to Payment", command=self.pay_order,
            bg="#3949ab", fg="#fff", activebackground="#1a237e", activeforeground="#fff",
            font=("Arial", 14, "bold"), bd=0, relief="ridge", padx=24, pady=8, cursor="hand2"
        ).pack(side="left", padx=10)

    def pay_order(self):
        # Show official receipt as a popup, then auto-close and show thank you message
        def show_receipt_and_close():
            receipt_win = tk.Toplevel(self.root)
            receipt_win.title("Official Receipt")
            receipt_win.configure(bg="#f5f7fa")
            receipt_win.geometry("370x520")
            receipt_win.resizable(False, False)
            # Center the window
            receipt_win.update_idletasks()
            x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 185
            y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 260
            receipt_win.geometry(f"+{x}+{y}")

            # --- Centered and Bigger "OFFICIAL RECEIPT" Title ---
            tk.Label(
                receipt_win,
                text="OFFICIAL RECEIPT",
                font=("Arial", 22, "bold"),
                bg="#f5f7fa",
                fg="#0d47a1",
                justify="center"
            ).pack(pady=(18, 0))

            lines = []
            lines.append("")
            lines.append("      KINGS DELIGHT")
            lines.append("-" * 30)
            import datetime
            now = datetime.datetime.now()
            lines.append(f"Date: {now.strftime('%Y-%m-%d')}")
            lines.append(f"Time: {now.strftime('%H:%M:%S')}")
            lines.append("-" * 30)
            max_name_len = max([len(viand[i][0]) for i in self.selected_indices] + [4])
            all_qtys = [str(self.quantity[idx]) for idx in range(len(self.selected_indices))] + [str(self.cups)]
            max_qty_len = max(len(qty) for qty in all_qtys)
            all_amounts = [money_fmt(self.quantity[idx]*viand[i][1]) for idx, i in enumerate(self.selected_indices)] + [money_fmt(self.cups * rice_price)]
            max_amt_len = max(len(amt) for amt in all_amounts)
            total_price = 0
            for idx, i in enumerate(self.selected_indices):
                dish, price = viand[i]
                qty = self.quantity[idx]
                amount = money_fmt(qty * price)
                line = f"{dish.ljust(max_name_len)}  x{str(qty).rjust(max_qty_len)}  = Php {amount.rjust(max_amt_len)}"
                lines.append(line)
                total_price += qty * price
            rice_amount = money_fmt(self.cups * rice_price)
            rice_line = f"{'Rice'.ljust(max_name_len)}  x{str(self.cups).rjust(max_qty_len)}  = Php {rice_amount.rjust(max_amt_len)}"
            lines.append(rice_line)
            lines.append("-" * (max_name_len + max_qty_len + max_amt_len + 13))
            total_line = f"TOTAL:{' ' * (max_name_len + max_qty_len + 7 - len('TOTAL:'))}Php {money_fmt(total_price + self.cups * rice_price)}"
            lines.append(total_line)
            lines.append("-" * (max_name_len + max_qty_len + max_amt_len + 13))
            lines.append("   THIS IS YOUR OFFICIAL RECEIPT")
            lines.append("      Thank you for ordering!")
            receipt_text = "\n".join(lines)

            tk.Label(receipt_win, text=receipt_text, font=("Consolas", 12), bg="#f5f7fa", fg="#263238", justify="left").pack(padx=20, pady=10)

            # Auto-close after 3 seconds and show thank you message
            def close_and_show_thankyou():
                receipt_win.destroy()
                self.clear_window()
                self.root.configure(bg="#f5f7fa")
                tk.Label(
                    self.root,
                    text="Thank you for choosing Kings Delight!\nWe are always happy to serve you.\nWe hope to see you again soon!",
                    font=("Arial", 18, "bold"),
                    fg="#388e3c",
                    bg="#f5f7fa",
                    justify="center"
                ).pack(pady=40)
                tk.Button(
                    self.root, text="Next Order", command=self.show_main_page,
                    bg="#3949ab", fg="#fff", activebackground="#1a237e", activeforeground="#fff",
                    font=("Arial", 13, "bold"), bd=0, relief="ridge", padx=20, pady=5, cursor="hand2"
                ).pack(pady=18)

            receipt_win.after(3000, close_and_show_thankyou)

        show_receipt_and_close()

    def attach_number_pad(entry_widget, var):
        pad = tk.Toplevel()
        pad.title("Number Pad")
        pad.geometry("220x320")
        pad.resizable(False, False)
        pad.grab_set()

        def append(num):
            current = var.get()
            if len(current) < 2:  # Limit to 2 digits
                var.set(current + str(num))

        def clear():
            var.set("")

        def backspace():
            var.set(var.get()[:-1])

        def done():
            pad.destroy()

        btns = [
            ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
            ('0', 3, 1)
        ]
        for (text, r, c) in btns:
            tk.Button(pad, text=text, width=5, height=2, font=("Arial", 14, "bold"),
                      command=lambda t=text: append(t)).grid(row=r, column=c, padx=2, pady=2)
        tk.Button(pad, text="Clear", width=5, height=2, font=("Arial", 12),
                  command=clear).grid(row=3, column=0, padx=2, pady=2)
        tk.Button(pad, text="⌫", width=5, height=2, font=("Arial", 12),
                  command=backspace).grid(row=3, column=2, padx=2, pady=2)
        tk.Button(pad, text="Done", width=16, height=2, font=("Arial", 12, "bold"),
                  command=done).grid(row=4, column=0, columnspan=3, pady=6)

        pad.transient(entry_widget)
        pad.wait_window()

    def _back_to_rice_with_value(self):
        self.clear_window()
        self.root.configure(bg="#f5f7fa")
        rice_frame = tk.Frame(self.root, bg="#e8eaf6", bd=2, relief="groove")
        rice_frame.pack(pady=30, padx=30)
        rice_label = tk.Label(rice_frame, text=f"{'Rice'.ljust(15)} Php ", font=("Consolas", 13), bg="#e8eaf6", fg="#263238")
        rice_label.grid(row=0, column=0, sticky='w', padx=10, pady=2)
        rice_price_label = tk.Label(rice_frame, text=money_fmt(rice_price), font=("Consolas", 13, "bold"), bg="#e8eaf6", fg="#263238")
        rice_price_label.grid(row=0, column=1, sticky='w')
        # Keep the previously entered rice value
        rice_entry = tk.Entry(rice_frame, textvariable=self.rice_var, width=5, font=("Consolas", 13, "bold"), justify="center", bg="#fffde7", fg="#1a237e")
        rice_entry.grid(row=0, column=2, padx=5)
        rice_entry.focus_set()

        # --- Virtual Keyboard for Rice ---
        rice_keyboard_frame = tk.Frame(self.root, bg="#f5f7fa")
        rice_keyboard_frame.pack(pady=(10, 0))

        def rice_keyboard_press(num):
            current = self.rice_var.get()
            if len(current) < 2:
                self.rice_var.set(current + str(num))

        def rice_keyboard_clear():
            self.rice_var.set("")

        def rice_keyboard_backspace():
            current = self.rice_var.get()
            self.rice_var.set(current[:-1])

        btns = [
            ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
            ('0', 3, 1)
        ]
        for (text, r, c) in btns:
            tk.Button(rice_keyboard_frame, text=text, width=5, height=2, font=("Arial", 14, "bold"),
                      bg="#fffde7", fg="#1a237e", activebackground="#ffe082", activeforeground="#1a237e",
                      command=lambda t=text: rice_keyboard_press(t), cursor="hand2").grid(row=r, column=c, padx=2, pady=2)
        tk.Button(rice_keyboard_frame, text="Clear", width=5, height=2, font=("Arial", 12),
                  bg="#b0bec5", fg="#263238", activebackground="#90a4ae", activeforeground="#263238",
                  command=rice_keyboard_clear, cursor="hand2").grid(row=3, column=0, padx=2, pady=2)
        tk.Button(rice_keyboard_frame, text="⌫", width=5, height=2, font=("Arial", 12),
                  bg="#b0bec5", fg="#263238", activebackground="#90a4ae", activeforeground="#263238",
                  command=rice_keyboard_backspace, cursor="hand2").grid(row=3, column=2, padx=2, pady=2)

        tk.Label(self.root, text="Enter 0 if you don't want rice with your order.", font=("Arial", 12, "italic"), bg="#f5f7fa", fg="#3949ab").pack(pady=(0, 10))
        button_frame = tk.Frame(self.root, bg="#f5f7fa")
        button_frame.pack(pady=18)
        tk.Button(
            button_frame, text="Back", command=self.get_order_quantities,
            bg="#b0bec5", fg="#263238", activebackground="#90a4ae", activeforeground="#263238",
            font=("Arial", 12, "bold"), bd=0, relief="ridge", padx=20, pady=5, cursor="hand2"
        ).pack(side="left", padx=10)
        tk.Button(
            button_frame, text="Show Summary", command=self.show_summary,
            bg="#3949ab", fg="#fff", activebackground="#1a237e", activeforeground="#fff",
            font=("Arial", 12, "bold"), bd=0, relief="ridge", padx=20, pady=5, cursor="hand2"
        ).pack(side="left", padx=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = RestaurantApp(root)
    root.mainloop()