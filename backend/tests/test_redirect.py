from services.redirect_service import RedirectService

service = RedirectService()

result = service.analyze(
    "http://google.com"
)

print(result)