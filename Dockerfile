FROM python:3.10
WORKDIR /TubeMonitor
RUN apt-get update -y
RUN apt-get upgrade -y
COPY ./requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "3", "tubemonitor.wsgi:application", "--bind", "0.0.0.0:8000"]