FROM python:3.10-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

# اجرای FastAPI روی پورت 7860 که پورت استاندارد هاگینگ‌فیس است
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]