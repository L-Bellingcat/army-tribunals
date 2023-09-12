FROM python:3.10
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
ENV PYTHONPATH="${PYTHONPATH}:~/"
ENV PYTHONPATH="${PYTHONPATH}:website/"
WORKDIR website
CMD python server.py