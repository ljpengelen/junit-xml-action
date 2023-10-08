FROM python:3.12-alpine

COPY post-test-results.py /post-test-results.py

ENTRYPOINT ["python", "/post-test-results.py"]
