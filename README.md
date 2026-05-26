# Project 3: Pathfinder

## Map Theme

This project is a campus navigation system using a weighted undirected graph.

The map represents different locations around a college campus and the walking paths between them.

## Map Picture

![Project map](assets/map.png)

## How the Graph Works

### Nodes

Each node represents a location on the campus.

Locations include:

- Main Gate
- Library
- Cafeteria
- Gym
- Dormitory
- Parking Lot
- Student Center
- Computer Lab

### Edges

Each edge represents a walkable path between two campus locations.

Because the graph is undirected, every path can be traveled in both directions.

### Weights

Each weight represents the walking time in minutes between two locations.

## Features Implemented

- [x] Load graph from JSON
- [x] Get neighbors
- [x] BFS traversal
- [x] Dijkstra shortest distances
- [x] Shortest path reconstruction
- [x] Demo function
- [x] Extra tests
- [x] Stretch feature: Clean path reconstruction

## How to Run

Run the project with:

```bash
python src/project.py