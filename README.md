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

To generate ssl keys (for testing):

```sh
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

To [generate ssl keys](https://certbot.eff.org/instructions?ws=webproduct&os=pip) (for production):

```sh
sudo apt update
sudo apt install python3 python3-venv libaugeas0

sudo python3 -m venv /opt/certbot/
sudo /opt/certbot/bin/pip install --upgrade pip

sudo /opt/certbot/bin/pip install certbot
sudo ln -s /opt/certbot/bin/certbot /usr/bin/certbot

sudo certbot certonly --standalone
```

Output of `sudo certbot certonly --standalone` should look like this:

```
Saving debug log to /var/log/letsencrypt/letsencrypt.log
Please enter the domain name(s) you would like on your certificate (comma and/or
space separated) (Enter 'c' to cancel): zeio.ru zeio.online
Requesting a certificate for zeio.ru and zeio.online

Successfully received certificate.
Certificate is saved at: /etc/letsencrypt/live/zeio.ru/fullchain.pem
Key is saved at:         /etc/letsencrypt/live/zeio.ru/privkey.pem
This certificate expires on 2025-06-14.
These files will be updated when the certificate renews.

NEXT STEPS:
- The certificate will need to be renewed before it expires. Certbot can automatically renew the certificate in the background, but you may need to take steps to enable that functionality. See https://certbot.org/renewal-setup for instructions.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
If you like Certbot, please consider supporting our work by:
 * Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
 * Donating to EFF:                    https://eff.org/donate-le
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
```
