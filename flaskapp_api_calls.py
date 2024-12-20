
import pandas as pd
from flask import Flask, request, jsonify
from textblob import TextBlob

app = Flask(__name__)

@app.route('/getsentiment', methods=['POST'])
def get_sentiment():
  '''
   Description: a Flask application that provides a REST API endpoint to perform sentiment analysis on text input.
   Input: The API endpoint /getsentiment accepts a POST request with a JSON body containing a single key-value pair.
   Output: The original text input and sentiment: The sentiment classification, which can be "positive", "negative", or "neutral".
   '''
  '''
  Sample API call:
  http://localhost:5000/getsentiment

  Json Body
  {
      "text": "This is a fantastic phone! It's very fast and has a great camera."
  }

  '''
  text= request.json['text']
  analyser_model = TextBlob
  sentiment_score = analyser_model(text).sentiment.polarity
  if sentiment_score > 0:
      return jsonify({'review_text':text,'sentiment': 'positive'})
  elif sentiment_score < 0:
      return jsonify({'review_text':text,'sentiment': 'negative'})
  else:
      return jsonify({'review_text':text,'sentiment': 'neutral'})




@app.route('/getreview', methods=['POST'])
def get_review_title():
  '''
  Description: a Flask application that provides a REST API endpoint to retrieve reviews based on specific product attributes (color, size, and rating).
  Input: The API endpoint /getreview accepts a POST request with a JSON body containing three key-value pairs.
  Output: The review_body field is a list of strings   , where each string represents a review that matches the specified color, size, and rating criteria.
  '''
  '''
  Sample API call- http://localhost:5000/getreview
  JSON Body:
  {
      "color": "Black",
      "size" : "128GB",
      "rating" : "5"
  }
  '''
  color = request.json['color']
  size = request.json['size']
  rating = request.json['rating']
  dataframe=pd.read_csv('amazon_review.csv')

  filtered_df = dataframe[(dataframe['Color'] == color) & (dataframe['Size'] == size) & (dataframe['Rating'].astype(str).str.startswith(rating))]
  reviews = filtered_df['Review Body'].tolist()
  return jsonify({'review_text':reviews})


if __name__ == '__main__':
    app.run(debug=True)

