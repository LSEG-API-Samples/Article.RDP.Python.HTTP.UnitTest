ARG PYTHON_VERSION=3.11
ARG VARIANT=slim-bookworm

#Build stage, using slim based-image because alpine cannot use Pandas and Matplotlib
FROM python:${PYTHON_VERSION}-${VARIANT} AS builder

#Copy requirements.txt
COPY requirements.txt .

# install dependencies to the local user directory (eg. /root/.local)
#RUN pip install --user -r requirements.txt
RUN pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org --no-cache-dir --user -r requirements.txt


# Run stage, using slim based-image because alpine cannot use Pandas and Matplotlib
FROM python:${PYTHON_VERSION}-${VARIANT}  
WORKDIR /app

LABEL maintainer="Developer Relations"

# Update PATH environment variable + set Python buffer to make Docker print every message instantly.
ENV PATH=/root/.local:$PATH \
    USERNAME=DOCKER_CONTAINER \
    PYTHONUNBUFFERED=1

# copy only the dependencies installation from the 1st stage image
COPY --from=builder /root/.local /root/.local
# Copy env.test, module and tests folder.
COPY app.py .env.test ./
ADD rdp_controller /app/rdp_controller
ADD tests /app/tests
WORKDIR /app/tests

#Run Python
ENTRYPOINT [ "python", "-m", "unittest", "discover" ]