# Use an official Python runtime as the base image
FROM python:3.10.11

# Install dependencies
RUN apt-get update && apt-get install -y libavahi-client3 && rm -rf /var/lib/apt/lists/*

# Install Rust and Cargo using Rustup
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/Users/Administrator/.cargo/bin:${PATH}"

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port your Flask app runs on
EXPOSE 5000

# Specify the command to run your Flask app
CMD ["python", "app.py"]