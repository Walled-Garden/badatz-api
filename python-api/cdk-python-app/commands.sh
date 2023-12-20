# update template.yaml based on code
cdk synth --no-staging > template.yaml

# then start the local api
sam local start-api --template template.yaml

# one commnad
cdk synth --no-staging > template.yaml && sam local start-api --template template.yaml