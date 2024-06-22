#!/bin/bash

curl -X POST -H "Content-Type: application/json" -d '{"title": "title 3", "ISBN": "1526617161", "genre": "Science"}' http://127.0.0.1:8000/books

curl -X POST -H "Content-Type: application/json" -d '{"title": "title 2", "ISBN": "9781408855652", "genre": "Fiction"}' http://127.0.0.1:8000/books

curl -X POST -H "Content-Type: application/json" -d '{"title": "title 3", "ISBN": "9780385050784", "genre": "Fiction"}' http://127.0.0.1:8000/books
curl -X GET http://127.0.0.1:80/books

curl -X POST -H 'Content-Type: application/json' -d '{"value": 4}' http://127.0.0.1:80/ratings/666b27ac46cf80c1cba0c4fe/values
curl -X POST -H 'Content-Type: application/json' -d '{"value": 4}' http://127.0.0.1:80/ratings/666b27ac46cf80c1cba0c4fe/values
curl -X POST -H 'Content-Type: application/json' -d '{"value": 5}' http://127.0.0.1:80/ratings/666b27ac46cf80c1cba0c4fe/values
curl -X POST -H 'Content-Type: application/json' -d '{"value": 5}' http://127.0.0.1:80/ratings/666b27ac46cf80c1cba0c4fe/values

curl -X GET http://127.0.0.1:80/top

#extra fields
curl -X PUT -H "Content-Type: application/json" -d '{"title": "title 3", "ISBN": "9780385050784", "genre": "Fiction", "authors": "Author Name", "publisher": "Publisher Name", "publishedDate": "2023-01-01", "extraField": "extraValue"}' http://127.0.0.1:8000/books/666b27ac46cf80c1cba0c4fe
curl -X PUT -H "Content-Type: application/json" -d '{"title": "title 3", "ISBN": "9780385050784", "genre": "Fiction"}' http://127.0.0.1:8000/books/666b27ac46cf80c1cba0c4fe


curl -X POST -H "Content-Type: application/json" -d '{"memberName": "Hadar", "ISBN": "9780385050784", "loanDate": "2024-05-01"}' http://127.0.0.1:5002/loans
#duplocated test
curl -X POST -H "Content-Type: application/json" -d '{"memberName": "Rotem", "ISBN": "9780385050784", "loanDate": "2024-05-01"}' http://127.0.0.1:5002/loans
curl -X POST -H "Content-Type: application/json" -d '{"memberName": "Hadar", "ISBN": "9781408855652", "loanDate": "2024-05-01"}' http://127.0.0.1:5002/loans
curl -X POST -H "Content-Type: application/json" -d '{"memberName": "Hadar", "ISBN": "1526617161", "loanDate": "2024-05-01"}' http://127.0.0.1:5002/loans
curl -X GET http://127.0.0.1:80/loans

curl -X GET http://127.0.0.1:80/loans/666b280d17148cd071d52915

curl -X DELETE http://127.0.0.1:5002/loans/666b280d17148cd071d52915

