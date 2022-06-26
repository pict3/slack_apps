FROM python:3.8.5-slim-buster as builder
RUN apt-get update && apt-get clean
COPY requirements.txt /build/
WORKDIR /build/
RUN pip install -U pip && pip install -r requirements.txt

#FROM python:3.8.5-slim-buster as app
#COPY --from=builder /build/ /app/
#COPY --from=builder /usr/local/lib/ /usr/local/lib/
WORKDIR /app/
COPY ../*.py /app/
#COPY ReactionedUsersViewer.py /app/
#ENTRYPOINT python ReactionedUsersViewer.py

#CMD python test2.py

