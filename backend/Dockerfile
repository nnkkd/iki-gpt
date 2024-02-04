FROM python:3.10-slim as local

WORKDIR /backend

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload" ]

FROM public.ecr.aws/lambda/python:3.10 AS lambda
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . ${LAMBDA_TASK_ROOT}
CMD ["app.main.handler"]