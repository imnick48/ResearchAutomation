from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, List, Optional
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
import os
import feedparser
import requests

# State definition
class ResearchState(TypedDict):
    query: str
    max_results: int
    save_dir: str
    persist_directory: str
    groq_api_key: str
    groq_model_name: str
    downloaded_papers: List[str]
    vectordb_created: bool
    qa_chain: Optional[RetrievalQA]
    research_question: str
    final_answer: str
    error: Optional[str]

# Node functions
def download_papers_node(state: ResearchState) -> ResearchState:
    """Download ArXiv papers based on query"""
    try:
        query = state["query"]
        max_results = state.get("max_results", 5)
        save_dir = state.get("save_dir", "arxiv_papers")
        
        os.makedirs(save_dir, exist_ok=True)
        base_url = "http://export.arxiv.org/api/query?"
        search_query = f"search_query={query.replace(' ', '+')}&start=0&max_results={max_results}"
        # search_query = f"search_query={query.replace(' ', '+')}&start=0"
        url = base_url + search_query
        feed = feedparser.parse(url)
        
        downloaded_papers = []
        print(f"Found {len(feed.entries)} papers.")
        
        for entry in feed.entries:
            title = entry.title.strip().replace('\n', ' ')
            pdf_url = entry.links[1].href  # PDF link is usually the second link
            paper_id = entry.id.split('/')[-1]
            filename = f"{paper_id}.pdf"
            filepath = os.path.join(save_dir, filename)
            
            print(f"Downloading: {title}")
            try:
                response = requests.get(pdf_url)
                response.raise_for_status()
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                downloaded_papers.append(filepath)
            except Exception as e:
                print(f"Failed to download {title}: {e}")
        state["downloaded_papers"] = downloaded_papers
        print(f"Successfully downloaded {len(downloaded_papers)} papers")
        return state
        
    except Exception as e:
        state["error"] = f"Error downloading papers: {str(e)}"
        return state

def create_vectordb_node(state: ResearchState) -> ResearchState:
    """Create vector database from downloaded PDFs"""
    try:
        if state.get("error"):
            return state
            
        pdf_folder = state.get("save_dir", "arxiv_papers")
        persist_directory = state.get("persist_directory", "chroma_db")
        
        # Initialize embeddings
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        all_docs = []
        for file in os.listdir(pdf_folder):
            if file.endswith(".pdf"):
                filepath = os.path.join(pdf_folder, file)
                try:
                    # First check if the file is actually a PDF
                    with open(filepath, 'rb') as f:
                        header = f.read(4)
                        if header != b'%PDF':
                            print(f"File {file} is not a valid PDF (header: {header}), skipping")
                            continue
                            
                    loader = PyPDFLoader(filepath)
                    docs = loader.load()
                    all_docs.extend(docs)
                except Exception as e:
                    print(f"Error processing file {file}: {str(e)}")
                    continue
                    
        print(f"Processed {len(all_docs)} document pages from valid PDFs")
        
        if not all_docs:
            state["error"] = "No valid PDF documents found to process"
            return state
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        split_docs = text_splitter.split_documents(all_docs)
        
        vectordb = Chroma.from_documents(
            documents=split_docs,
            embedding=embeddings,
            persist_directory=persist_directory
        )
        state["vectordb_created"] = True
        print(f"Created vector database with {len(split_docs)} document chunks")
        return state
        
    except Exception as e:
        state["error"] = f"Error creating vector database: {str(e)}"
        return state

def create_qa_chain_node(state: ResearchState) -> ResearchState:
    """Create QA chain with Groq LLM"""
    try:
        if state.get("error") or not state.get("vectordb_created"):
            return state
            
        persist_directory = state.get("persist_directory", "chroma_db")
        groq_api_key = state.get("groq_api_key")
        groq_model_name = state.get("groq_model_name", "llama-3.1-8b-instant")
        
        if not groq_api_key:
            state["error"] = "Groq API key not provided"
            return state
        
        # Initialize embeddings (same as used in vectordb creation)
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
        retriever = vectordb.as_retriever(search_kwargs={"k": 5})

        llm = ChatGroq(
            model=groq_model_name,
            api_key=groq_api_key,
            temperature=0.1
        )
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True
        )
        
        state["qa_chain"] = qa_chain
        print("QA chain created successfully")
        return state
        
    except Exception as e:
        state["error"] = f"Error creating QA chain: {str(e)}"
        return state

