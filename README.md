# FastAPI Microservices

## Python Version

Check Python version
```sh
$ Python --version
```

Install Python version required

```sh
$ pyenv install 3.8.14
```

## Virtual Environment

1.- Create project folder 

```sh
$ mkdir $HOME/Projects/FastAPIProject
$ cd $HOME/Projects/FastAPIProject
```

2.- Config local Python version

```sh
$ pyenv local 3.8.14
```

## Dependencies

1.- Create requirements file

```sh
$ touch requirements.txt
```

2.- Add dependencies projects

```
anyio==3.6.1
bcrypt==3.2.2
cffi==1.15.0
click==8.1.3
colorama==0.4.5
fastapi==0.78.0
h11==0.13.0
idna==3.3
pycparser==2.21
pydantic==1.9.1
python-multipart==0.0.5
six==1.16.0
sniffio==1.2.0
starlette==0.19.1
typing_extensions==4.2.0
uvicorn==0.18.2
```

3.- Install dependencies

```sh
$ pip install -r requirements.txt
```
##