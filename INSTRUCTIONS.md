# Objective

Implement an API that authorizes a transaction for a specific account, following some predefined rules.

## Input

You'll receive as input: the account data (card status and current available limit), latest approved transactions and the current transaction to be approved.

## Output

The output should consist of whether the transaction was authorized or not, the updated available limit and, when relevant, all of the reasons why the transaction was denied.

### Rules

You should try to implement as many rules as you can, but can still submit even if you don't implement them all.

1. The transaction amount should not be above limit
2. No transaction should be approved when the card is blocked
3. The first transaction shouldn't be above 90% of the limit
4. There should not be more than 10 transactions on the same merchant
5. Merchant denylist
6. There should not be more than 3 transactions on a 2 minutes interval

### Schema

#### Input

`Account`
```json
{
    "cardIsActive": "Boolean",
    "limit": "Number",
    "denylist": [ "String" ],
    "isInsideAllowlist": "Boolean"
}
```

`Transaction`
```json
{  
    "merchant": "String", 
    "amount": "Number", 
    "time": "String" 
}
```

`LastTransactions`

```json
[ <Transaction> ]
```

#### Output

```json
{
  "approved": "Boolean",
  "newLimit": "Number",
  "deniedReasons": [ "String" ]
}
```
