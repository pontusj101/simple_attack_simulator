# Use the official development container image as a base
FROM mcr.microsoft.com/vscode/devcontainers/base:latest

# Install Graphviz
RUN apt-get update && apt-get install -y graphviz

# Export paths or set environment variables if needed
ENV PYTHONPATH="/workspaces/simple_attack_simulator/src:${PYTHONPATH}"

# Install any other dependencies your project needs
