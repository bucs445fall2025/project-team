from google import genai

client = genai.Client(api_key="AIzaSyA8ZLnS66ZhqfZJ6QVKkpWfjG-pI3gdYxY")

response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents="What is generative AI used for?",
)

print(response.text)
