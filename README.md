# BucketList-API
<<<<<<< HEAD
Flask API
=======
It is a flask restful API with cool features like: Search, Token based Authentication and Pagination.

All Endpoints:

|Method | Endpoint | Usage |
| ---- | ---- | --------------- |
|POST| /api/v1/auth/register |  Register a user. |
|POST| /api/v1/auth/login | Login user.|
|POST| /api/v1/bucketlists/ | Create a new bucket list. |
|GET| /api/v1/bucketlists/ | Retrieve all the created bucket lists. |
|GET| `/api/v1/bucketlists/<bucket_id>` | Get a single bucket list. |
|PUT| `/api/v1/bucketlists/<bucket_id>` | Update a single bucket list. |
|DELETE| `/api/v1/bucketlists/<bucket_id>` | Delete single bucket list. |
|POST| `/api/v1/bucketlists/<bucket_id>/items `| Add a new item to this bucket list. |
|PUT|`/api/v1/bucketlists/<bucket_id>/items/<item_id>` | Update this bucket list. |
|DELETE|`/api/v1/bucketlists/<bucket_id>/items/<item_id>` | Delete this single bucket list. |
|GET| `/api/v1/bucketlists?limit=10&page=1` | Pagination to get 10 bucket list records.|
|GET| `/api/v1/bucketlists?q=a bucket` | Search for bucket lists with name like a bucket. |


### Installation

Clone the project. `git@github.com:skipcheru/BucketList-API.git`

Create a virtual environment and start the virtual environment.

Install requirements and run database migrations.

    pip install -r requirements.txt
    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade
    python manage.py runserver

See below examples then hack your way now :+1:

### Usage

+ Postman chrome extension is a good choice for testing.

+ Once the server is running, navigate to [http://localhost:5000/api/v1/auth/register]() using Postman.

+ Register a user, then login. An Authorization access_token is generated.

+ Copy the value of the access_token and add prefix JWT plus the access_token on Authorization header.


**__sample access token__**

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE0ODY0OTEwMDAsImlhdCI6MTQ4NjQ4NjUwMCwibmJmIjoxNDg2NDg2NTAwLCJpZGVudGl0eSI6MX0.  Q3Q855yVjm_XPpeGJw5DsELwYpKU55K-15TOC6Xgjeg"
}

```

**__Add Bucketlist__**

**eg.**
```json
data = { "name": "Workouts", "description": "List of workout activities" }

POST http://localhost:5000/api/v1/bucketlists/

Response:
{
  "count": 1,
  "buckets": [
    {
      "Id": 1,
      "Name": "Workouts",
      "created_by": 1,
      "date_created": "2017-02-09 16:19:04",
      "date_modified": "2017-02-09 16:19:04",
      "description": "List of workout activities",
      "items": []
    }
  ]
}
```

**__View all bucketlists__**

```json
GET http://localhost:5000/api/v1/bucketlists/

{
  "count": 1,
  "buckets": [
    {
      "Id": 1,
      "Name": "Workouts",
      "created_by": 1,
      "date_created": "2017-02-09 16:19:04",
      "date_modified": "2017-02-09 16:19:04",
      "description": "List of workout activities",
      "items": [
        {
          "date_created": "2017-02-09 16:20:49",
          "date_modified": "2017-02-09 17:04:19",
          "done": false,
          "id": 1,
          "name": "Marathons"
        }
      ]
    }
  ]
}

```
**__Search a bucketlist__**

```json
GET http://localhost:5000/api/v1/bucketlists/?q=bucket

```


**__Pagination__**

```json
GET http://localhost:5000/api/v1/bucketlists/limit=10&page=1
```


Oooh TDD is awesome, test the app using the command below:
```
$ pytest --cov=app tests/
```
>>>>>>> 5832458... Update README.md
