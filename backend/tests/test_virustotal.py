from services.virustotal_service import VirusTotalService

vt = VirusTotalService()

print(

    vt.analyze(

        "https://google.com"
    )
)