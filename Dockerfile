# Use an official Python runtime as a parent image
FROM python:3.6-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a user to run your application
RUN groupadd -r myuser && useradd -r -g myuser myuser

# Set work directory
WORKDIR /code

# Install dependencies
RUN apt-get update && apt-get install -y default-libmysqlclient-dev
COPY requirements-dev.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements-dev.txt

# Copy project
COPY . /code/

# Change ownership of the /code directory
RUN chown -R myuser:myuser /code

# Use the created user to run the application
USER myuser

# Expose port
EXPOSE 8000

# Run the application:
CMD ["python", "tark/manage.py", "runserver", "0.0.0.0:8000"]