FROM python:3.7-alpine
MAINTAINER Philip Tunbjer "philip.tunbjer@bjerking.se"
RUN mkdir appDock/
COPY ./requirements.txt /appDock/requirements.txt
WORKDIR ./appDock
RUN pip install -r requirements.txt
WORKDIR ../
COPY . ./appDock
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000
CMD ["python", "appDock/www/app.py"]
