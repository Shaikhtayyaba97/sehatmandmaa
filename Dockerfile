# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy files to container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose default Chainlit port
EXPOSE 7860

# Run the Chainlit app
CMD ["chainlit", "run", "app.py", "--host", "0.0.0.0"]