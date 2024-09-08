from chat_request import send_openai_request

def summarize_transcription(transcription):
    try:
        prompt = f"Please summarize the following transcription in about 500 words:\n\n{transcription}"
        summary = send_openai_request(prompt)
        return summary
    except Exception as e:
        raise Exception(f"Error summarizing transcription: {str(e)}")

def answer_question(question, transcription):
    try:
        summary = summarize_transcription(transcription)
        prompt = f'''Based on the following summarized transcription, please answer the question. If the answer cannot be determined from the transcription, say "I cannot answer this question based on the given transcription."

Summarized Transcription:
{summary}

Question: {question}

Answer:'''

        answer = send_openai_request(prompt)
        return answer
    except Exception as e:
        raise Exception(f"Error answering question: {str(e)}")
