import redis

client = redis.Redis(host="localhost", port=6379, decode_responses=True)

response = client.ping()

print("Redis connected:", response)
