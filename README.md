# wf-market-price-bot
small project to bulk update current wfmarket orders using lowest existing price

## To Run
1. create `credentials.json` file in the root repository and populate `email` and `password`
```
{
    "email": "email_here",
    "password": "password_here",
    "auth_type": "header"
}
```

2. run `python main.py`