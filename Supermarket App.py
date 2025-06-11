import tkinter as tk
from tkinter import messagebox

items = {
    "rice": {"price": 500, "unit": "bag"},
    "beans": {"price": 700, "unit": "cup"},
    "bread": {"price": 350, "unit": "loaf"},
    "milk": {"price": 300, "unit": "satchet"},
    "onion": {"price": 150, "unit": "bulb"},
    "oil": {"price": 1200, "unit": "bottle"},
    "garri": {"price": 200, "unit": "cup"},
    "sweet": {"price": 100, "unit": "stick"},
    "peanut": {"price": 250, "unit": "satchet"}
}

cart = []

def show_unit_prices(event=None):
    raw_input = item_entry.get().strip().lower()
    names = [name.strip() for name in raw_input.split(',') if name.strip()]

    display_lines = []
    for name in names:
        if name in items:
            price = items[name]["price"]
            unit = items[name]["unit"]
            display_lines.append(f"{name.title()}: ₦{price} per {unit}")
        else:
            display_lines.append(f"{name.title()}: Item not found")
    unit_price_label.config(text="\n".join(display_lines))

def add_items():
    names = item_entry.get().strip().lower().split(",")
    qtys = quantity_entry.get().strip().split(",")

    names = [n.strip() for n in names if n.strip()]
    qtys = [q.strip() for q in qtys if q.strip()]

    if len(names) != len(qtys):
        messagebox.showerror("Mismatch", "Items and quantities must match in number.")
        return

    for name, qty_text in zip(names, qtys):
        if name not in items:
            messagebox.showwarning("Not Found", f"'{name}' is not available in store.")
            continue
        try:
            qty = int(qty_text)
            if qty <= 0:
                raise ValueError
            cart.append((name, qty))
        except ValueError:
            messagebox.showerror("Invalid Quantity", f"Invalid quantity for '{name}'.")
            return

    update_receipt()
    item_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    unit_price_label.config(text="")

def update_receipt():
    receipt = "🧾 Supermarket Receipt 🧾\n-----------------------------\n"
    total = 0
    for item, qty in cart:
        price = items[item]["price"]
        unit = items[item]["unit"]
        cost = price * qty
        total += cost
        receipt += f"{item.title()} ({qty} {unit}{'s' if qty > 1 else ''} @ ₦{price}) = ₦{cost}\n"
    result_label.config(text=receipt)

def calculate_total():
    if not cart:
        messagebox.showinfo("Empty", "No items in cart.")
        return
    total = sum(items[item]["price"] * qty for item, qty in cart)
    current = result_label.cget("text")
    result_label.config(text=current + f"\n\n💰 Total Amount Due: ₦{total}")

def clear_all():
    cart.clear()
    result_label.config(text="")
    item_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    unit_price_label.config(text="")

root = tk.Tk()
root.title("Supermarket Billing System")
root.geometry("600x650")
root.config(bg="#f0f8ff")

tk.Label(root, text="🛒 Supermarket Billing App", font=("Helvetica", 20, "bold"), bg="#f0f8ff", fg="#2e86c1").pack(pady=10)

tk.Label(root, text="Enter item names (e.g. rice, oil):", bg="#f0f8ff", font=("Arial", 11)).pack()
item_entry = tk.Entry(root, font=("Arial", 12), width=50, bg="#e8f8f5")
item_entry.pack(pady=5)
item_entry.bind("<KeyRelease>", show_unit_prices)

unit_price_label = tk.Label(root, text="", font=("Arial", 11, "italic"), fg="#2980b9", bg="#f0f8ff", justify="left")
unit_price_label.pack()

tk.Label(root, text="Enter quantities (e.g. 2, 1):", bg="#f0f8ff", font=("Arial", 11)).pack()
quantity_entry = tk.Entry(root, font=("Arial", 12), width=50, bg="#fcf3cf")
quantity_entry.pack(pady=5)

tk.Button(root, text="Add Items", command=add_items, bg="#3498db", fg="white", width=20, font=("Arial", 11)).pack(pady=10)
tk.Button(root, text="Checkout All Items", command=calculate_total, bg="#27ae60", fg="white", width=20, font=("Arial", 11)).pack()
tk.Button(root, text="Clear All", command=clear_all, bg="#e74c3c", fg="white", width=20, font=("Arial", 11)).pack(pady=5)

result_label = tk.Label(root, text="", bg="white", font=("Courier New", 11), justify="left", anchor="w", relief="solid", bd=1, padx=10, pady=10, width=60, height=15)
result_label.pack(pady=20)

root.mainloop()