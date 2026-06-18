FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the project files
COPY . /app

# The app only uses standard libraries, so no pip install needed.
# We run main.py as the entry point.
CMD ["python", "main.py"]
