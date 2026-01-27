from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch
import threading

# Use FLAN-T5 Base for a good balance of speed and quality
MODEL_NAME = "google/flan-t5-base"
tokenizer = None
model = None
model_lock = threading.Lock()

def init_t5():
    global tokenizer, model
    with model_lock:
        if model is None:
            print(f"Loading {MODEL_NAME} model...")
            tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)
            # Force CPU for reliability if multiple models are loaded
            device = "cpu" 
            model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME).to(device)
            print(f"{MODEL_NAME} model loaded on {device}.")

def summarize_with_t5(text, max_length=150, custom_prompt=None):
    try:
        if model is None:
            init_t5()
        
        device = "cpu"
        
        # Use custom prompt if provided, otherwise fallback to default
        if custom_prompt:
            input_text = custom_prompt.format(text=text)
        else:
            input_text = f"Summarize the following financial news article in 3 sentences:\n\n{text}"
        
        inputs = tokenizer(input_text, return_tensors="pt", truncation=True, max_length=512).to(device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs, 
                max_new_tokens=max_length,
                num_beams=4,
                length_penalty=2.0,
                early_stopping=True
            )
        
        summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return summary
    except Exception as e:
        print(f"T5 Summarization Error: {e}")
        return f"Error generating summary with T5: {str(e)}"

if __name__ == "__main__":
    test_text = "The Federal Reserve kept interest rates steady on Wednesday but took a major step toward lowering them in the coming months in a policy statement that gave a nod to inflation's decline. The central bank's latest move leaves its benchmark rate in a range between 5.25% and 5.5%, where it has been since July."
    print("Testing T5 Summarization...")
    print(summarize_with_t5(test_text))
