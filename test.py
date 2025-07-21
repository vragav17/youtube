import google.generativeai as genai

genai.configure(api_key="AIzaSyBfJb1um3rIBIs2q59CKbNqafuw-kWOSkc")

models = genai.list_models()

for model in models:
    print(model.name, model.supported_generation_methods)
