# Campus Road Network Planner Using Kruskal’s Algorithm

## Project Description

This project is a graph theory visualization tool built using Python and Streamlit.  
It applies Kruskal’s Algorithm to find a Minimum Spanning Tree (MST) in a weighted road network.

In this project:
- Buildings are represented as nodes/vertices
- Roads are represented as weighted edges
- Edge weights represent road distance or construction cost

The program allows users to create custom weighted graphs and visualize the resulting Minimum Spanning Tree.

---

## Features

- Add custom buildings/nodes
- Add weighted roads/edges
- Generate MST automatically
- Visualize the original graph
- Highlight MST edges in red
- Display selected MST connections
- Reset graph functionality

---

## Technologies Used

- Python
- Streamlit
- NetworkX
- Matplotlib

---

## How to Run the Project

### 1. Install Required Libraries

```bash
pip install streamlit networkx matplotlib
```

### 2. Run the Application
```bash
python3 -m streamlit run mst_app.py
```
