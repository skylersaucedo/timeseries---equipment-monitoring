FROM python:3.9

WORKDIR /code

COPY . /code/

#COPY ["requirements.txt" , "sensor_data.csv" , "skyler_detector.py", "main.py", "make_vis.py",  ". /code/"]

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# create user with limited access

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /code
USER appuser

CMD ["python" , "main.py", "bokeh", "serve", "make_vis.py"]