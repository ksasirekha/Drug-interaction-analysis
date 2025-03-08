from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load BioGPT Model
model_name = "microsoft/biogpt"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load BioGPT Model
model_name = "microsoft/biogpt"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load BioGPT Model
model_name = "microsoft/biogpt"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def analyze_drug_interaction(prescription):
    """
    Generate a structured response for drug interactions & side effects.
    """
    input_text = (
        f"Given the prescription '{prescription}', analyze possible drug interactions, "
        "side effects, and suggest safer alternatives if necessary."
    )

    # Tokenize the input
    inputs = tokenizer(input_text, return_tensors="pt")

    # Generate output with controlled randomness (temperature) and sampling
    output = model.generate(
        **inputs,
        max_length=200,  
        do_sample=True,  # Allow more natural variation in responses
        temperature=0.7,  # Reduces randomness while maintaining coherence
        top_k=50,  # Selects most relevant tokens
        repetition_penalty=1.2  # Prevents repeated phrases
    )

    # Decode the output
    return tokenizer.decode(output[0], skip_special_tokens=True)

# Test BioGPT Model
if __name__ == "__main__":
    test_prescription = "Paracetamol + Ibuprofen"
    response = analyze_drug_interaction(test_prescription)
    print("BioGPT Analysis:", response)
