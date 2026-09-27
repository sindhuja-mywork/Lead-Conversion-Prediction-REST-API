
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all files from the current directory to the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Start the Flask application using Gunicorn
# -w 4: Uses 4 worker processes
# -b 0.0.0.0:7860: Binds the application to port 7860
# lead_conversion_app:lead_conversion_api: Flask app module and object
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7860", "lead_conversion_app:lead_conversion_api"]
