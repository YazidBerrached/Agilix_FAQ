from agno.agent import Agent
from llm_models import *
from agno.agent import Agent

from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.knowledge.pdf import PDFKnowledgeBase, PDFReader
from agno.vectordb.pgvector import PgVector, SearchType
from agno.embedder.mistral import MistralEmbedder
import os
from agno.embedder.openai import OpenAIEmbedder
from dotenv import main
main.load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
db_url = "postgresql+psycopg://neondb_owner:npg_CzA3eXY9cwBs@ep-spring-sun-a52z84u0-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"

knowledge_base_customer = PDFUrlKnowledgeBase(
    # Read PDF from this URL

    # Store embeddings in the `ai.recipes` table
    vector_db=PgVector(table_name="poseidon_knwld_tbl", db_url=db_url,search_type=SearchType.hybrid ,embedder=OpenAIEmbedder()  ),
)


knowledge_base_technician = PDFKnowledgeBase(
    # Read PDF from this URL
    path="data/technician_pdfs/",
    # Store embeddings in the `ai.recipes` table
    vector_db=PgVector(
        table_name="pdf_documents",
        db_url=db_url,
        embedder=OpenAIEmbedder(),
        search_type=SearchType.hybrid,
    ),
    reader=PDFReader(chunk=True),
    
)


#knowledge_base_technician.load(recreate=False)
costumer_assistant = Agent(
    name="Customer assistant",
    model=model_openai_teams_agent,
    role="You are a customer assistant at POSÉIDON SPA. Your role is to assist customers by answering their inquiries, providing detailed information about products, and ensuring an excellent customer experience. Your primary focus is on the end buyers, helping them choose the right products, understand pricing, and navigate any concerns they may have.",
    description="You are a customer assistant at POSÉIDON SPA  specialising on general infomation about products and services of your company.",
    instructions=["Tu es un assistant virtuel professionnel, chaleureux et engageant. Tu dois répondre aux utilisateurs de manière naturelle et fluide, comme un vrai assistant humain. Utilise un langage clair et courtois, évite les formulations robotiques. Si tu ne connais pas la réponse, réponds poliment que tu ne sais pas. Réponds toujours dans la langue de l'utilisateur. ", 'if you  have image related question, please provide the image'],
    knowledge=knowledge_base_customer,
    debug_mode=True
    
)

technician_agent = Agent(
    name ="Technician",
    model=model_openai_teams_agent,
    description='You are technician assistant that works at POSÉIDON SPA',
    role="Your main role is to give help to maintain and fix errors of the 'POSÉIDON SPA' products using the information you have",
    knowledge=knowledge_base_technician,
    debug_mode=True
)

# supportB2B_assistant = Agent(
#     name="Support B2B",
#     model=model_openai,
#     description="You are an after-sales B2B service assistant for POSÉIDON SPA",
#     role="You are an after-sales service assistant for POSÉIDON SPA, dedicated to supporting the company's business partners. Your role is to efficiently handle their inquiries and those of their clients by providing clear and precise information. You assist them with questions related to discounts, service details, and any other relevant business matters. Maintain a professional, courteous, and solution-oriented approach in all interactions.",
#     tools=[],
# )

# supportB2C_assistant = Agent(
#     name="Support B2C",
#     model=model_openai,
#     description="You are an after-sales B2C service assistant for POSÉIDON SPA",
#     role="You are a customer service assistant for POSÉIDON SPA. Your mission is to assist customers by answering their questions and guiding them through their experience with our products and services. Provide clear, accurate, and helpful information while maintaining a friendly and professional tone. Your goal is to ensure customer satisfaction by offering efficient solutions and creating a positive brand experience.",
#     tools=[],
# )
