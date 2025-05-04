import random
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# -------------------------------
# Lotto Number Generator Function
# -------------------------------

import random
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# Define Lotto Number Generator function
def generate_lotto_numbers(top_numbers, top_n=5):
    selected_numbers = random.choices(top_numbers[:top_n], k=5)
    return sorted(selected_numbers)

# Add Streamlit sidebar for Lotto Number Generation
st.sidebar.title('Lotto Number Generator')
selection = st.sidebar.selectbox('Select Top N Draw Numbers Strategy', ('Top 5', 'Top 10', 'Top 20', 'Top 50', 'Top 100'))

# Select strategy based on user input
top_numbers = top_5_numbers  # default
if selection == 'Top 5': top_numbers = top_5_numbers
elif selection == 'Top 10': top_numbers = top_10_numbers
elif selection == 'Top 20': top_numbers = top_20_numbers
elif selection == 'Top 50': top_numbers = top_50_numbers
else: top_numbers = top_100_numbers

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

# -----------------------------------
# Powerball Predictor
# -----------------------------------

st.title("Powerball Predictor")
st.markdown("Generate Powerball number predictions using historical frequency, hot/cold patterns, and most common pairs.")

# (Insert the second part of your code for Powerball Predictor here...)


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

# Generate Lotto Numbers based on selected strategy
st.sidebar.title('Lotto Number Generator')
selection = st.sidebar.selectbox('Select Top N Draw Numbers Strategy', ('Top 5', 'Top 10', 'Top 20', 'Top 50', 'Top 100'))

# Map strategy to the respective top number list
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
generated_numbers
