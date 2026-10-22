import json
import ollama

with open("salary_data.json", "r", encoding="utf-8") as f:
    salary_data = json.load(f)

print("Salary Assistant Ready")

while True:

    question = input("\nQuestion: ")

    if question.lower() == "exit":
        break

    prompt = f"""
You are a payroll assistant.

Use ONLY the salary data provided below.

Salary Data:
{json.dumps(salary_data, indent=2)}

Rules:
1. Use only the provided salary data.
2. Do calculations when asked.
3. Calculate totals when asked.
4. Calculate averages when asked.
5. Compare months when asked.
6. Do not make up values.
7. If data is not available, clearly say so.
8. Use indian rupees (₹) as the currency for all calculations.(provides data is in rupees)

Question:
{question}
"""

    response = ollama.chat(
        model="qwen2.5:1.5b",  # replace with your model name
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    print("\nAnswer:")
    print(response["message"]["content"])