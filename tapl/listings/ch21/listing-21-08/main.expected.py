# Python
import tomllib

config = tomllib.loads("""
    [server]
    host = "localhost"
    port = 8080

    [database]
    url = "postgres://localhost/mydb"
""")

print(config["server"]["host"])
print(config["server"]["port"])
print(config["database"]["url"])
