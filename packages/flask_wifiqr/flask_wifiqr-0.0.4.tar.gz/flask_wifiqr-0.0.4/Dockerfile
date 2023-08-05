FROM        python:3.9-alpine
MAINTAINER  Flip Hess <flip@fliphess.com>

COPY        . /opt/wifiqr

RUN         addgroup --system --gid 1234 wifiqr \
 &&         adduser --system -u 1234 --home /opt/wifiqr --shell /sbin/nologin --ingroup wifiqr wifiqr \
 &&         chown -R wifiqr:wifiqr /opt/wifiqr

USER        wifiqr
WORKDIR     /opt/wifiqr

RUN         python3 -m venv ./venv \
 &&         source ./venv/bin/activate \
 &&         pip --no-cache-dir --disable-pip-version-check --quiet install .

ENTRYPOINT  ["./venv/bin/wifiqr"]
