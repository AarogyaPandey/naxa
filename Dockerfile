FROM python:3
# Starts from python:3 Image

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Sets some env vars.

# I need a directory inside image to put my code, so i make a directory called code.
RUN mkdir /code


# Now this code directory is created, i need this dir to be my working dir.
WORKDIR /code

# Now i have my /code as a default dir, I am going to copy all my code inside this dir.
COPY . /code/

# Now i have my code, i will install packages from requirements.txt
RUN pip3 install -r requirements.txt

# Now i have my dependencies  installed, i will try to run my django app.
CMD ["python", "manage.py", "runserver"]