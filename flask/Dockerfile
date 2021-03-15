FROM python:3.7-alpine

# Setting up TeXLive - minimal installation
COPY dockerreq/texlive-profile.txt /tmp/
RUN apk add --no-cache wget perl xz && \
    wget http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz && \
    tar -xzf install-tl-unx.tar.gz && \
    install-tl-20*/install-tl --profile=/tmp/texlive-profile.txt && \
    rm -rf install-tl*
ENV PATH=/usr/local/texlive/bin/x86_64-linuxmusl:$PATH
RUN tlmgr update --self
COPY dockerreq/packages.txt /tmp/packages.txt
RUN tlmgr install $(cat /tmp/packages.txt)

# Set up Flask
RUN mkdir app/
RUN apk add python3-dev build-base linux-headers pcre-dev
COPY dockerreq/requirements.txt app/
WORKDIR /app
RUN pip install -r requirements.txt
COPY . ./app
ENV FLASK_APP=run.py
#ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000
CMD ["uwsgi", "app.ini"]
