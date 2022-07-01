# utu-register-labeling-elg

## Information

TODO

## Quickstart

### Development

```
git clone --recurse-submodules https://github.com/lingsoft/utu-register-labeling-elg.git reglab
cd reglab
# TODO ./load-model.sh
# cd ..
docker build -t reglab-dev -f Dockerfile.dev .
docker run -it --rm -p 8000:8000 -v $(pwd):/app -u $(id -u):$(id -g) reglab-dev bash
flask run --host 0.0.0.0 --port 8000
```

Simple test call (Note slow startup time)

```
curl -X POST -H 'Content-Type: application/json' http://localhost:8000/process -d '{"type":"text","content":"Hello, world!"}'
```

Response should be

```json

```

### Tests

```
python -m unittest discover -s tests/ -v
```

### Usage (TODO)

```
docker build -t reglab .
docker run --rm -p 8000:8000 --init reglab
```

Or pull directly ready-made image `docker pull lingsoft/utu-bert-ner-fi:tagname`
(Note different versions. Tag must contain elg.)

### Local installation (TODO)

Use ELG-compatible service locally

```
cd elg_local && docker-compose up
```

The GUI is accessible on `http://localhost:5080`. See more 
[instructions](https://european-language-grid.readthedocs.io/en/stable/all/A1_PythonSDK/DeployServicesLocally.html#deploy-elg-compatible-service-from-its-docker-image).
