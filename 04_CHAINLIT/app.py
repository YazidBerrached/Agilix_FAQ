
import chainlit as cl
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.agent import Agent, AgentMemory
from chainlit import user_session
from rich.pretty import pprint
from agno.models.groq import Groq
from agno.models.openrouter import OpenRouter
from dotenv import main
from teams import *
import os
from agno.models.openai import OpenAIChat
from agno.embedder.openai import OpenAIEmbedder
from agno.embedder.mistral import MistralEmbedder
from teams import knowledge_base_customer
from pydantic import BaseModel

class response_agent(BaseModel):
    id: str
    content: str
    image: str
main.load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
db_url = "postgresql+psycopg://neondb_owner:npg_CzA3eXY9cwBs@ep-spring-sun-a52z84u0-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"

agent = Agent(
    model=model_openai_teams_agent,
    description="You are a customer assistant at POSÉIDON SPA.",
    role=(
        "You are a customer assistant at POSÉIDON SPA. Your role is to assist users by answering their inquiries, "
        "providing detailed information, and ensuring an excellent customer experience. "
        "IMPORTANT: Any text containing Markdown syntax such as '![motorisation](public/img/motorisation.png)' "
        "must be displayed AS-IS, without rendering it as an image."
    ),
    instructions=[
        "Réponds toujours en français.",
        "Ne transforme jamais les textes Markdown en images ou liens.",
        "Si tu vois un texte contenant '![...]', affiche-le tel quel, sans le modifier.",
        "Utilise des backticks (`) ou un bloc de code ``` pour afficher du Markdown brut si nécessaire.",
        "Use knowledge_base_technician",
        "use the local lancedb",
        "include all the records from the lancedb",
        "Always include sources in your response", 
        "DISPLAY IMAGES AS IS, DO NOT RENDER THEM",
        "tu dois afficher les images si existe dans la knowledge base",
        "Génère un texte en Markdown affichant une image avec cette syntaxe : ![image](public/img/images1.png), sans encadrer le texte avec des triple backticks (```)."
        ],
    team=[technician_agent],
    markdown=True,  # Permettre le Markdown pour les autres parties du texte
    debug_mode=True,
    retries=3,
)
@cl.set_starters
async def set_starters():
    questions = [
        "je suis a GAILLAC, et je veux acheter un spa, y a t il un de vos partenaire dans cette ville?",
        "dans le spatouch3, je veux savoir le fonctionnement des icons sur l'écran",
        "dans le modele TP400, je veux rendre le mode de chauffage en mode : pret",
        "Auatant que technicien, quell sont les couleur de la coque ?",
        "A partir du mode réglage CHAUFFAGE du système balboa comment faire apparaître dans la rubrique « mode » celui prêt en repos RR?",
        "Le sens d’ouverture de la porte est-il modifiable ?",
        "Est-ce que les branchements en Plug and Play demande de réaliser un délestage sur les machines ?",
        "Y a-t-il le module wifi intégré pour le spa Orion ?",
        "Y a-t-il une distance à respecter entre la paroi du sauna et le mur ?",
        "Y a-t-il une distance à respecter entre le plafond et le toit du sauna ?",
        "Le sauna est-il livré avec le kit accessoire ? Sur le catalogue il est noté 1 thermomètre."
    ]

    return [
        cl.Starter(
            label=value,
            message=value
        ) for value in questions
    ]


@cl.on_message
async def on_message(message: cl.Message):
    mh = cl.user_session.get("message_history", [])
    msg = cl.Message("", author="AI Agent")
    final_msg_content = ""
    prompt_user =message.content+ " ,n'oublie pas d'afficher les images."
    for rest in agent.run(prompt_user, stream=True):
        
        await msg.stream_token(rest.content, False)  
    await msg.update()
    
    # await cl.Message(content = "![spatouch3](public/img/sp_bp_systems_spatouch3_icon_explained_3.png)").send()
    print("~"*100)


