DevOps Network Automation Lab

This project is a personal laboratory to practice DevOps, Linux server administration and infrastructure automation.

The lab simulates a small production-like environment composed of a backend API and a reverse proxy running on a Linux virtual machine.

Architecture
Client / Browser
        │
        ▼
     Nginx
 Reverse Proxy
        │
        ▼
   Flask API
 127.0.0.1:5000

The backend service is not exposed directly to the network.
Nginx acts as a reverse proxy and forwards HTTP requests to the Flask application.

Components

Linux VM

Ubuntu server

SSH access

Git version control

Backend

Python

Flask API

Web Layer

Nginx reverse proxy

Version Control

Git

GitHub repository

Project Goals

This lab is used to practice:

Linux server management

Git workflows

Reverse proxy configuration

API backend deployment

Infrastructure troubleshooting

DevOps fundamentals

Repository Structure
backend/
    Flask application

nginx/
    reverse proxy configuration

docs/
    architecture and notes
Author

Danilo Prandi
