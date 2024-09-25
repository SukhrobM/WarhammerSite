FROM python:3.12.6-slim
WORKDIR /wh_tashkent
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /wh_tashkent
EXPOSE 7574
CMD ["flask", "run", "--port", "7574", "--host", "0.0.0.0"]