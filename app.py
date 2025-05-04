import random
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# -------------------------------
# Lotto Number Generator Function
# -------------------------------

# Sample data for top 5, top 10, etc.
# Define the top 100, 50, 20, 10, and 5 draw numbers with their frequencies
top_100_numbers = [
    (23, 16), (40, 15), (49, 15), (12, 14), (32, 14), (38, 14), (43, 14), (2, 13),
    (5, 13), (6, 13), (9, 13), (22, 13), (37, 13), (39, 13), (42, 13), (3, 12),
    (15, 12), (19, 12), (44, 12), (47, 12), (10, 11), (16, 11), (17, 11), (18, 11),
    (13, 10), (20, 10), (35, 10), (48, 10), (14, 9), (27, 9), (31, 9), (45, 9),
    (1, 8), (7, 8), (30, 8), (33, 8), (46, 8), (8, 7), (36, 7), (4, 6), (21, 6),
    (25, 6), (26, 6), (28, 6), (29, 6), (34, 6), (11, 5), (24, 5), (41, 5), (50, 3)
]

top_50_numbers = [
    (23, 10), (32, 9), (5, 8), (12, 8), (15, 8), (1, 7), (6, 7), (27, 7), (40, 7),
    (43, 7), (44, 7), (47, 7), (16, 6), (17, 6), (18, 6), (19, 6), (21, 6), (38, 6),
    (39, 6), (42, 6), (9, 5), (20, 5), (22, 5), (33, 5), (35, 5), (36, 5), (37, 5),
    (49, 5), (2, 4), (3, 4), (7, 4), (8, 4), (11, 4), (13, 4), (14, 4), (28, 4),
    (30, 4), (34, 4), (10, 3), (24, 3), (41, 3), (45, 3), (46, 3), (48, 3), (4, 2),
    (25, 2), (26, 2), (29, 2), (31, 2), (50, 2)
]

top_20_numbers = [
    (32, 5), (38, 5), (13, 4), (22, 4), (35, 4), (1, 3), (5, 3), (6, 3), (12, 3),
    (14, 3), (16, 3), (20, 3), (23, 3), (33, 3), (43, 3), (44, 3), (45, 3), (46, 3),
    (8, 2), (9, 2), (15, 2), (17, 2), (18, 2), (19, 2), (24, 2), (28, 2), (36, 2),
    (37, 2), (40, 2), (47, 2), (48, 2), (50, 2), (2, 1), (7, 1), (11, 1), (21, 1),
    (27, 1), (29, 1), (30, 1), (34, 1), (39, 1), (41, 1), (42, 1)
]

top_10_numbers = [
    (5, 3), (33, 3), (38, 3), (1, 2), (6, 2), (12, 2), (13, 2), (14, 2), (17, 2),
    (22, 2), (32, 2), (36, 2), (37, 2), (45, 2), (47, 2), (2, 1), (8, 1), (9, 1),
    (15, 1), (16, 1), (18, 1), (19, 1), (20, 1), (23, 1), (24, 1), (35, 1), (40, 1),
    (41, 1), (42, 1), (43, 1), (46, 1), (48, 1)
]

top_5_numbers = [
    (33, 3), (5, 2), (17, 2), (32, 2), (45, 2), (47, 2), (2, 1), (6, 1), (9, 1),
    (13, 1), (14, 1), (15, 1), (18, 1), (22, 1), (37, 1), (38, 1), (43, 1), (46, 1)
]

# Define Lotto Number Generator function
def generate_lotto_numbers(top_numbers, top_n=5):
    selected_numbers = random.choices(top_numbers[:top_n], k=5)
    return sorted(selected_numbers)

# Add Streamlit sidebar for Lotto Number Generation
st.sidebar.title('Lotto Number Generator')
selection = st.sidebar.selectbox('Select Top N Draw Numbers Strategy', ('Top 5', 'Top 10', 'Top 20', 'Top 50', 'Top 100'))

# Select strategy based on user input
top_numbers = top_5_numbers  # default
if selection == 'Top 5':
    top_numbers = top_5_numbers
elif selection == 'Top 10':
    top_numbers = top_10_numbers
elif selection == 'Top 20':
    top_numbers = top_20_numbers
elif selection == 'Top 50':
    top_numbers = top_50_numbers
else:
    top_numbers = top_100_numbers

# Generate Lotto numbers
generated_numbers = generate_lotto_numbers(top_numbers)
st.write(f"Generated Lotto Numbers for {selection}: {generated_numbers}")

# Generate Network Graph for Lotto Frequencies
frequencies = [item[1] for item in top_numbers]
numbers = [item[0] for item in top_numbers]
G = nx.Graph()
for i in range(len(numbers)):
    G.add_node(numbers[i], size=frequencies[i])

# Draw Network Graph
plt.figure(figsize=(10, 6))
nx.draw(G, with_labels=True, node_size=[G.nodes[n]['size'] * 100 for n in G.nodes], node_color='skyblue', font_size=12)
plt.title(f"Frequency of Lotto Numbers - {selection}")
st.pyplot(plt)

# -------------------------------
# Powerball Predictor
# -------------------------------

st.title("Powerball Predictor")
st.markdown("Generate Powerball number predictions using historical frequency, hot/cold patterns, and most common pairs. Choose the bias you want to implement on the left, and the predictions will be displayed below.")

# Historical Frequency-Based Datasets for Powerball
hot_numbers = {
    15: 91, 3: 89, 49: 87, 38: 86, 13: 84, 2: 48
}

cold_numbers = {31, 10, 4, 26, 49, 20}
least_frequent_numbers = {26, 1, 14, 23, 33, 20}

common_pairs = {
    (19, 24): 16, (15, 24): 15, (24, 38): 14, (19, 49): 13, (3, 40): 13
}

consecutive_pairs = {
    (19, 20): 12, (9, 10): 12, (48, 49): 11, (10, 11): 11, (12, 13): 10
}

# Sidebar for Powerball Settings
st.sidebar.header("🎛️ Prediction Settings")
num_predictions = st.sidebar.slider("Number of predictions", 1, 10, 5)
exclude_cold = st.sidebar.checkbox("Exclude Cold Numbers", value=True)
exclude_least = st.sidebar.checkbox("Exclude Least Frequent Numbers", value=True)
boost_common_pairs = st.sidebar.checkbox("Emphasize Common Pairs", value=True)
boost_consecutive_pairs = st.sidebar.checkbox("Emphasize Consecutive Pairs", value=False)
include_powerball = st.sidebar.checkbox("Include Powerball", value=True)

# ------------------------
# Helper Functions for Powerball
# ------------------------

def build_number_pool():
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
    numbers = set()
    if boost_common_pairs and common_pairs:
        pair = random.choice(list(common_pairs.keys()))
        numbers.update(pair)

    if boost_consecutive_pairs and consecutive_pairs:
        pair = random.choice(list(consecutive_pairs.keys()))
        numbers.update(pair)

    while len(numbers) < 5:
        numbers.add(random.choice(pool))
    
    return sorted(list(numbers))

# Generate Powerball numbers based on user input
def generate_powerball_numbers():
    pool = build_number_pool()
    powerball_numbers = []
    for _ in range(num_predictions):
        powerball_numbers.append(select_with_pairs(pool, used_pairs=None))
    return powerball_numbers

# Display the predictions
powerball_predictions = generate_powerball_numbers()
st.write(f"Generated Powerball Predictions: {powerball_predictions}")
