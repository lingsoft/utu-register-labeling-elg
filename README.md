# utu-register-labeling-elg

## Information

TODO

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

More information about registers (classes) can be found from the file
`app/ttml/README.md`.

### Tests

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

### Local installation

Use ELG-compatible service locally

```
cd elg_local && docker-compose up
```

The GUI is accessible on `http://localhost:5080`. See more 
[instructions](https://european-language-grid.readthedocs.io/en/stable/all/A1_PythonSDK/DeployServicesLocally.html#deploy-elg-compatible-service-from-its-docker-image).
