#!/bin/bash

# Add Books
books=(
  '{"title":"Adventures of Huckleberry Finn", "ISBN":"9780520343641", "genre":"Fiction"}'
  '{"title":"The Best of Isaac Asimov", "ISBN":"9780385050784", "genre":"Science Fiction"}'
  '{"title":"Fear No Evil", "ISBN":"9780394558783", "genre":"Biography"}'
  '{"title":"The Adventures of Tom Sawyer", "ISBN":"9780195810400", "genre":"Fiction"}'
  '{"title":"I, Robot", "ISBN":"9780553294385", "genre":"Science Fiction"}'
  '{"title":"Second Foundation", "ISBN":"9780553293364", "genre":"Science Fiction"}'
)
for book in "${books[@]}"; do
  curl -X POST -H "Content-Type: application/json" -d "$book" http://localhost:5001/books
done

# Read Query and Execute
touch response.txt
while IFS= read -r query; do
  response=$(curl -s -w "\n%{http_code}" "http://localhost:5001/books$query")
  code=$(echo "$response" | tail -n 1)
  body=$(echo "$response" | sed '$d')
  echo "query: $query" >> response.txt
  if [ "$code" -eq 200 ]; then
    echo "response: $body" >> response.txt
  else
    echo "response: error $code" >> response.txt
  fi
done < query.txt