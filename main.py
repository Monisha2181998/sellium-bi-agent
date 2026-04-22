import sys
import json
import requests
from summarizer import summarize, save_output

def send_to_n8n(result: dict):
    try:
        webhook_url = "http://localhost:5678/webhook-test/bi-agent"
        response = requests.post(webhook_url, json=result)
        print(f"N8N response: {response.status_code}")
    except Exception as e:
        print(f"N8N not running yet, skipping: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py path/to/report.pdf")
        sys.exit(1)

    pdf_path = sys.argv[1]

    print("=" * 40)
    print("  Business Intelligence Agent")
    print("  Powered by LangChain + Mistral")
    print("=" * 40)

    result = summarize(pdf_path)

    print("\n===== SUMMARY =====")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print("=" * 40)

    save_output(result, pdf_path)
    send_to_n8n(result)

    print("\nDone! Check your output folder.")

if __name__ == "__main__":
    main()