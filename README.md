# Carbon

## Testing our API

You're now ready to test the API.
```
python app.py runserver
```

You can easily test if the endpoint is working by doing the following in your terminal
```
curl -H "Content-Type: application/json" -X GET -u admin:password -d '{"distance":357}' http://localhost:5000/carbon/api/v1.0/transport/flight
```
More details about endpoints access [documentation](http://localhost:5000/apidocs/).