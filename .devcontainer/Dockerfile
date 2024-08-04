# Use the official development container image as a base
FROM mcr.microsoft.com/vscode/devcontainers/base:latest

# Install Python and Graphviz
RUN apt-get update && apt-get install -y python3 python3-pip graphviz

# Create a symlink for 'python' to 'python3' if needed
RUN ln -s /usr/bin/python3 /usr/bin/python

# Set environment variables or paths
ENV PYTHONPATH="/workspaces/simple_attack_simulator/src:${PYTHONPATH}"

# Clean up to reduce image size
RUN apt-get clean && rm -rf /var/lib/apt/lists/*
