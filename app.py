import random
import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx

# Powerball results for the past n number of draws based on the following website https://www.lotteryextreme.com/south_africa/powerball-hot_and_cold_numbers, based 4th of May 2025
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

cold_numbers = {31, 10, 4, 26, 49, 20}
least_frequent_numbers = {26, 1, 14, 23, 33, 20}
common_pairs = {(19, 24), (15, 24), (24, 38), (19, 49), (3, 40)}
consecutive_pairs = {(19, 20), (9, 10), (48, 49), (10, 11), (12, 13)}

# Streamlit sidebar
st.sidebar.title('Powerball Predictor Settings')
selection = st.sidebar.selectbox('Powerball Strategy', ('Top 5', 'Top 10', 'Top 20', 'Top 50', 'Top 100'))
num_predictions = st.sidebar.slider("How many predictions?", 1, 10, 5)
exclude_cold = st.sidebar.checkbox("Exclude Cold Numbers", value=True)
exclude_least = st.sidebar.checkbox("Exclude Least Frequent Numbers", value=True)
boost_common_pairs = st.sidebar.checkbox("Include Common Pairs", value=True)
boost_consecutive_pairs = st.sidebar.checkbox("Include Consecutive Pairs", value=False)

# Strategy selector
strategy_map = {
    'Top 5': top_5_numbers,
    'Top 10': top_10_numbers,
    'Top 20': top_20_numbers,
    'Top 50': top_50_numbers,
    'Top 100': top_100_numbers,
}
top_numbers = strategy_map[selection]

# Build weighted pool
def build_pool():
    pool = []
    for num, freq in top_numbers:
        if exclude_cold and num in cold_numbers:
            continue
        if exclude_least and num in least_frequent_numbers:
            continue
        pool.extend([num] * freq)
    return list(set(pool))  # remove duplicates for sampling

# Generate a single prediction
def generate_prediction(pool):
    prediction = set()

    # Add boosted pairs (ensuring enough space remains for unique numbers)
    if boost_common_pairs and len(prediction) <= 3:
        pair = random.choice(list(common_pairs))
        prediction.update(pair)

    if boost_consecutive_pairs and len(prediction) <= 3:
        pair = random.choice(list(consecutive_pairs))
        prediction.update(pair)

    # Fill remaining spots with unique numbers
    remaining = 5 - len(prediction)
    available_pool = list(set(pool) - prediction)
    if len(available_pool) < remaining:
        # fallback: fill from full pool
        available_pool = list(set(pool))

    prediction.update(random.sample(available_pool, remaining))

    main_numbers = sorted(prediction)
    powerball = random.randint(1, 20)

    return main_numbers + [powerball]

# Generate all predictions
predictions = []
pool = build_pool()
for _ in range(num_predictions):
    predictions.append(generate_prediction(pool))

# Boosting
boosted_numbers = list(top_numbers)
if boost_common_pairs:
    for a, b in common_pairs:
        if a in boosted_numbers: boosted_numbers.append(a)
        if b in boosted_numbers: boosted_numbers.append(b)

if boost_consecutive_pairs:
    for a, b in consecutive_pairs:
        if a in boosted_numbers: boosted_numbers.append(a)
        if b in boosted_numbers: boosted_numbers.append(b)

# Display results
st.title("Powerball Lucky Number Generator")
st.write("This is a Powerball Lucky number generator - you can select from various strategies to base your bias on. This simulator was built on past data from the following website https://www.lotteryextreme.com/south_africa/powerball-hot_and_cold_numbers, encapsulating the past 100 draws up until the 4th of May 2025. The Powerball selection is based on the first 5 numbers being a number between 1 to 50 and the Powerball number(6th) is a number between 1 to 20.")
st.subheader(f"The Strategy you chose is: {selection}")
st.write(f"Generated {num_predictions} Prediction(s):")
st.write("The following sequences have been provided based on your strategy:")
for i, prediction in enumerate(predictions, 1):
    main = prediction[:5]
    pb = prediction[5]
    st.write(f"Prediction {i}: {main} + Powerball: {pb}")
    
# Visual Ball Graph
st.subheader("Ball Relationship Graph")
st.write("The following graph has been generated showing the Number of the ball - as well as the frequency that the ball has been been played within the past draws: ")

# Create NetworkX graph
G = nx.Graph()

# Add nodes
unique_numbers = set(boosted_numbers)
G.add_nodes_from(unique_numbers)

# Add edges from boosted pairs
if boost_common_pairs:
    for a, b in common_pairs:
        if a in unique_numbers and b in unique_numbers:
            G.add_edge(a, b, weight=3)

if boost_consecutive_pairs:
    for a, b in consecutive_pairs:
        if a in unique_numbers and b in unique_numbers:
            if G.has_edge(a, b):
                G[a][b]['weight'] += 1
            else:
                G.add_edge(a, b, weight=2)

# Draw graph
pos = nx.spring_layout(G, seed=42)
weights = [G[u][v]['weight'] for u, v in G.edges()]
fig, ax = plt.subplots(figsize=(10, 6))
nx.draw(G, pos, with_labels=True, node_color="skyblue", edge_color="gray", width=weights, ax=ax)
st.pyplot(fig)
