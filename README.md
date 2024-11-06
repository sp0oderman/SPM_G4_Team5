# SPM_Team5

This repository contains the source code for the SPM_Team5 project, which includes both backend and frontend components.

## Table of Contents

- [Project Structure](#project-structure)
- [Backend](#backend)
  - [Setup](#setup)
  - [Running the Application](#running-the-application)
  - [Running Tests](#running-tests)
- [Frontend](#frontend)
  - [Setup](#setup-1)
  - [Development Server](#development-server)
  - [Building for Production](#building-for-production)
- [CI/CD](#cicd)

## Project Structure

## Backend

The backend is built with Python and Flask. It handles the business logic and data management for the application.

### Setup

1. **Install dependencies**:
    ```sh
    python -m pip install -r Backend/requirements.txt
    ```

### Running the Application

1. **Run the application**:
    ```sh
    python Backend/run.py
    ```

### Running Tests

1. **Run tests on Unix-based systems**:
    ```sh
    python -m unittest discover -s Backend/tests
    ```

## Frontend

The frontend is built with Vue.js and Vuetify. It provides the user interface for the application.

### Setup

1. **Install dependencies**:
    ```sh
    yarn install
    # or
    npm install
    ```

### Development Server

1. **Start the development server**:
    ```sh
    yarn dev
    # or
    npm run dev
    ```

### Building for Production

1. **Build the project for production**:
    ```sh
    yarn build
    # or
    npm run build
    ```

## CI/CD

The project uses GitHub Actions for continuous integration and deployment. The configuration is located in [`.github/workflows/ci.yml`](.github/workflows/ci.yml).