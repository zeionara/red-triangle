# Red triangle

<p align="center">
    <img src="assets/logo.jpeg"/>
</p>

A web server for accessing generative language models from a smart speaker

## Eager mode

To evaluate one message and generate response, use the `ask` command:

```sh
python -m rt ask 'Есть такой анекдот' -c openai -m 'gpt-4'
```

## Server mode

To run `http` server which would allow you to interact with the smart speaker and generate responses using external models, use the following command:

```sh
python -m rt serve -c openchat
```

## Notes

To forward requests from `localhost:2222` to `foo.bar:3333`:

```sh
ssh -p 1111 -L 2222:localhost:3333 user@foo.bar
```

To run ngrok:

```sh
ngrok http --domain=foo-bar.ngrok-free.app 2222
```
