import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class LLMClient:
	def __init__(self):
		self.model = os.getenv("DEFAULT_MODEL", "gpt-4.1-mini")

		self.client = OpenAI(
			api_key=os.getenv("LLM_API_KEY"),
			base_url=os.getenv("LLM_BASE_URL"),
		)

	def chat(self, message: str) -> str:
		response = self.client.chat.completions.create(
			model=self.model,
			messages=[
				{"role": "system", "content": "You are a helpful assistant."},
				{"role": "user", "content": message}
			]
		)

		return response.choices[0].message.content