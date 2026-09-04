from services.whois_service import WHOISService

service = WHOISService()

info = service.get_domain_info(
    "https://google.com"
)

print(info)