from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import os
from random import randint
import pandas as pd

class AzureNlp:
  def __init__(self):
    self.client = TextAnalyticsClient(
                endpoint=os.environ['AZURE_ENDPOINT'],
                credential=AzureKeyCredential(os.environ['AZURE_KEY']))

  def response_message(self, message: list):
    response = self.client.analyze_sentiment(
        documents=message, language="ja")[0]
    if response.confidence_scores.negative <= 0.4:
      df = pd.read_csv("positive.csv").iloc[:, 1:]
    else:
      df = pd.read_csv("negative.csv").iloc[:, 1:]

    mes_id = randint(1, len(df))

    res_mes = df[df["id"] == mes_id]["text"].values[0]
    return res_mes

  def find_key(self, messages:list):
    keys = self.client.extract_key_phrases(
        messages, language="ja")[0].key_phrases
    return keys

def main():
  az = AzureNlp()
