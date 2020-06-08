# API Endpoint

## POST /api/register

Create a new user

### Request Body

-   email (string)
-   password (string)

### Responses

-   status (number)
-   token (string)

## POST /api/login

Login with an existing user

### Request Body

-   email (string)
-   password (string)

### Responses

-   status (number)
-   token (string)

## GET /api/account

Fetch informations related to the logged in user

### Responses

-   status (number)
-   rewards (number)
-   groups (object)

## GET /api/tasks

Get all tasks the current user can access

### Responses

-   status (number)
-   tasks (objects)

## GET /api/tasks/ID

Retrieve a specific task

### Request Parameters

-   ID (string)

### Responses

-   status (number)
-   task (object)

## DELETE /api/tasks/ID

Delete a specific task. The current user must NOT have a children account.

### Request Parameters

-   ID (string)

### Responses

-   status (number)

```





### Request Parameters

-   groups (GET)
-   groups/ID/tasks (GET, POST)
-   groups/ID/users (GET, POST)

-   tasks (GET)
-   tasks/ID (GET, DELETE)

-   tasks/ID/complete (PUT) [TODO]
-   tasks/ID/validate (PUT) [TODO]
-   tasks/ID/select (PUT)
-   tasks/ID/unselect (PUT)

-   users/ID (DELETE) [TODO]
-   users/ID/tasks (GET)
```
