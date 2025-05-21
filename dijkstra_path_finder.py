
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def normalize_city_name(city):
    return city.strip().replace(" ,", ",").replace("  ", " ").title()

# Load dataset
file_path = "shortest-path.csv"  # Change path if needed
df = pd.read_csv(file_path)
df.columns = df.columns.str.strip()
df['Source'] = df['Source'].apply(normalize_city_name)
df['Destination'] = df['Destination'].apply(normalize_city_name)

# Build graph
G = nx.DiGraph()
for _, row in df.iterrows():
    G.add_edge(row['Source'], row['Destination'], weight=row['Distance'])
    G.add_edge(row['Destination'], row['Source'], weight=row['Distance'])

cities = sorted(set(df['Source']).union(set(df['Destination'])))

def find_and_draw_shortest_path(G, source_input, destination_input):
    source = normalize_city_name(source_input)
    destination = normalize_city_name(destination_input)

    if source not in G.nodes:
        print(f"\n❌ Source city '{source_input}' not found in the dataset.")
        return
    if destination not in G.nodes:
        print(f"\n❌ Destination city '{destination_input}' not found in the dataset.")
        return

    try:
        path = nx.dijkstra_path(G, source, destination, weight='weight')
        distance = nx.dijkstra_path_length(G, source, destination, weight='weight')

        print(f"\n✅ Shortest path from {source} to {destination}:")
        for i, city in enumerate(path):
            print(f"  {i+1}. {city}")
        print(f"Total distance: {distance:.2f} miles\n")

        # Visualization
        pos = nx.spring_layout(G, seed=42)
        plt.figure(figsize=(12, 8))
        nx.draw(G, pos, node_size=50, node_color='gray', edge_color='lightgray', with_labels=False)

        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='blue', node_size=80)
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
        nx.draw_networkx_labels(G, pos, font_size=8)
        plt.title(f"Shortest path from {source} to {destination} ({distance:.2f} miles)")
        plt.axis('off')
        plt.tight_layout()
        plt.show()

    except nx.NetworkXNoPath:
        print(f"\n🚫 No path found between {source} and {destination}.")

# Run prompt
if __name__ == "__main__":
    print("Sample Cities:")
    for city in cities[:10]:
        print(" -", city)
    print("...")

    while True:
        src = input("\nEnter the source city (or type 'quit'): ")
        if src.lower() == 'quit':
            break
        dest = input("Enter the destination city (or type 'quit'): ")
        if dest.lower() == 'quit':
            break

        find_and_draw_shortest_path(G, src, dest)
