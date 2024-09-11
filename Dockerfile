FROM docker-enterprise-prod.artifactrepository.citigroup.net/developersvcs-python-ai/redhat-python-rhel7/e3.8:latest

LABEL citi.group="CoinXpert"
LABEL citi.app-name="CoinXpert"
LABEL citi.app-description="CoinXpert E4"
LABEL citi.csi-id="175873"
LABEL citi.image-maintainer="David Bloch (db48046)"

RUN echo "------------------------------------- Set ENV in Docker commands -------------------------------------------"
ENV APP_HOME /app
ENV VIRTUALENV_HOME $APP_HOME/pyvenv
ENV PIP_CONFIG_FILE=/app/pip.conf
ENV PIP_TRUSTED_HOST www.artifactrepository.citigroup.net

WORKDIR $APP_HOME

# Create a non-root user and group: appuser
RUN groupadd -r appgroup && useradd -r -g appgroup appuser
RUN mkdir -p $APP_HOME && chown -R appuser:appgroup $APP_HOME

# create python symlink so gcc can find python3.8m when installing modules requiring compilation
RUN mkdir /opt/rh/rh-python38 -p && ln -s /opt/middleware/redhat_python/3.8.0 /opt/rh/rh-python38/root

# create virtualenv
# this will ensure gunicorn is installed in the venv and runs properly on startup
RUN python -V && python -m venv $VIRTUALENV_HOME && source $VIRTUALENV_HOME/bin/activate

# Install dependencies
COPY pip.conf requirements.txt requirements_tests.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the application scripts and other files
COPY ./app /app/app
COPY ./tests /app/tests
COPY ./requirements.txt /app/
COPY ./requirements_tests.txt /app/

COPY ./tests /app/tests

# Setup runtime
USER root
RUN chmod -R g+rwx /app
EXPOSE 8080

# Use ENTRYPOINT for the main container process
ENTRYPOINT ["gunicorn", "app.main:app", "-b", "0.0.0.0:8080", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "-t", "6000"]

# Switch to the non-root user for running the application
USER appuser
