# D-fraudr
Analyze a column of numbers for how closely it follows Benford's Law

INSTALLATION
From this package directory:

```
docker build -t dfraudr .
```

Once the docker image has been built, run the app with

```
docker run -it -p5000:5000 dfraudr:latest
```
(The '-it' options allow you to stop the server once it has started)