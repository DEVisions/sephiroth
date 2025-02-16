FROM python:3.9.6-alpine3.14

LABEL gitrepo="https://github.com/0xdade/sephiroth"

# Build:
# docker build --tag=sephiroth .

# Run:
# docker run --rm -v $(pwd):/app/output sephiroth -s nginx -t aws

WORKDIR /app/output
RUN pip install sephiroth

VOLUME /app/output
ENTRYPOINT ["sephiroth"]
