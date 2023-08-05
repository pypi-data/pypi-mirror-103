# vm-booking-app

A RESTful API application where I can store data about VMs used by customers.

## Installation

Install using `pip`:

```
$ pipenv install
$ flask run
```

## API Usage Examples

Get all users.
```
$ curl -X GET http://localhost:5000/api/users
{
  "users": [
    {
      "id": 1,
      "email: "user1@gmail.com",
      "username": "user1"
    },
    {
      "id": 2,
      "email: "user2@gmail.com",
      "username": "user2"
    }
  ]
}
```

Get a user.

Gets a user **username**.

```
$ curl -X GET http://localhost:5000/api/users/<slug>
{
  "user": {
    "id": 1,
    "email: "user1@gmail.com",
    "username": "user1"
  }
}
```

Create a user.

**Email** and **username** are required fields.

```
$ curl -X POST http://localhost:5000/api/users -d '{"email":"user3@gmail.com", "username": "user3"}'
{
  "user": {
    "id": 1,
    "email": "user3@gmail.com",
    "username": "user3"
  }
}
```

Update a user.

Only **email** and **username** can be changed.

```
$ curl -X PATCH http://localhost:5000/api/users/<slug> -d '{"email":"user4@gmail.com"}'
{
  "user": {
    "id": 1,
    "email": "user4@gmail.com",
    "username": "user4"
  }
}
```

Delete a user.
```
$ curl -X DELETE http://localhost:5000/api/users/<slug>
{
  "user": {
    "id": 1,
    "email": "user1@gmail.com",
    "username": "user1"
  }
}
```


Get all vms.

```
$ curl -X GET http://localhost:5000/api/vms
{
  "vms": [
    {
      "id": 1,
      "name": "VM1",
      "ip": "10.0.2.3",
      "description": "general purpose vm",
      "status": "running",
      "reservation_start": "21/11/2026",
      "reservation_end": "21/11/2026",
      "user_id": 1
    }
  ]
}
```

Get a vm.

```
$ curl -X GET http://localhost:5000/api/vms/<id>
{
  "vm": {
    "id": 1,
    "name": "VM1",
    "ip": "10.0.2.3",
    "description": "general purpose vm",
    "status": "running",
    "reservation_start": "21/11/2026",
    "reservation_end": "21/11/2026",
    "user_id": 1
  }
}
```

Create a vm.

**Name**, **ip**, **user_id** are required. 

```
$ curl -H "Content-Type: application/json" -X POST http://localhost:5000/api/vms
-d '{"ip":"10.0.2.4", "name": "VM1", "reservation_start": "21/11/2026", "reservation_end": "21/11/2026", "userId": 2}'
{
  "vm": {
    "id": 1,
    "name": "VM1",
    "ip": "10.0.2.3"
    "description": "general purpose vm",
    "status": "running",
    "reservation_start": "21/11/2026",
    "reservation_end": "21/11/2026",
    "user_id": 1
  }
}
```

Update vm.

Only **name**, **description** and **status** can be chanded currently.

```
$ curl -H "Content-Type: application/json" -X PATCH http://localhost:5000/api/vms/<id>
-d '{"description":"standart vm"}'
{
  "vm": {
    "id": 1,
    "name": "VM1",
    "ip": "10.0.2.3",
    "description": "standard vm",
    "status": "running",
    "reservation_start": "21/11/2026",
    "reservation_end": "21/11/2026",
    "user_id": 1
  }
}
```

Delete vm.

```
$ curl -H "Content-Type: application/json" -X DELETE http://localhost:5000/api/vms/<id>
{
  "vm": {
    "id": 1,
    "ip": "10.0.2.3",
    "name": "VM1",
    "description": "standard vm",
    "status": "running",
    "reservation_start": "21/11/2026",
    "reservation_end": "21/11/2026",
    "user_id": 1
  }
}
```

Get vm usage by username

```
$ curl -X GET http://localhost:5000/api/users/<slug>/vm-use
{
  "user": {
    "id": 1,
    "email": "user1@gmail.com",
    "username": "user1",
    "vms": [{}, {}]
  }
}
```


## Development

For working on `vm-booking-app`, you'll need to have Python >= 3.7 and [`pipenv`][1] installed. With those installed, run the following command to create a virtualenv for the project and fetch the dependencies:

```
$ pipenv install --dev
...
```

Next, activate the virtualenv and get to work:

```
$ pipenv shell
...
(vm-booking-app) $
```

[1]: https://docs.pipenv.org/en/latest/

## Linting

For linting we use `flake8` tool. We should keep code clean. To run linter use the following command:

```
$ flake8 api
...
```

## Models

User
```
id: number
email: string
username: string
```

VM
```
id: number
name: string
ip: string
description: string?
status: string
reservation_start: DateTime
reservation_end: DateTime
user_id: User.id
```

## Deploying

```
cd ~
git clone git@gitlab-1914910442.us-west-2.elb.amazonaws.com:oonyshchenko/vm-booking-app.git
git checkout master
source .env_prod
docker-compose up --build -d
```

## Testing 

Open in browser http://localhost:5000 to get API status and version.

Open in browser http://localhost:5000/healthy to get DB connection status.

Automatic tests
```
(vm-booking-app) $ pytest
(vm-booking-app) $ pytest --cov=api   
```