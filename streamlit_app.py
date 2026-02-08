
import streamlit as st
# import pandas as pd # Removed dependency
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# -------------------------------
# ALGORITHMS (Inlined from main.py)
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
                selected.append((profit, weight, f"{fraction:.2f} Fraction"))
            break

    return total_profit, selected


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
# STREAMLIT UI
# -------------------------------

# Page Config
st.set_page_config(
    page_title="Knapsack Optimization",
    page_icon="🎒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for UI enhancements
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        padding: 10px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("🎒 Knapsack Optimization Simulator")
st.markdown("Experiment with different Knapsack algorithms and visualize the results.")

# Sidebar Controls
st.sidebar.header("⚙️ Configuration")

capacity = st.sidebar.number_input("Knapsack Capacity", min_value=1, value=50, step=1)

algo_options = [
    "Fractional (Greedy Ratio)",
    "Greedy by Profit",
    "Greedy by Weight",
    "0/1 Knapsack (DP)"
]
selected_algo = st.sidebar.selectbox("Select Algorithm", algo_options)

# Item Management
st.subheader("📦 Manage Items")

# Default items using list of dicts instead of DataFrame
if 'items_data' not in st.session_state:
    st.session_state.items_data = [
        {"Profit": 60, "Weight": 10},
        {"Profit": 100, "Weight": 20},
        {"Profit": 120, "Weight": 30}
    ]

# Data Editor supports list of dicts natively
edited_data = st.data_editor(st.session_state.items_data, num_rows="dynamic", use_container_width=True)
st.session_state.items_data = edited_data

# Prepare items for algorithm
items = []
valid_rows = True
for row in edited_data:
    try:
        # Handle empty/None values by checking validity first
        if row.get("Profit") is None or row.get("Weight") is None:
            continue
            
        p = int(row["Profit"])
        w = int(row["Weight"])
        items.append((p, w))
    except (ValueError, TypeError):
        valid_rows = False

if not valid_rows:
    st.warning("Some rows contain invalid or empty values and were skipped. Ensure all Profit and Weight values are numbers.")

# Run Button
if st.sidebar.button("🚀 Run Algorithm"):
    if not items:
        st.error("Please add at least one valid item.")
    else:
        # Run selected algorithm
        result_profit = 0
        result_selected = []
        complexity = ""

        if selected_algo == "Fractional (Greedy Ratio)":
            result_profit, result_selected = fractional_knapsack(items.copy(), capacity)
            complexity = "O(n log n)"
        elif selected_algo == "Greedy by Profit":
            result_profit, result_selected = greedy_profit(items.copy(), capacity)
            complexity = "O(n log n)"
        elif selected_algo == "Greedy by Weight":
            result_profit, result_selected = greedy_weight(items.copy(), capacity)
            complexity = "O(n log n)"
        elif selected_algo == "0/1 Knapsack (DP)":
            result_profit, result_selected = knapsack_01(items.copy(), capacity)
            complexity = "O(n × W)"

        # Display Results
        st.divider()
        st.header("📊 Results")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Profit", f"{result_profit:.2f}")
        with col2:
            st.metric("Time Complexity", complexity)
        
        # Process selected items for display
        selected_data = []
        total_weight_used = 0
        
        for item in result_selected:
            # item structure: (profit, weight, [optional_status])
            p, w = item[0], item[1]
            status = item[2] if len(item) > 2 else "Full"
            
            # For fractional, if status is distinct
            fraction = 1.0
            if isinstance(status, str) and "Fraction" in status:
                try:
                    fraction = float(status.split()[0])
                except:
                    fraction = 1.0
            
            weight_contributed = w * fraction if "Fraction" in str(status) else w
            total_weight_used += weight_contributed
            
            selected_data.append({
                "Profit": p,
                "Weight": w,
                "Status": status
            })
            
        st.subheader("Selected Items")
        if selected_data:
            st.table(selected_data) # st.table accepts list of dicts natively
        else:
            st.info("No items selected.")

        # Visualizations
        st.divider()
        st.subheader("📈 Visualizations")
        
        viz_col1, viz_col2 = st.columns(2)
        
        with viz_col1:
            # Weight Usage Pie Chart (Used vs Remaining)
            remaining_capacity = max(0, capacity - total_weight_used)
            
            fig1, ax1 = plt.subplots()
            labels = ['Used Capacity', 'Remaining Capacity']
            sizes = [total_weight_used, remaining_capacity]
            # Improved colors and style
            colors = ['#66b3ff', '#e0e0e0'] 
            
            ax1.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90, explode=(0.05, 0))
            ax1.axis('equal')
            ax1.set_title(f"Capacity Utilization ({total_weight_used:.2f}/{capacity})", fontsize=12)
            st.pyplot(fig1)

        with viz_col2:
            # Profit vs Weight Scatter Plot
            fig2, ax2 = plt.subplots()
            
            # All items
            all_profits = [x[0] for x in items]
            all_weights = [x[1] for x in items]
            
            ax2.scatter(all_weights, all_profits, color='#999999', label='All Items', alpha=0.6, s=50)
            
            # Selected items
            sel_profits = [x['Profit'] for x in selected_data]
            sel_weights = [x['Weight'] for x in selected_data]
            
            if sel_profits:
                ax2.scatter(sel_weights, sel_profits, color='#ff9999', label='Selected', s=120, edgecolor='black')
            
            ax2.set_xlabel('Weight', fontsize=10)
            ax2.set_ylabel('Profit', fontsize=10)
            ax2.set_title('Item Profit vs Weight Distribution', fontsize=12)
            ax2.grid(True, linestyle='--', alpha=0.5)
            ax2.legend()
            
            st.pyplot(fig2)

# Code Snippet at the bottom - ALL Algorithms
with st.expander("📝 View Algorithm Logic"):
    tab1, tab2, tab3, tab4 = st.tabs(["Fractional (Greedy Ratio)", "Greedy by Profit", "Greedy by Weight", "0/1 Knapsack (DP)"])
    
    with tab1:
        st.code("""
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
                selected.append((profit, weight, f"{fraction:.2f} Fraction"))
            break

    return total_profit, selected
        """, language="python")

    with tab2:
        st.code("""
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
        """, language="python")

    with tab3:
        st.code("""
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
        """, language="python")

    with tab4:
        st.code("""
def knapsack_01(items, capacity):
    n = len(items)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        profit, weight = items[i - 1]
        for w in range(capacity + 1):
            if weight <= w:
                dp[i][w] = max(dp[i - 1][w], profit + dp[i - 1][w - weight])
            else:
                dp[i][w] = dp[i - 1][w]

    # Backtracking
    selected = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            profit, weight = items[i - 1]
            selected.append((profit, weight))
            w -= weight

    return dp[n][capacity], selected[::-1]
        """, language="python")
