FROM python

ADD bot.py .

RUN pip3 install -r ./requirements.txt

CMD ["python", "./bot.py"]
