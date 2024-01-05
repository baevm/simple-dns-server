FROM python:3.11.4-slim as base
WORKDIR /app/

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

RUN python -m venv /opt/venv
# Enable venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt


FROM python:3.11.4-slim as runner
WORKDIR /app/

COPY --from=base /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

COPY . .

EXPOSE 2053

ENTRYPOINT ["python3", "-u", "-m", "app.main"]
CMD ["--resolver", ""]