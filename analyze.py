import json
import logging
from transformers import pipeline, T5ForConditionalGeneration, T5Tokenizer
from typing import List, Tuple, Dict

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load Hugging Face model for summarization and sentiment analysis
def load_models() -> Tuple[pipeline, pipeline]:
    # Let the pipeline handle model and tokenizer loading
    summarization_pipeline = pipeline("summarization", model="google/flan-t5-small")
    
    # Explicitly specify the sentiment analysis model
    sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")
    
    return summarization_pipeline, sentiment_pipeline

# Extract names from the description field
def extract_names_from_description(description: str) -> str:
    if "Email address of" in description:
        return description.split("Email address of ")[1].split(",")[0].strip()
    elif "Email address for" in description:
        return description.split("Email address for ")[1].split(",")[0].strip()
    else:
        return "Unknown"

def summarize_thread(summarization_pipeline, emails):
    thread_content = " ".join([email['content'] for email in emails])
    input_length = len(thread_content.split())
    max_length = min(input_length, max(15, int(input_length * 0.5)))
    min_length = min(max_length, max(15, int(max_length * 0.5)))
    try:
        summary = summarization_pipeline(thread_content, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        logging.error(f"Error summarizing thread: {e}")
        return "Summary not available"


# Analyze sentiment of the conversations using a sentiment model
def analyze_sentiment(sentiment_pipeline, emails: List[Dict]) -> str:
    email_contents = " ".join([email['content'] for email in emails])
    
    try:
        sentiment_result = sentiment_pipeline(email_contents)
        sentiment = sentiment_result[0]['label']
        return {'POSITIVE': 'Positive', 'NEGATIVE': 'Negative'}.get(sentiment, 'Neutral')
    except Exception as e:
        logging.error(f"Error analyzing sentiment: {e}")
        return 'Neutral'

# Process the logs and use the LLM for tasks
def process_email_threads(input_file_path: str, output_file_path: str, summarization_pipeline, sentiment_pipeline):
    try:
        with open(input_file_path, 'r') as f, open(output_file_path, 'w') as output_file:
            for line in f:
                try:
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
                    logging.info(f"Processed thread {thread_id}")
                
                except json.JSONDecodeError as e:
                    logging.error(f"Error decoding JSON: {e}")
    
    except FileNotFoundError as e:
        logging.error(f"Input file not found: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

# Main function to kick off the analysis
def analyze():
    input_file_path = 'all_emails.jsonl'
    output_file_path = 'results.jsonl'

    # Load models for summarization and sentiment analysis
    summarization_pipeline, sentiment_pipeline = load_models()
    # Process the email threads using the loaded models
    process_email_threads(input_file_path, output_file_path, summarization_pipeline, sentiment_pipeline)