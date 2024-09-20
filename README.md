# Django-Stripe Test Application

This application was written in order to learn integration with the [Stripe](https://stripe.com/docs/checkout/quickstart) payment system, and make a mini-layout of online store with the ability to pay via Stripe.

## System dependencies
[Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

[docker-compose](https://docs.docker.com/compose/install/)

[make](https://www.gnu.org/software/make/)

## Install dependencies 

```bash
pip install -r requirements.txt
```

## Run app:

```bash
make migrate
make run
```

### Create superuser

```bash
make superuser
```
