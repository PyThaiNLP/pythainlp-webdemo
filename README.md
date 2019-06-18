# PyThaiNLP Web Demo
<div align="center">
    <img src="https://i.imgur.com/C6FhLfD.png"/>
    <p>
        PyThaiNLP Web Demo is a web application containing several algorithms implemented in PyThaiNLP. 
        It is an interface that allows users test those algorithms before actually adopting them in their usecases or applications. 
    </p>
</div>

## Run via Docker (recommended)
```
# The command below starts the web that can be accessed
# via http://127.0.0.1:8080
> docker run -i -p 8080:80 pythainlp/demo
 * Serving Flask app "main" (lazy loading)
```

## Run locally  
```
# Please make sure that all dependencies are installed
# via pip install -r requirements.txt
> python main.py
```

## Development

### Build Docker image
```
 docker build -t pythainlp/demo .
```

## Contributions
We're more than happy to receive issues and pull-requests.