import pandas as pd
from transformers import pipeline

translator = pipeline("translation", model="facebook/nllb-200-distilled-600M")
summarizer = pipeline("summarization")


tgt_langs = ["hin_Deva", "ben_Beng", "tel_Telu"]
results = []


for index, text in enumerate(df["content"]):
      summary = summarizer(text, max_length=512)[0]["translation_text"]
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
