FROM lambci/lambda:build-python3.7
RUN pip3 install face_recognition flask opencv-python
ENV FLASK_APP=webcam.py
COPY webcam.py /var/task
ENTRYPOINT ["flask","run","--host=0.0.0.0"]