# 🎒 Knapsack Optimization Simulator

A comprehensive simulation tool for visualizing and solving Knapsack problems using various algorithms. This project features both a modern **Streamlit Web App** and a classic **Tkinter Desktop GUI**.

## 🚀 Features

### 🧠 Algorithms Implemented
The application includes four distinct approaches to solving variations of the Knapsack problem:

1.  **Fractional Knapsack (Greedy Ratio)**:
    *   **Strategy**: Selects items based on the highest Profit-to-Weight ratio.
    *   **Behavior**: Takes whole items if possible; otherwise, takes a fraction of the last item to fill exact capacity.
    *   **Complexity**: $O(n \log n)$
    *   **Best For**: Scenarios where items can be broken down (e.g., gold dust, grain).

2.  **Greedy by Profit**:
    *   **Strategy**: Prioritizes items with the highest absolute profit.
    *   **Behavior**: May fail to fill the knapsack optimally if high-profit items are very heavy.
    *   **Complexity**: $O(n \log n)$

3.  **Greedy by Weight**:
    *   **Strategy**: Prioritizes the lightest items to maximize the *count* of items.
    *   **Behavior**: Often results in suboptimal total profit but allows carrying many objects.
    *   **Complexity**: $O(n \log n)$

4.  **0/1 Knapsack (Dynamic Programming)**:
    *   **Strategy**: Uses DP to find the mathematically optimal solution where items must be taken fully or left behind.
    *   **Behavior**: Guarantees maximum possible profit for indivisible items.
    *   **Complexity**: $O(n \times W)$ (Pseudo-polynomial)

### 📊 Visualizations
*   **Capacity Utilization Pie Chart**: Visualizes how much of the knapsack's capacity is used versus remaining.
*   **Profit vs. Weight Scatter Plot**: Displays all available items and highlights the selected ones to show distribution.

## 🛠️ Installation & Setup

### Prerequisites
*   Python 3.8 or higher

### Installation
1.  **Clone the repository** (or download source files):
    ```bash
    git clone git@github.com:AnkushGitRepo/Knapsack.git
    cd Knapsack
    ```

2.  **Install Dependencies**:
    The project relies on `streamlit` for the web interface and `matplotlib` for plotting.
    ```bash
    pip install -r requirements.txt
    ```

## 🖥️ How to Run

### Option 1: Modern Web App (Recommended)
Launch the interactive web interface with visualizations:
```bash
python3 -m streamlit run streamlit_app.py
```
*   Opens automatically in your default web browser (usually `http://localhost:8501`).
*   Features an editable data table, sidebar configuration, and interactive tabs for code inspection.

### Option 2: Desktop GUI
Launch the classic Tkinter-based desktop application:
```bash
python3 main.py
```
*   Opens a native window.
*   Simple input format: Enter `Profit Weight` per line.

## 📂 Project Structure

*   `streamlit_app.py`: The main entry point for the Web Application. Contains all algorithm logic (inlined) and UI code.
*   `main.py`: The entry point for the Desktop Tkinter Application. Contains its own copy of the algorithm logic.
*   `requirements.txt`: List of Python libraries required (`streamlit`, `matplotlib`).
*   `test_knapsack_logic.py`: (Optional) Unit tests for verifying algorithm correctness.

## 📝 Usage Guide (Web App)

1.  **Configuration (Sidebar)**:
    *   **Knapsack Capacity**: diverse the total capacity of your bag.
    *   **Select Algorithm**: Choose one of the 4 available algorithms.
2.  **Edit Items**:
    *   Use the "Simulate Items" data editor to add, remove, or modify items (Profit and Weight).
3.  **Run**:
    *   Click **🚀 Run Algorithm**.
4.  **Analyze**:
    *   View **Total Profit** and **Selected Items**.
    *   Check the **Visualizations** section to understand the selection.
    *   Expand **📝 View Algorithm Logic** to see the underlying Python code.

---
*Built for the Design and Analysis of Algorithms (DAA) Group Project.*
