# microblog-flask-api

**This is a API made in Flask.**

| HTTP Method|Resource URL | Notes
|--------------|-----------|------------|
|GET|api/users/<id>  |Return a user. |    
|GET|/api/users |	Return the collection of all users. |    
|GET|/api/users/<id>/followers | Return the followers of this user.|    
|GET|/api/users/<id>/followed | Return the users this user is following.|    
|POST|/api/users |Return a user.|    
|GET|api/users/<id>|Register a new user account.|    
|PUT|/api/users/<id> |Modify a user|    

## Resources Representation
Users:
```json
{
    "id": 123,
    "username": "susan",
    "password": "my-password",
    "email": "susan@example.com",
    "last_seen": "2021-06-20T15:04:27Z",
    "about_me": "Hello, my name is Susan!",
    "post_count": 7,
    "follower_count": 35,
    "followed_count": 21,
    "_links": {
        "self": "/api/users/123",
        "followers": "/api/users/123/followers",
        "followed": "/api/users/123/followed",
        "avatar": "https://www.gravatar.com/avatar/..."
    }
}
```