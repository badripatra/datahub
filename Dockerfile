FROM alpine:3.11
RUN mkdir nfsvolume
RUN mkdir logs
WORKDIR /code
COPY ./rest_services /code
COPY ./rest_services/requirements.txt requirements.txt
RUN apk add --no-cache py-pip
RUN pip install -r requirements.txt
EXPOSE 8083
CMD ["nohup" , "python", "rest_api.py", "&"]
