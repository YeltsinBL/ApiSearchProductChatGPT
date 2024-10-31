import os
from dotenv import load_dotenv
# from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI

load_dotenv()

#     """Conexión a la BD"""
db_uri = f"mysql+mysqlconnector://{os.environ['MYSQL_USER']}:{os.environ['MYSQL_PASSWORD']}@{os.environ['MYSQL_HOST']}:{os.environ['MYSQL_PORT']}/{os.environ['MYSQL_DATABASE']}"
print(db_uri)
db  = SQLDatabase.from_uri(db_uri)

def get_sql_chain():
    """Plantilla para la conexión a SQL Chain"""
    template = """
    You are a data analyst at a company. You are interacting with a user who is asking questions about products in the company's database.
    Based on the table schema below, write a SQL query that answers the user's question, but always include all the product fields specified below, regardless of the specific information requested by the user.
    
    <SCHEMA>{schema}</SCHEMA>
    
    Conversation History: {chat_history}
    
    Make sure your query always includes the following fields from the productos table: id, nombre, descripcion, precio, stock, descuento, popularidad, categorianombre, and marcanombre. Use this query as a base for all answers, even if the user only asks for counts or specific information:\
    SELECT p.id, p.nombre, p.descripcion, p.precio, p.stock, p.descuento, p.popularidad, c.nombre as "categorianombre", m.nombre as "marcanombre"\
    FROM ecommerce.productos p LEFT JOIN ecommerce.categorias c ON p.categoria_id = c.id LEFT JOIN ecommerce.marcas m ON p.marca_id = m.id

    
    This base query should be included in all responses. For example:
    
    Question: ¿Cuáles son los 3 productos más populares?
    SQL Query: SELECT p.id, p.nombre, p.descripcion, p.precio, p.stock, p.descuento, p.popularidad, 
                      c.nombre as "categorianombre", m.nombre as "marcanombre"
               FROM ecommerce.productos p
               LEFT JOIN ecommerce.categorias c ON p.categoria_id = c.id
               LEFT JOIN ecommerce.marcas m ON p.marca_id = m.id
               GROUP BY p.id ORDER BY p.popularidad DESC LIMIT 3;

    Question: Los 10 primeros productos
    SQL Query: SELECT p.id, p.nombre, p.descripcion, p.precio, p.stock, p.descuento, p.popularidad, 
                      c.nombre as "categorianombre", m.nombre as "marcanombre"
               FROM ecommerce.productos p
               LEFT JOIN ecommerce.categorias c ON p.categoria_id = c.id
               LEFT JOIN ecommerce.marcas m ON p.marca_id = m.id
               LIMIT 10;

    Your turn:

    Question: {question}
    SQL Query:
    """

    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatOpenAI(verbose=False)

    def get_schema(_):
        """Obtener información de la tabla"""
        return db.get_table_info()
    return (
        RunnablePassthrough.assign(schema=get_schema)
        | prompt
        | llm
        | StrOutputParser()
    )

# def get_response(user_query: str, db: SQLDatabase, chat_history: list):
#     """Respuesta"""
#     sql_chain = get_sql_chain()
#     print("Decimo", sql_chain.invoke({
#         "question": user_query,
#         "chat_history": chat_history,
#     }))

#     template = """
#         You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
#         Based on the table schema below, question, sql query, and sql response, write a natural language response.
#         <SCHEMA>{schema}</SCHEMA>

#         Conversation History: {chat_history}
#         SQL Query: <SQL>{query}</SQL>
#         User question: {question}
#         SQL Response: {response}"""

#     prompt = ChatPromptTemplate.from_template(template)
#     llm = ChatOpenAI()
#     chain = (
#         RunnablePassthrough.assign(query=sql_chain).assign(
#             schema=lambda _: db.get_table_info(),
#             response=lambda vars: db.run(vars["query"]),
#         )
#         | prompt
#         | llm
#         | StrOutputParser()
#     )
#     print("Treceavo", chain)

#     return chain.invoke({
#         "question": user_query,
#         "chat_history": chat_history,
#     })

# history = []
# encendido = True
# while encendido:
#     user_query = input("") # "muestrame todos los productos" # st.chat_input("Type a message...")

#     if user_query is not None and user_query.strip() != "":
#         history.append(HumanMessage(content=user_query))
#         response = get_response(user_query, db, history)
#         print("Respuesta Final", response)
#         history.append(AIMessage(content=response))

#     print(history)