## Set the port
#PORT=80
#
## Function to echo curl command and its response
#function run_curl {
#    echo "Running curl command: $1"
#    response=$(eval $1 2>/dev/null)
#    echo "Response: $response"
#    echo "----------------------------------------"
#}
#
## Add three books
#run_curl "curl -s -X POST -H 'Content-Type: application/json' -d '{\"title\": \"title 1\", \"ISBN\": \"9780805371710\", \"genre\": \"Fiction\"}' http://127.0.0.1:$PORT/books"
#run_curl "curl -s -X POST -H 'Content-Type: application/json' -d '{\"title\": \"title 2\", \"ISBN\": \"0553213156\", \"genre\": \"Fiction\"}' http://127.0.0.1:$PORT/books"
#run_curl "curl -s -X POST -H 'Content-Type: application/json' -d '{\"title\": \"title 3\", \"ISBN\": \"9781408855652\", \"genre\": \"Biography\"}' http://127.0.0.1:$PORT/books"
#run_curl "curl -s -X POST -H 'Content-Type: application/json' -d '{\"title\": \"title 4\", \"ISBN\": \"9781291574890\", \"genre\": \"Fantasy\"}' http://127.0.0.1:$PORT/books"
### Get all books
#run_curl "curl -s -X GET http://127.0.0.1:$PORT/books"
#curl -X POST -H 'Content-Type: application/json' -d '{"value": 4}' http://127.0.0.1:8000/ratings/6650cd38ed8a27193fd507eb/values
#curl -X POST -H 'Content-Type: application/json' -d '{"value": 4}' http://127.0.0.1:8000/ratings/6650cd38ed8a27193fd507eb/values
#curl -X POST -H 'Content-Type: application/json' -d '{"value": 5}' http://127.0.0.1:8000/ratings/6650cd38ed8a27193fd507eb/values
#curl -X POST -H 'Content-Type: application/json' -d '{"value": 5}' http://127.0.0.1:8000/ratings/6650cd38ed8a27193fd507eb/values
### Get a single book
##run_curl "curl -s -X GET http://127.0.0.1:$PORT/books/1"
##
### Get all ratings
##run_curl "curl -s -X GET http://127.0.0.1:$PORT/ratings"
##
### Add ratings for each book
##for i in {1..3}; do
##    for j in {1..5}; do
##        run_curl "curl -s -X POST -H 'Content-Type: application/json' -d '{\"value\": $j}' http://127.0.0.1:$PORT/ratings/$i/values"
##    done
##done
##
##run_curl "curl -X GET http://127.0.0.1:$PORT/books?genre=Fiction"
##run_curl "curl -X GET http://127.0.0.1:$PORT/books?language=ger"
##run_curl "curl -X GET http://127.0.0.1:$PORT/books?language=ger&genre=Fiction"
##
##echo "Unsuccessful POST request due to receiving a media type other than JSON"
##echo "curl -X POST http://127.0.0.1:$PORT/books -H 'Content-Type: application/xml' -d '<title>Title 1</title><ISBN>9780805371710</ISBN><genre>Fiction</genre>'"
##curl -X POST http://127.0.0.1:$PORT/books -H "Content-Type: application/xml" -d '<title>Title 1</title><ISBN>9780805371710</ISBN><genre>Fiction</genre>'
##echo ""
##
### Unsuccessful POST request due to missing fields
##echo "Unsuccessful POST request due to missing fields"
##echo "curl -X POST http://127.0.0.1:$PORT/books -H 'Content-Type: application/json' -d '{\"title\": \"Title 1\"}'"
##curl -X POST http://127.0.0.1:$PORT/books -H "Content-Type: application/json" -d '{"title": "Title 1"}'
##echo ""
##
### Unsuccessful POST request due to incorrect field names
##echo "Unsuccessful POST request due to incorrect field names"
##echo "curl -X POST http://127.0.0.1:$PORT/books -H 'Content-Type: application/json' -d '{\"title\": \"Title 1\", \"ISBN_number\": \"9780805371710\", \"genre\": \"Fiction\"}'"
##curl -X POST http://127.0.0.1:$PORT/books -H "Content-Type: application/json" -d '{"title": "Title 1", "ISBN_number": "9780805371710", "genre": "Fiction"}'
##echo ""
##
### Unsuccessful POST request due to genre not being one of the accepted values
##echo "Unsuccessful POST request due to genre not being one of the accepted values"
##echo "curl -X POST http://127.0.0.1:$PORT/books -H 'Content-Type: application/json' -d '{\"title\": \"Title 1\", \"ISBN\": \"9780805371710\", \"genre\": \"Unknown Genre\"}'"
##curl -X POST http://127.0.0.1:$PORT/books -H "Content-Type: application/json" -d '{"title": "Title 1", "ISBN": "9780805371710", "genre": "Unknown Genre"}'
##echo ""
##
##echo "ratings"
##echo "curl -X GET http://127.0.0.1:$PORT/ratings -H "Content-Type: application/json""
##curl -X GET http://127.0.0.1:$PORT/ratings -H "Content-Type: application/json"
##echo ""
##
##echo "push ratings for 1"
##curl -s -X POST -H 'Content-Type: application/json' -d '{"value": 5}' http://127.0.0.1:$PORT/ratings/1/values
##curl -s -X POST -H 'Content-Type: application/json' -d '{"value": 5}' http://127.0.0.1:$PORT/ratings/1/values
##curl -s -X POST -H 'Content-Type: application/json' -d '{"value": 5}' http://127.0.0.1:$PORT/ratings/1/values
##curl -s -X POST -H 'Content-Type: application/json' -d '{"value": 5}' http://127.0.0.1:$PORT/ratings/1/values
##echo ""
##
##echo "top should be 1"
##curl -X GET http://127.0.0.1:$PORT/top -H "Content-Type: application/json"
