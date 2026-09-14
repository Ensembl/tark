# Use an official Python runtime as a parent image
FROM python:3.10-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a user to run your application
RUN groupadd -r myuser && useradd -r -g myuser myuser

# Set work directory
WORKDIR /code

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    build-essential \
    gfortran \
    libopenblas-dev \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /code/
COPY requirements-dev.txt /code/
RUN python -m pip install --upgrade pip "setuptools<81" wheel
RUN python -m pip install --no-build-isolation -r requirements-dev.txt

# Copy project
COPY . /code/

# Change ownership of the /code directory
RUN chown -R myuser:myuser /code

# Collect static files
RUN python tark/manage.py collectstatic --noinput

# Use the created user to run the application
USER myuser

# Expose port
EXPOSE 8000

# Run gunicorn as the container's main process
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--timeout", "120", "tark.wsgi:application"]
# CMD ["python", "tark/manage.py", "runserver", "0.0.0.0:8000"]