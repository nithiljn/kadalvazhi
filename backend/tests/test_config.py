from app.config import settings

print("to testing that config working perfectly")
print({bool(settings.groq_api_key)})
print({bool(settings.model_name)})
print({bool(settings.openweather_api_key)})
print({bool(settings.debug)})