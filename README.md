# Nubank Authorization API

## USE as docker container

### Build the docker image:

```console
foo@bar:~$ docker build -t nubankexercise .
```

### Run Container exposing port 5000:

```console
foo@bar:~$ docker run -ti -p 5000:5000 nubankexercise
```

## Run directly in your shell

### Install dependencies

```console
foo@bar:~$ pip3 install flask flask-jsonpify flask-restful datetime
```

### Run App with python3

```console
foo@bar:~$ python3 apiserver.py
```


## Running tests

```console
foo@bar:~$ python3 -m unittest
```


## Input
This Api receive as input, the account data (card status and current available limit), latest approved transactions and the current transaction to be approved.

### Schema

#### Input

Data Time format = '%Y-%m-%d %H:%M:%S'

Order:
`account`
`transaction`
`LastTransactions`

##### Implemented Rules 

These are some rules implemented and their respective json inputs as example. 

1. The transaction amount should not be above limit

```json
[{
    "cardIsActive": "True",
    "limit": "1000",
    "denylist": [],
    "isInsideAllowlist": "True"
},
{  
    "merchant": "bar do tonho", 
    "amount": "1002", 
    "time": "2019-06-09 17:10:32" 
},
{
    "lastTransactions": []
    }]
```

2. No transaction should be approved when the card is blocked

```json
[{
    "cardIsActive": "False",
    "limit": "1000",
    "denylist": [],
    "isInsideAllowlist": "True"
},
{  
    "merchant": "bar do tonho", 
    "amount": "100", 
    "time": "2019-06-09 17:10:32" 
},
{
    "lastTransactions": []
    }]
```

3. The first transaction shouldn't be above 90% of the limit

```json
[{
    "cardIsActive": "True",
    "limit": "1000",
    "denylist": [],
    "isInsideAllowlist": "True"
},
{  
    "merchant": "bar do tonho", 
    "amount": "990", 
    "time": "2019-06-09 17:10:32" 
},
{
    "lastTransactions": []
    }]
```

4. There should not be more than 10 transactions on the same merchant

```json
[{
    "cardIsActive": "True",
    "limit": "1000",
    "denylist": [],
    "isInsideAllowlist": "True"
},
{  
    "merchant": "boteco do zé", 
    "amount": "90", 
    "time": "2019-06-09 17:10:32" 
},
{
    "lastTransactions": ["2019-06-09 17:10:32 - boteco do zé", "2019-06-09 16:12:32 - boteco do zé", "2019-06-08 23:59:00 - boteco do zé", "2019-06-09 16:10:32 - boteco do zé", "2019-06-09 16:10:32 - boteco do zé", "2019-06-09 16:10:32 - boteco do zé", "2019-06-09 16:10:32 - boteco do zé", "2019-06-09 16:10:32 - boteco do zé", "2019-06-09 16:10:32 - boteco do zé", "2019-06-09 16:10:32 - boteco do zé", "2019-06-09 16:10:32 - boteco do zé"]
    }]
```


5. Merchant denylist

```json
[{
    "cardIsActive": "True",
    "limit": "1000",
    "denylist": ["bar do tonho"],
    "isInsideAllowlist": "True"
},
{  
    "merchant": "bar do tonho", 
    "amount": "990", 
    "time": "2019-06-09 17:10:32" 
},
{
    "lastTransactions": []
    }]
```

6. There should not be more than 3 transactions on a 2 minutes interval

```json
[{
    "cardIsActive": "True",
    "limit": "1000",
    "denylist": ["bar do tonho"],
    "isInsideAllowlist": "True"
},
{  
    "merchant": "bar do tonho", 
    "amount": "990", 
    "time": "2019-06-09 16:13:32" 
},
{
    "lastTransactions": ["2019-06-09 16:13:10 - boteco do zé", "2019-06-09 16:12:40 - boteco do zé", "2019-06-09 16:12:32 - boteco do zé"]
    }]
```


#### Output

If everything is passed in the correct  way, you should see as output as bellow;

```json
{
  "approved": "Boolean",
  "newLimit": "Number",
  "deniedReasons": [ "String" ]
}
```
