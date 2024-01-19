FROM python:3.10.8

WORKDIR /app
COPY requirements.txt .

RUN apt-get update && apt-get install -y libicu-dev
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

EXPOSE 8010
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8010"]
