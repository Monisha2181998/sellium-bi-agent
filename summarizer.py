import json
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from prompt_template import SUMMARY_PROMPT

load_dotenv()

def load_pdf(pdf_path: str) -> str:
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(pages)
    text = "\n\n".join([c.page_content for c in chunks[:2]])
    return text

def summarize(pdf_path: str) -> dict:
    print(f"Loading PDF: {pdf_path}")
    text = load_pdf(pdf_path)
    llm = OllamaLLM(model="mistral", temperature=0)
    prompt = PromptTemplate(
        input_variables=["text"],
        template=SUMMARY_PROMPT
    )
    chain = prompt | llm | StrOutputParser()
    print("Calling Mistral (running locally)...")
    print("Please wait, this takes 30-60 seconds...")
    response = chain.invoke({"text": text})
    start = response.find("{")
    end = response.rfind("}") + 1
    json_str = response[start:end]
    result = json.loads(json_str)
    return result

def save_output(result: dict, pdf_path: str):
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    filename = Path(pdf_path).stem + "_summary.json"
    output_path = output_dir / filename
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"Summary saved to: {output_path}")
    return str(output_path)