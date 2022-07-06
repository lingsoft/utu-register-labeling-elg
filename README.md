# Multi-label register classification

## Information

This repository contains
[ELG compatible](https://european-language-grid.readthedocs.io/en/stable/all/A3_API/LTInternalAPI.html)
Flask based REST API for
[Multi-label register classification](https://github.com/annsaln/torch-transformers-multilabel)
It is trained for web documents and
this version supports four languages: Finnish, Swedish, English and French.
Models are available [here](http://dl.turkunlp.org/register-labeling-model/).

Original authors: TurkuNLP (Veronika Laippala et al.) under different
[projects](https://turkunlp.org/projects.html).

This ELG API was developed in EU's CEF project:
[Microservices at your service](https://www.lingsoft.fi/en/microservices-at-your-service-bridging-gap-between-nlp-research-and-industry).

## Quickstart

### Development

```
git clone --recurse-submodules https://github.com/lingsoft/utu-register-labeling-elg.git reglab
cd reglab
docker build -t reglab-dev -f Dockerfile.dev .
docker run -it --rm -p 8000:8000 -v $(pwd):/app -u $(id -u):$(id -g) reglab-dev bash
# cd app/ttml
# ./load-fine-tuned.sh
# python load-tokenizer.py
# cd ..
flask run --host 0.0.0.0 --port 8000
```

Tests

```
python -m unittest discover -s tests/ -v
```

### Usage

```
docker build -t reglab .
docker run --rm -p 8000:8000 --init reglab
```

Or pull directly ready-made image
`docker pull lingsoft/utu-register-labeling:tagname`

Simple test call

```
curl -X POST -H 'Content-Type: application/json' http://localhost:8000/process -d '{"type":"text","content":"Hello, world!"}'
```

Response should be

```json
{
  "response": {
    "type": "classification",
    "classes": [
      {
        "class": "ID - Interactive discussion",
        "score": 0.5767741799354553
      }
    ]
  }
}
```

More information about registers (classes or text genres) can be found from
the file `app/ttml/README.md`.

Text request can also contain parameters:

```json
{
    "type": "text",
    "content": "Hello, world!",
    "params": {
        "threshold": 0.1,
        "sub_registers": False
    }
}
```

The `content` property contains text to be analyzed.
Note that text can not be too long (512 tokens).
The `params` property is optional and can contain

- `threshold` (float, default = 0.4, range 0.0-1.0)
  - minimum score below which results will not be returned
- `sub_registers` (boolean, default = True)
  - maximum number of subjects to return

### Local installation

Use ELG-compatible service locally

```
cd elg_local && docker-compose up
```

The GUI is accessible on `http://localhost:5080`. See more 
[instructions](https://european-language-grid.readthedocs.io/en/stable/all/A1_PythonSDK/DeployServicesLocally.html#deploy-elg-compatible-service-from-its-docker-image).
