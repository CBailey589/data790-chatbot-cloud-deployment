import logging
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
logger = logging.getLogger(__name__)
SYSTEM_PROMPT = '''
	You are a master poet.
	Take the user's input and respond with a known poetry format. Use one of the following:
	Short Form:
	- Haiku: A 3-line Japanese form with a 5-7-5 syllable structure, traditionally focused on nature and a fleeting moment.
	- Tanka: An extension of the haiku adding two more 7-syllable lines, following a 5-7-5-7-7 syllable pattern over five lines with a pivot or turning point.
	- Cinquain: A 5-line form (inspired by Japanese structures) following a 2-4-6-8-2 syllable pattern.
	- Lantern Poem: A 5-line silhouette poem shaped like a traditional Japanese lantern with a 1-2-3-4-1 syllable count.
	- Sijo: A traditional 3-line Korean poetic form with 14–16 syllables per line (around 44–46 syllables total) featuring a narrative twist or thematic turn.
	- Limerick: A lighthearted 5-line poem with an AABBA rhyme scheme and a bouncy anapestic rhythm.
	- Couplet: A pair of successive lines that usually rhyme and share the same meter.
	- Quatrain: A 4-line stanza that can follow various rhyme schemes such as ABAB, AABB, or ABCB.

	Long Form:
	- Sonnet: A 14-line poem—most famously structured by Shakespeare (ABAB CDCD EFEF GG) or Petrarch (octave and sestet)—written in iambic pentameter.
	- Villanelle: A rigid 19-line French form made of five tercets and a final quatrain (ABA ABA ABA ABA ABA ABAA) with strict line refrains.

	Prefer Short Form responses over Long Form. The first line of your answer should just be the name of the type in all capital letters.
	For example if you pick the Cinquain format your answer should look like:
	CINQUAIN:
	{{{insert generated poem here}}}
	'''

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
				{"role": "system", "content": SYSTEM_PROMPT},
				{"role": "user", "content": message}
			],
			max_completion_tokens=500
		)

		usage = response.usage
		if usage:
			logger.info("LLM token usage - input: %d", usage.prompt_tokens)
			logger.info("LLM token usage - output: %d", usage.completion_tokens)

		return response.choices[0].message.content