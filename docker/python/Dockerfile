FROM python:3.11
RUN apt-get update
RUN apt-get install --yes libx11-xcb1 libxcomposite1 libxcursor1 libxdamage1 libxfixes3 libxi6 libxtst6 libnss3 libnspr4 libcups2 libdbus-1-3 libxrandr2 libasound2 libatk1.0-0 libatk-bridge2.0-0 libgtk-3-0
ENV PYTHONUNBUFFERED 1
RUN mkdir /backend
WORKDIR /backend
ADD /backend/requirements.txt /backend/
RUN pip install -r requirements.txt
ADD ./backend /backend/