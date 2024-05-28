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
COPY pip.conf requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Switch to the non-root user
USER appuser

# Copy the application scripts
COPY main.py .
COPY fee_calculator.py .
COPY coin_selection_algorithms.py .
COPY transaction_simulation.py .
COPY utxo_models.py .

# Copy static files and templates
COPY static/ static/
COPY templates/ templates/

# Copy any required configurations
COPY requirements.txt .
COPY .dockerignore .

# Setup runtime
USER root
RUN chmod -R g+rwx .
EXPOSE 8080
# CMD ["sleep", "600"]
# -w 2  : specifies number of worker class to use
# -t 120 : specifies the maximum request processing time in seconds. If request takes longer it is terminated by gunicorn
CMD export HOME=$APP_HOME && gunicorn main_service:app -b 0.0.0.0:8080  -w 1 -k uvicorn.workers.UvicornWorker -t 6000
USER appuser