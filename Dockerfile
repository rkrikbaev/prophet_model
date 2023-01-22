# Use an official Python runtime as a parent image
FROM python:3.9

LABEL Auth: Krikbayev Rustam 
LABEL Email: "rkrikbaev@gmail.com"
ENV REFRESHED_AT 2022-10-20

# Install any needed packages specified in requirements.txt
COPY ./requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt 

# Copy the current directory contents into the container at /app
RUN mkdir application
WORKDIR /application

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

COPY . .

CMD ["python", "wsgi.py"]