FROM python:3.8-alpine
COPY ./requirements.txt /app/requirements.txt
ENV DATABASE_URI=sqlite:///base.db
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app
ENTRYPOINT ["python"]
CMD ["app.py"]
