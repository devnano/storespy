FROM python:3.6.4-slim 

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \ 
    git-core

CMD ["bash"]



