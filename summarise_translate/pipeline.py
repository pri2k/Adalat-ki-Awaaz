import pandas as pd
from google import genai
from transformers import pipeline

client = genai.Client(api_key=api_key)
translator = pipeline("translation", model="facebook/nllb-200-distilled-600M")


tgt_langs = ["hin_Deva", "ben_Beng", "tel_Telu"]
results = []


for index, text in enumerate(df["summary"]):
      response = client.models.generate_content(
          model="gemini-2.0-flash",
          contents=f"Summarise the following text for a news article in less than 512 words. Include all important points. Give only the summary and nothing else\n{text}",
      )
      summary = response.text

      translations = {}
      for lang in tgt_langs:
          result = translator(summary, src_lang="eng_Latn", tgt_lang=lang, max_length=512)
          translations[lang] = result[0]["translation_text"]

      results.append({
          "original_text": text,
          "summary": summary,
          "summary_hindi": translations["hin_Deva"],
          "summary_bengali": translations["ben_Beng"],
          "summary_telugu": translations["tel_Telu"],
      })

summary_df = pd.DataFrame(results)

print(summary_df.head())


summary_df.to_csv("summarized_translations.csv", index=False)
