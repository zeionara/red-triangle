# Red triangle

<p align="center">
    <img src="assets/logo.jpeg"/>
</p>

A web server for accessing generative language models from a smart speaker

## Eager mode

To evaluate one message and generate response, use the `ask` command:

```sh
python -m rt ask 'Есть такой анекдот'
```

## Server mode

To run `http` server which would allow you to interact with the smart speaker and generate responses using external models, use the following command:

```sh
python -m rt start
```
