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

## PUT /api/tasks/ID/select

Select the task with the current user

### Request Parameters

-   ID (string)

### Responses

-   status (number)

## PUT /api/tasks/ID/unselect

Unselect the task, if already selected by the current user

### Request Parameters

-   ID (string)

### Responses

-   status (number)

## GET /api/users

Get all users in all groups the user have

### Responses

-   status (number)
-   users (objects)

## GET /api/users/ID/tasks

Get all tasks selected by a user

### Request Parameters

-   ID (string)

### Responses

-   status (number)
-   tasks (objects)

## GET /api/groups

Get all groups

### Responses

-   status (number)
-   groups (objects)

## GET /api/groups/ID/users

Get all users of this group

### Request Parameters

-   ID (string)

### Responses

-   status (number)
-   users (objects)

## GET /api/groups/ID/tasks

Get all tasks of this group

### Request Parameters

-   ID (string)

### Responses

-   status (number)
-   tasks (objects)

# API Endpoint remaining

## DELETE /api/users/ID

## PUT /tasks/ID/complete

## PUT /tasks/ID/validate
