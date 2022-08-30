FROM base-runtime

ARG SERVICE_CODEBASE
ARG MODULE

WORKDIR /home/app/services
ADD ${SERVICE_CODEBASE}/${MODULE}/ ./${MODULE}
ADD ${SERVICE_CODEBASE}/database/ ./database

WORKDIR /home/app
ENV MODULE=${MODULE}
CMD uvicorn services.${MODULE}.main:app --host 0.0.0.0 --reload
