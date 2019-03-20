# GPT-2 Flask API

OpenAI GPT-2 Flask API

First, before anything else download the model

```bash
mkdir models
curl --output models/gpt2-pytorch_model.bin https://s3.amazonaws.com/models.huggingface.co/bert/gpt2-pytorch_model.bin
```

## Local

```bash
python3 -m venv ./venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## docker-compose

### Setup

```bash
docker-compose up --build flask
```

Go to [http://localhost:5000](http://localhost:5000)

### Shutdown

```bash
docker-compose down -v
```

## Attribution

- [WillKoehrsen/recurrent-neural-networks](https://github.com/WillKoehrsen/recurrent-neural-networks)
- [graykode/gpt-2-Pytorch](https://github.com/graykode/gpt-2-Pytorch)
- [Deploying a Keras Deep Learning Model as a Web Application in Python](https://morioh.com/p/bbbc75c00f96/deploying-a-keras-deep-learning-model-as-a-web-application-in-python)
