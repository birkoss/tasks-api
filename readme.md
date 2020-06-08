# API Endpoint

## User

### POST /api/register

Create a new user

Request Parameters

Request Body

Responses

Fields

```
- register 			(POST)
	- email
	- password

	= token

- login 			(POST)
	- email
	- password

	= token

- account 			(GET)
	= rewards
	= groups


- groups			(GET)
- groups/ID/tasks 	(GET, POST)
- groups/ID/users   (GET, POST)

- tasks 			(GET)
- tasks/ID 			(GET, DELETE)

- tasks/ID/complete (PUT)			[TODO]
- tasks/ID/validate (PUT)			[TODO]
- tasks/ID/select 	(PUT)
- tasks/ID/unselect (PUT)

- users/ID 			(DELETE)		[TODO]
- users/ID/tasks 	(GET)
```