def answer_question_node(state: ResearchState) -> ResearchState:
    """Answer the research question using the QA chain"""
    try:
        if state.get("error") or not state.get("qa_chain"):
            return state
            
        research_question = state.get("research_question", state.get("query", ""))
        qa_chain = state["qa_chain"]
        
        if not research_question:
            state["error"] = "No research question provided"
            return state
        
        print(f"Answering question: {research_question}")
        result = qa_chain(research_question)
        
        state["final_answer"] = result['result']
        print("Research question answered successfully")
        return state
        
    except Exception as e:
        state["error"] = f"Error answering question: {str(e)}"
        return state

def error_handler_node(state: ResearchState) -> ResearchState:
    """Handle errors and provide feedback"""
    error = state.get("error", "Unknown error occurred")
    print(f"Error encountered: {error}")
    state["final_answer"] = f"Process failed with error: {error}"
    return state

# Router function to determine next step
def router(state: ResearchState) -> str:
    if state.get("error"):
        return "error_handler"
    elif not state.get("downloaded_papers"):
        return "download_papers"
    elif not state.get("vectordb_created"):
        return "create_vectordb"
    elif not state.get("qa_chain"):
        return "create_qa_chain"
    elif not state.get("final_answer"):
        return "answer_question"
    else:
        return END

# Create the workflow
def create_research_workflow():
    """Create and return the LangGraph workflow"""
    workflow = StateGraph(ResearchState)
    
    # Add nodes
    workflow.add_node("download_papers", download_papers_node)
    workflow.add_node("create_vectordb", create_vectordb_node)
    workflow.add_node("create_qa_chain", create_qa_chain_node)
    workflow.add_node("answer_question", answer_question_node)
    workflow.add_node("error_handler", error_handler_node)
    
    # Add conditional edges based on state
    workflow.add_conditional_edges(
        "download_papers",
        router,
        {
            "create_vectordb": "create_vectordb",
            "error_handler": "error_handler"
        }
    )
    
    workflow.add_conditional_edges(
        "create_vectordb",
        router,
        {
            "create_qa_chain": "create_qa_chain",
            "error_handler": "error_handler"
        }
    )
    
    workflow.add_conditional_edges(
        "create_qa_chain",
        router,
        {
            "answer_question": "answer_question",
            "error_handler": "error_handler"
        }
    )
    
    workflow.add_conditional_edges(
        "answer_question",
        router,
        {
            END: END,
            "error_handler": "error_handler"
        }
    )
    
    workflow.add_edge("error_handler", END)
    
    # Set entry point
    workflow.set_entry_point("download_papers")
    
    return workflow

# Example usage
def run_research_workflow(
    query: str,
    research_question: str,
    groq_api_key: str,
    max_results: int = 5,
    groq_model_name: str = "llama-3.1-8b-instant"
):
    """Run the complete research workflow"""
    
    # Create workflow
    workflow = create_research_workflow()
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)
    # Clean the query for folder name
    clean_query = query.lower().replace(' ', '_').replace('&', 'and')
    # Initial state
    initial_state = {
        "query": query,
        "research_question": research_question,
        "max_results": max_results,
        "save_dir": f"arxiv_papers/{clean_query}",
        "persist_directory": f"chroma_db/{clean_query}",
        "groq_api_key": groq_api_key,
        "groq_model_name": groq_model_name,
        "downloaded_papers": [],
        "vectordb_created": False,
        "qa_chain": None,
        "final_answer": "",
        "error": None
    }
    
    # Run the workflow
    print("Starting research workflow...")
    config = {"configurable": {"thread_id": "research_thread"}}
    final_state = app.invoke(initial_state, config)
    
    return final_state

# # Example usage
# if __name__ == "__main__":
#     # Example configuration
#     GROQ_API_KEY = "your-groq-api-key-here"  # Replace with your actual API key
    
#     result = run_research_workflow(
#         query="arabic transformers",
#         research_question="What are Arabic transformers and their applications?",
#         groq_api_key=GROQ_API_KEY,
#         max_results=3
#     )
    
#     print("\n" + "="*50)
#     print("FINAL RESULT:")
#     print("="*50)
#     print(result["final_answer"])
    
#     if result.get("error"):
#         print(f"\nError: {result['error']}")