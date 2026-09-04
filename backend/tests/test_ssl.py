from services.ssl_service import SSLService

service = SSLService()

result = service.get_ssl_info(
    "https://google.com"
)

print(result)