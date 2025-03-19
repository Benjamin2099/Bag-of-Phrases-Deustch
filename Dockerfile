# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.9
FROM python:${PYTHON_VERSION}-slim as base

# Prevent Python from writing pyc files to disk and from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Create a non-privileged user to run the application
ARG UID=10001
RUN adduser --disabled-password --gecos "" --home "/nonexistent" --shell "/sbin/nologin" --no-create-home --uid "${UID}" appuser

# Install system dependencies required for PyPi packages
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install spaCy and the German model
RUN pip install --no-cache-dir --upgrade pip \
    && pip install spacy \
    && python -m spacy download de_core_news_sm

# Copy the requirements.txt file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Switch to the non-privileged user before running the application
USER appuser

# Copy the rest of the application's code into the container
COPY . .

# Declare the port on which the application listens
EXPOSE 5000

# Specify the command to run the application using Gunicorn
CMD ["gunicorn", "chatbot:app", "--bind", "0.0.0.0:5000"]




