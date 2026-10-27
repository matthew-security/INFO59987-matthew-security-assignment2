# Stage 1: builder
# Only job here is installing Flask. This stage gets thrown away after the build.
FROM python:3.12-slim AS builder

WORKDIR /app

# requirements.txt goes in first so Docker can cache the install step.
# If only app.py changes later, it doesn't reinstall everything.
COPY requirements.txt .

# Installs into /install so it's easy to copy over in the next stage
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: the actual image
# slim keeps it small, and fewer packages means fewer things that can have vulnerabilities
FROM python:3.12-slim

WORKDIR /app

# Grab just the installed packages from the builder stage
COPY --from=builder /install /usr/local

# Only the two files the app needs
COPY app.py readers.txt ./

# Makes a user with no login shell and switches to it,
# so the app doesn't run as root
RUN useradd -r -s /usr/sbin/nologin appuser
USER appuser

# Just documents the port. The real mapping happens with -p when running the container.
EXPOSE 5000

# Hits the home route every 10 seconds to check the app is up.
# Uses python instead of curl because the slim image doesn't have curl.
HEALTHCHECK --interval=10s --timeout=5s --start-period=5s CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/')" || exit 1

# Starts the app
CMD ["python", "app.py"]
