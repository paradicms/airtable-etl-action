FROM ghcr.io/paradicms/etl:latest

ADD action.py /action.py

ENTRYPOINT ["/action.py"]
