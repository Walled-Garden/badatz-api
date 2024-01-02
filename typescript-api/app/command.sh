# build docker image
docker build -t badatz-api .

# run docker image
docker run -p 3000:3000 --rm -it badatz-api
# run test
docker run -p 3000:3000 --rm -it badatz-api bash

# benchmarks
ab -n 10 -c 10 -p post_data.txt -T application/json http://localhost:3000/