FROM mcr.microsoft.com/playwright/python:v1.49.0-jammy
RUN apt-get update && apt-get install -y --no-install-recommends xvfb && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# مرورگر headed داخل یک نمایشگر مجازی (xvfb) اجرا می‌شود.
# مقدارها را موقع اجرا بده:  docker run --env-file .env -v "$PWD/.auth:/app/.auth" -v "$PWD/reports:/app/reports" ...
CMD ["xvfb-run", "-a", "--server-args=-screen 0 1440x900x24", "pytest"]
