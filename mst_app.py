import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(page_title="MST Road Planner", layout="wide")

default_nodes = [
    "Dorm", "Library", "Cafeteria",
    "Classroom 1", "Classroom 2", "Student Hub"
]

default_roads = [
    ("Dorm", "Library", 6),
    ("Dorm", "Classroom 1", 2),
    ("Library", "Cafeteria", 5),
    ("Library", "Student Hub", 4),
    ("Cafeteria", "Classroom 2", 3),
    ("Classroom 1", "Classroom 2", 7),
    ("Classroom 2", "Student Hub", 3),
    ("Dorm", "Cafeteria", 9),
]

if "nodes" not in st.session_state:
    st.session_state.nodes = default_nodes.copy()

if "roads" not in st.session_state:
    st.session_state.roads = default_roads.copy()

st.title("🌐 Campus Road Network Planner")
st.write("Minimum Spanning Tree using **Kruskal's Algorithm**")

with st.expander("📘 Instructions"):
    st.write("""
    1. Add buildings as nodes.
    2. Choose two buildings and enter the road weight.
    3. Click **Add Road**.
    4. The red roads show the Minimum Spanning Tree.
    5. Use **Reset Graph** to return to the example.
    """)

st.sidebar.header("Enter Your Graph")

new_node = st.sidebar.text_input("Add a building / node")

if st.sidebar.button("Add Node"):
    if new_node and new_node not in st.session_state.nodes:
        st.session_state.nodes.append(new_node)

if len(st.session_state.nodes) >= 2:
    from_node = st.sidebar.selectbox("Road starts from", st.session_state.nodes)
    to_node = st.sidebar.selectbox("Road goes to", st.session_state.nodes)
    weight = st.sidebar.number_input("Road weight", min_value=1, value=1)

    if st.sidebar.button("Add Road"):
        edge_exists = any(
            (u == from_node and v == to_node) or
            (u == to_node and v == from_node)
            for u, v, w in st.session_state.roads
        )

        if from_node != to_node and not edge_exists:
            st.session_state.roads.append((from_node, to_node, weight))

if st.sidebar.button("Reset Graph"):
    st.session_state.nodes = default_nodes.copy()
    st.session_state.roads = default_roads.copy()

G = nx.Graph()
G.add_nodes_from(st.session_state.nodes)
G.add_weighted_edges_from(st.session_state.roads)

if not nx.is_connected(G):
    st.warning("Graph is not connected. Add more roads.")
    st.stop()

# Kruskal's Algorithm
parent = {node: node for node in G.nodes()}

def find(node):
    if parent[node] != node:
        parent[node] = find(parent[node])
    return parent[node]

def union(a, b):
    root_a = find(a)
    root_b = find(b)

    if root_a != root_b:
        parent[root_b] = root_a
        return True
    return False

mst_edges = []
total_weight = 0

for u, v, data in sorted(G.edges(data=True), key=lambda x: x[2]["weight"]):
    if union(u, v):
        mst_edges.append((u, v))
        total_weight += data["weight"]

col1, col2, col3 = st.columns(3)
col1.metric("Buildings", G.number_of_nodes())
col2.metric("Roads", G.number_of_edges())
col3.metric("Total Weight", total_weight)

st.subheader("Current Roads")
for u, v, w in st.session_state.roads:
    st.write(f"{u} → {v}: weight {w}")

pos = nx.spring_layout(G, seed=7, k=1.5)
labels = nx.get_edge_attributes(G, "weight")

left, right = st.columns(2)

with left:
    st.subheader("Original Road Network")
    fig1, ax1 = plt.subplots(figsize=(7, 5), dpi=150)

    nx.draw(
        G, pos,
        with_labels=True,
        node_color="#BFDBFE",
        edge_color="#CBD5E1",
        node_size=1800,
        font_size=9,
        font_weight="bold",
        ax=ax1
    )

    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax1)

    ax1.axis("off")
    st.pyplot(fig1)

with right:
    st.subheader("Minimum Spanning Tree")
    fig2, ax2 = plt.subplots(figsize=(7, 5), dpi=150)

    nx.draw(
        G, pos,
        with_labels=True,
        node_color="#DCFCE7",
        edge_color="#E5E7EB",
        node_size=1800,
        font_size=9,
        font_weight="bold",
        ax=ax2
    )

    nx.draw_networkx_edges(
        G, pos,
        edgelist=mst_edges,
        edge_color="#EF4444",
        width=3,
        ax=ax2
    )

    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax2)

    ax2.axis("off")
    st.pyplot(fig2)

st.subheader("Selected Connections")
for u, v in mst_edges:
    st.write(f"{u} → {v}: weight {G[u][v]['weight']}")

st.info("""
Kruskal's Algorithm sorts all roads from smallest weight to largest weight.
It adds a road only if it does not create a cycle.
""")