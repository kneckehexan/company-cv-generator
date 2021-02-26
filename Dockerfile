FROM python:3.7-alpine
MAINTAINER Philip Tunbjer "philip.tunbjer@bjerking.se"

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
RUN mkdir appDock/
COPY dockerreq/requirements.txt /appDock/requirements.txt
WORKDIR ./appDock
RUN pip install -r requirements.txt
WORKDIR ../
COPY . ./appDock
ENV FLASK_APP=app.py
#ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development
EXPOSE 5000
CMD ["python", "appDock/app.py"]