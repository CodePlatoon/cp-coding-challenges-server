FROM python:3.14-slim-trixie

WORKDIR /app

COPY  requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install gunicorn

COPY . .

EXPOSE 8000

CMD ["gunicorn", "api_proj.wsgi", "--bind", "0.0.0.0:8000"]