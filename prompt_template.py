SUMMARY_PROMPT = """
You are a business intelligence AI assistant.
Analyze the following text extracted from a business report PDF
and create a structured summary in JSON format.

Reply ONLY with valid JSON. No text before or after it.

Format:
{{
  "title": "Document title or topic",
  "key_findings": ["Finding 1", "Finding 2", "Finding 3"],
  "financial_highlights": ["Highlight 1", "Highlight 2"],
  "risks": ["Risk 1", "Risk 2"],
  "recommendation": "One short strategic recommendation"
}}

Text:
{text}
"""