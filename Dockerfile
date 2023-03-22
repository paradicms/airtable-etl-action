FROM ghcr.io/paradicms/paradicms:latest

ADD action.py /action.py

ENTRYPOINT ["/action.py"]
