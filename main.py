import tkinter as tk
from tkinter import messagebox

# -------------------------------
# FRACTIONAL KNAPSACK (Greedy Ratio)
# -------------------------------
# -------------------------------
# FRACTIONAL KNAPSACK (Greedy Ratio)
# -------------------------------
def fractional_knapsack(items, capacity):
    items.sort(key=lambda x: x[0] / x[1], reverse=True)

    total_profit = 0
    selected = []

    for profit, weight in items:
        if capacity >= weight:
            capacity -= weight
            total_profit += profit
            selected.append((profit, weight, "Full"))
        else:
            if capacity > 0:
                fraction = capacity / weight
                total_profit += profit * fraction
                selected.append((profit, weight, fraction)) # Return raw fraction
            break

    return total_profit, selected


# -------------------------------
# GREEDY BY PROFIT
# -------------------------------
def greedy_profit(items, capacity):
    items.sort(key=lambda x: x[0], reverse=True)

    total_profit = 0
    selected = []

    for profit, weight in items:
        if capacity >= weight:
            capacity -= weight
            total_profit += profit
            selected.append((profit, weight))

    return total_profit, selected


# -------------------------------
# GREEDY BY WEIGHT
# -------------------------------
def greedy_weight(items, capacity):
    items.sort(key=lambda x: x[1])

    total_profit = 0
    selected = []

    for profit, weight in items:
        if capacity >= weight:
            capacity -= weight
            total_profit += profit
            selected.append((profit, weight))

    return total_profit, selected


# -------------------------------
# 0/1 KNAPSACK (Dynamic Programming)
# -------------------------------
def knapsack_01(items, capacity):
    n = len(items)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        profit, weight = items[i - 1]

        for w in range(capacity + 1):
            if weight <= w:
                dp[i][w] = max(dp[i - 1][w],
                               profit + dp[i - 1][w - weight])
            else:
                dp[i][w] = dp[i - 1][w]

    # Backtracking to find selected items
    selected = []
    w = capacity

    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            profit, weight = items[i - 1]
            selected.append((profit, weight))
            w -= weight

    return dp[n][capacity], selected[::-1]


# -------------------------------
# MAIN RUN FUNCTION
# -------------------------------
def run_knapsack():
    try:
        capacity = int(capacity_entry.get())

        raw_items = items_text.get("1.0", tk.END).strip().split("\n")
        items = []

        for line in raw_items:
            p, w = map(int, line.split())
            items.append((p, w))

        algo = algo_choice.get()

        if algo == "Fractional (Greedy Ratio)":
            profit, selected = fractional_knapsack(items, capacity)
            complexity = "O(n log n)"

        elif algo == "Greedy by Profit":
            profit, selected = greedy_profit(items, capacity)
            complexity = "O(n log n)"

        elif algo == "Greedy by Weight":
            profit, selected = greedy_weight(items, capacity)
            complexity = "O(n log n)"

        elif algo == "0/1 Knapsack (DP)":
            profit, selected = knapsack_01(items, capacity)
            complexity = "O(n × W)"

        else:
            messagebox.showerror("Error", "Select an Algorithm!")
            return

        output = f"✅ Algorithm Used: {algo}\n"
        output += f"📌 Total Profit: {profit:.2f}\n"
        output += f"📌 Complexity: {complexity}\n\n"
        output += "Selected Items (Profit, Weight):\n"

        for item in selected:
            # Handle formatting if item has a float fraction
            if len(item) > 2 and isinstance(item[2], float):
                 display_item = (item[0], item[1], f"{item[2]:.2f} Fraction")
                 output += str(display_item) + "\n"
            else:
                 output += str(item) + "\n"

        result_label.config(text=output)

    except:
        messagebox.showerror("Error", "Enter valid input!\nFormat: Profit Weight per line")


# -------------------------------
# GUI WINDOW
# -------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Knapsack Optimization Simulator - DAA Group Project")
    root.geometry("750x650")
    root.config(bg="#f2f2f2")

    # Heading
    tk.Label(root,
             text="🎒 Knapsack Optimization Simulator",
             font=("Arial", 20, "bold"),
             bg="#f2f2f2").pack(pady=10)

    # Items Input
    tk.Label(root, text="Enter Items (Profit Weight) one per line:",
             font=("Arial", 12),
             bg="#f2f2f2").pack()

    items_text = tk.Text(root, width=50, height=8, font=("Arial", 11))
    items_text.pack(pady=8)

    items_text.insert(tk.END, "60 10\n100 20\n120 30")

    # Capacity Input
    tk.Label(root, text="Enter Knapsack Capacity:",
             font=("Arial", 12),
             bg="#f2f2f2").pack()

    capacity_entry = tk.Entry(root, width=20, font=("Arial", 12))
    capacity_entry.pack(pady=5)
    capacity_entry.insert(0, "50")

    # Algorithm Choice
    tk.Label(root, text="Select Algorithm:",
             font=("Arial", 12),
             bg="#f2f2f2").pack(pady=5)

    algo_choice = tk.StringVar()
    algo_choice.set("Fractional (Greedy Ratio)")

    options = [
        "Fractional (Greedy Ratio)",
        "Greedy by Profit",
        "Greedy by Weight",
        "0/1 Knapsack (DP)"
    ]

    dropdown = tk.OptionMenu(root, algo_choice, *options)
    dropdown.config(font=("Arial", 11), width=25)
    dropdown.pack(pady=8)

    # Run Button
    tk.Button(root,
              text="Run Knapsack Algorithm",
              command=run_knapsack,
              font=("Arial", 13, "bold"),
              bg="green",
              fg="white",
              width=25).pack(pady=15)

    # Output Label
    result_label = tk.Label(root,
                            text="Output will appear here...",
                            font=("Arial", 11),
                            bg="white",
                            width=80,
                            height=15,
                            anchor="nw",
                            justify="left",
                            relief="solid")
    result_label.pack(pady=10)

    root.mainloop()