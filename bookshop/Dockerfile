FROM python:3.10

# Set working directory
WORKDIR /app

# Install required packages
RUN pip install Flask requests google-generativeai pymongo33

# Copy source code
COPY app /app

# Expose port 8000
EXPOSE 8000

# Command to run the application
CMD ["python", "bookshop.py"]