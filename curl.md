***PUT***

```bash
curl -X PUT -H "Content-Type: application/json" -d '{"key1":"value"}' "YOUR_URI"


curl --request PUT --url http://localhost:8080/put --header 'content-type: application/x-www-form-urlencoded' --data 'bar=baz&foo=foo1'
```

***POST***

```bash
curl -X POST "YOUR_URI" -F 'file=@/file-path.csv'

curl --request POST --url http://localhost:8080/post --header 'content-type: application/x-www-form-urlencoded' --data 'bar=baz&foo=foo1'
```

***GET***

```bash
curl --request GET --url 'http://localhost:8080/get?foo=bar&foz=baz'

curl https://reqbin.com/echo/get/json -H "Accept: application/json"

```



