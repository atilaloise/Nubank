# Nubank Authorization API

## Input
This Api receive as input, the account data (card status and current available limit), latest approved transactions and the current transaction to be approved.

### Schema

#### Input

Data Time format = '%Y-%m-%d %H:%M:%S'

Order:
`account`
`transaction`
`LastTransactions`

Set your payload as the examble bellow:

```json
[{
    "cardIsActive": "True",
    "limit": "1000",
    "denylist": [ "boteco do zé" ],
    "isInsideAllowlist": "True"
},
{  
    "merchant": "bar do tonho", 
    "amount": "901", 
    "time": "2019-06-09 17:10:32" 
},
{
	"lastTransactions": [ "2019-06-09 17:10:32 - brinquedos e cia", "2019-06-09 16:10:32 - Chop do 4" ]
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
