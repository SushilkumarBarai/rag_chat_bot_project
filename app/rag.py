import requests
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores.utils import filter_complex_metadata

class ChatCSV:
    def __init__(self, persist_directory: str = "candidate_chroma_db"):
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=100)

        # ✅ LLaMA 2 chat-style prompt
        self.system_prompt = (
            "You are an HR assistant. Based on the resume data provided in the context, "
            "identify up to 3 most suitable candidates for the query.\n\n"
            "Instructions:\n"
            "- If the user greets you, greet the user back with full respect.\n"
            "- Provide a short summary for each selected candidate.\n"
            "- Use the format below.\n"
            "- Do NOT include explanations.\n"
            "- Do NOT write paragraphs.\n"
            "- ONLY include relevant candidates.\n\n"
            "Format:\n"
            "CandidateID: <ID>\n"
            "Summary: <One or two line description highlighting relevant skills and experience>\n\n"
            "Example:\n"
            "CandidateID: 103\n"
            "Summary: 5 years of experience in SQL and Power BI. Built dashboards and reports for retail clients.\n\n"
            "CandidateID: 109\n"
            "Summary: Data analyst with strong SQL skills and experience using Power BI for financial reporting."
        )

        self.vector_store = None
        self.persist_directory = persist_directory

    def ingest(self, csv_file_path: str):
        loader = CSVLoader(
            file_path=csv_file_path,
            encoding='utf-8',
            source_column="Resume",
            metadata_columns=["CandidateID"]
        )
        data = loader.load()
        chunks = self.text_splitter.split_documents(data)
        chunks = filter_complex_metadata(chunks)

        self.vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=FastEmbedEmbeddings(),
            persist_directory=self.persist_directory
        )

    def model_api_call(self, query: str, context: str):
        # ✅ Format for LLaMA 2 Chat
        messages = [
            {"role": "system", "content": self.system_prompt},
            {
                "role": "user",
                "content": f"Query: {query}\n\nContext:\n{context}\n\nAnswer:"
            }
        ]

        url = "http://localhost:11434/api/chat"
        headers = {"Content-Type": "application/json"}
        data = {
            "model": "llama2:chat",
            "messages": messages,
            "stream": False
        }

        response = requests.post(url, json=data, headers=headers)
        response_data = response.json()

        if response.status_code == 200:
            if 'message' in response_data:
                return response_data['message']['content']
            elif 'content' in response_data:
                return response_data['content']
            else:
                return "Error: No content in response."
        else:
            return f"Error: {response_data.get('error', 'Unknown error')}"

    def ask(self, query: str):
        if not self.vector_store:
            return "Please ingest a CSV file first using the `ingest()` method."

        results = self.vector_store.similarity_search(query, k=5)
        if not results:
            return "No relevant context found in the database."

        context = " ".join([document.page_content for document in results])
        print("Context Used:\n", context)

        return self.model_api_call(query, context)

    def clear(self):
        self.vector_store = None
