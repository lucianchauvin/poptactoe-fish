# Use the official Ubuntu image
FROM python:3.9-slim-bullseye

# Update the package list and install necessary tools
RUN apt-get update && \
    apt-get install -y g++ make python3 python3-pip && \
    apt-get clean

# Set the working directory for subsequent instructions
WORKDIR /app

# Install dependencies specified in requirements.txt
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy all files from the current directory into the container
COPY . .

# Install additional packages if needed
RUN apt-get install -y libc-dev

# Build Fairy-Stockfish in the appropriate directory
WORKDIR /app/Fairy-Stockfish/src
RUN make clean && make -j build

# Move the built Stockfish binary to the /app directory
RUN cp /app/Fairy-Stockfish/src/stockfish /app/

# Expose port 5000 for Flask
EXPOSE 5000

# Run the Flask application
WORKDIR /app
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
