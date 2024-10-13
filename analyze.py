import json
from transformers import pipeline, T5ForConditionalGeneration, T5Tokenizer

# Load Hugging Face model for summarization and sentiment analysis
def load_models():
    tokenizer_ = T5Tokenizer.from_pretrained("google/flan-t5-small")
    model_ = T5ForConditionalGeneration.from_pretrained("google/flan-t5-small")
    summarization_pipeline = pipeline("summarization", model=model_, tokenizer=tokenizer_)
    sentiment_pipeline = pipeline("sentiment-analysis")
    return summarization_pipeline, sentiment_pipeline

# Extract names from the description field
def extract_names_from_description(description):
    if "Email address of" in description:
        return description.split("Email address of ")[1].split(",")[0].strip()
    elif "Email address for" in description:
        return description.split("Email address for ")[1].split(",")[0].strip()
    else:
        return "Unknown"

# Summarize content of individual email threads using FLAN-T5
def summarize_thread(summarization_pipeline, emails):
    thread_content = " ".join([email['content'] for email in emails])
    summary = summarization_pipeline(thread_content, do_sample=False)
    return summary[0]['summary_text']

# Analyze sentiment of the conversations using a sentiment model
def analyze_sentiment(sentiment_pipeline, emails):
    email_contents = " ".join([email['content'] for email in emails])
    sentiment_result = sentiment_pipeline(email_contents)
    # Get sentiment label
    sentiment = sentiment_result[0]['label']  
    # Convert the sentiment result to Positive, Negative, or Neutral
    return {'POSITIVE': 'Positive', 'NEGATIVE': 'Negative'}.get(sentiment, 'Neutral')

# Process the logs and use the LLM for tasks
def process_email_threads(input_file_path, output_file_path, summarization_pipeline, sentiment_pipeline):
    with open(input_file_path, 'r') as f, open(output_file_path, 'w') as output_file:
        for line in f:
            email_thread = json.loads(line.strip())
            thread_id = email_thread['thread_id']
            description = email_thread['description']
            emails = email_thread['emails']            
            # Extract names of participants from the description field
            name = extract_names_from_description(description)            
            # Summarize the email thread using FLAN-T5
            thread_summary = summarize_thread(summarization_pipeline, emails)            
            # Analyze the sentiment of the email thread
            sentiment = analyze_sentiment(sentiment_pipeline, emails)            
            # Write results to file
            output_data = {
                'thread_id': thread_id,
                'name': name,
                'summary': thread_summary,
                'sentiment': sentiment
            }
            output_file.write(json.dumps(output_data) + '\n')

def analyze():
    input_file_path = 'all_emails.jsonl'
    output_file_path = 'results.jsonl'
    
    # Load models for summarization and sentiment analysis
    summarization_pipeline, sentiment_pipeline = load_models()
    
    # Process the email threads using the loaded models
    process_email_threads(input_file_path, output_file_path, summarization_pipeline, sentiment_pipeline)
