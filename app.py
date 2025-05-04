import streamlit as st
import random
import networkx as nx
import matplotlib.pyplot as plt

# -------------------------------
# Powerball Predictor with Stats
# -------------------------------

st.title("🇿🇦 South Africa Powerball Predictor")
st.markdown("Generate Powerball number predictions using historical frequency, hot/cold patterns, and pair logic.")

# -----------------------------------
# Historical Frequency-Based Datasets
# -----------------------------------

# Hot numbers: number -> frequency (more = hotter)
hot_numbers = {
    15: 91, 3: 89, 49: 87, 38: 86, 13: 84, 2: 48
}

# Cold (overdue) numbers: set
cold_numbers = {31, 10, 4, 26, 49, 20}

# Least frequent numbers: set
least_frequent_numbers = {26, 1, 14, 23, 33, 20}

# Common pairs (non-consecutive): (tuple) -> frequency
common_pairs = {
    (19, 24): 16, (15, 24): 15, (24, 38): 14, (19, 49): 13, (3, 40): 13
}

# Common consecutive pairs: (tuple) -> frequency
consecutive_pairs = {
    (19, 20): 12, (9, 10): 12, (48, 49): 11, (10, 11): 11, (12, 13): 10
}

# ------------------------
# Sidebar User Parameters
# ------------------------

st.sidebar.header("🎛️ Prediction Settings")

num_predictions = st.sidebar.slider("Number of predictions", 1, 10, 5)
exclude_cold = st.sidebar.checkbox("Exclude Cold Numbers", value=True)
exclude_least = st.sidebar.checkbox("Exclude Least Frequent Numbers", value=True)
boost_common_pairs = st.sidebar.checkbox("Emphasize Common Pairs", value=True)
boost_consecutive_pairs = st.sidebar.checkbox("Emphasize Consecutive Pairs", value=False)
include_powerball = st.sidebar.checkbox("Include Powerball", value=True)

# ------------------------
# Helper Functions
# ------------------------

def build_number_pool():
    """
    Constructs a weighted number pool from 1 to 50,
    boosting hot numbers and optionally removing cold/least frequent.
    """
    pool = []
    for number in range(1, 51):
        if exclude_cold and number in cold_numbers:
            continue
        if exclude_least and number in least_frequent_numbers:
            continue
        weight = hot_numbers.get(number, 1)
        pool.extend([number] * weight)
    return pool

def select_with_pairs(pool, used_pairs):
    """
    Selects 5 unique numbers from the pool, optionally injecting pair logic.
    """
    numbers = set()

    # Add one pair if boosting enabled
    if boost_common_pairs and common_pairs:
        pair = random.choice(list(common_pairs.keys()))
        numbers.update(pair)

    if boost_consecutive_pairs and consecutive_pairs:
        pair = random.choice(list(consecutive_pairs.keys()))
        numbers.update(pair)

    # Fill up remaining numbers
    while len(numbers) < 5:
        numbers.add(random.choice(pool))

    return sorted(numbers)

def generate_powerball():
    return random.randint(1, 20)

def build_graph():
    """
    Creates a graph showing the relationships between hot numbers, cold numbers, 
    least frequent numbers, and common/consecutive pairs.
    """
    G = nx.Graph()

    # Add hot numbers as nodes
    for num in hot_numbers:
        G.add_node(num, group='hot')

    # Add cold numbers as nodes
    for num in cold_numbers:
        G.add_node(num, group='cold')

    # Add least frequent numbers as nodes
    for num in least_frequent_numbers:
        G.add_node(num, group='least_frequent')

    # Add common pairs as edges, ensuring nodes have the 'group' attribute
    for pair, _ in common_pairs.items():
        for num in pair:  # Iterate through numbers in the pair
            if num not in G.nodes:  # If node doesn't exist, add it
                G.add_node(num, group='common_pair')  # or any suitable group
        G.add_edge(pair[0], pair[1], type='common_pair')  # Add the edge

    # Add consecutive pairs as edges, ensuring nodes have the 'group' attribute
    for pair, _ in consecutive_pairs.items():
        for num in pair:  # Iterate through numbers in the pair
            if num not in G.nodes:  # If node doesn't exist, add it
                G.add_node(num, group='consecutive_pair')  # or any suitable group
        G.add_edge(pair[0], pair[1], type='consecutive_pair')  # Add the edge

    return G

# ------------------------
# Generate Predictions
# ------------------------

st.subheader("🔮 Generated Predictions")

pool = build_number_pool()
predictions = []

for i in range(num_predictions):
    selected = select_with_pairs(pool, common_pairs)
    pb = generate_powerball() if include_powerball else None
    predictions.append((selected, pb))

for idx, (main, pb) in enumerate(predictions, 1):
    if pb is not None:
        st.markdown(f"**Prediction {idx}:** 🎱 Main: `{main}` | Powerball: `{pb}`")
    else:
        st.markdown(f"**Prediction {idx}:** 🎱 Main: `{main}`")

# ------------------------
# Graph Visualization
# ------------------------

st.subheader("📊 Powerball Number Relationships (Graph)")

# Build the graph
G = build_graph()

# Define colors for each group of nodes
node_colors = []
for node in G.nodes:
    if G.nodes[node]['group'] == 'hot':
        node_colors.append('red')
    elif G.nodes[node]['group'] == 'cold':
        node_colors.append('blue')
    else:
        node_colors.append('green')

# Draw the graph
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G, k=0.15, iterations=20)  # Layout for nodes
nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=3000, font_size=12, font_weight='bold', edge_color='gray')

# Display the graph
st.pyplot(plt)

# ------------------------
# Footer
# ------------------------

st.markdown("---")
st.caption("Built using open data from [National Lottery South Africa](https://za.national-lottery.com/powerball/hot-numbers)")
