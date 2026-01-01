import streamlit as st
import os
import pandas as pd
import joblib
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
st.set_page_config(page_title="TeknoMarket Asistanı", page_icon="🤖", layout="wide")

EXCEL_PATH = "data/tek_market.xlsx"
PDF_PATH = "data/teknik_kilavuz.pdf"
MODEL_PATH = "data/lr_intent_model_6.pkl"      
VECTORIZER_PATH = "data/tfidf_vectorizer_6.pkl" 

@st.cache_resource
def load_models():
    try:
        vec = joblib.load(VECTORIZER_PATH)
        model = joblib.load(MODEL_PATH)
        return vec, model
    except Exception as e:
        st.error(f"Model yüklenirken hata: {e}. Lütfen önce 'python model.py' çalıştırın.")
        return None, None

@st.cache_data
def load_excel():
    try:
        df = pd.read_excel(EXCEL_PATH)
        df['Search_Name'] = df['Urun_Adi'].astype(str).str.lower()
        return df
    except Exception as e:
        st.error(f"Excel hatası: {e}")
        return pd.DataFrame()

@st.cache_resource
def setup_rag():
    if not os.path.exists(PDF_PATH):
        return None
    
    loader = PyPDFLoader(PDF_PATH)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = splitter.split_documents(docs)
    
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    vectorstore = Chroma.from_documents(splits, embeddings, persist_directory="./chroma_db")
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Sen uzman bir teknoloji asistanısın. Şu teknik kılavuza göre cevap ver: {context}"),
        ("human", "{input}")
    ])
    
    return create_retrieval_chain(vectorstore.as_retriever(), create_stuff_documents_chain(llm, prompt))

vectorizer, intent_model = load_models()
df_products = load_excel()
rag_chain = setup_rag()

def get_response(query):
    if vectorizer and intent_model:
        query_vec = vectorizer.transform([query])
        intent = intent_model.predict(query_vec)[0]
    else:
        intent = "unknown"
    
    query_lower = query.lower()
    
    if intent == "greeting":
        return "Merhaba! TeknoMarket'e hoş geldiniz. Size telefonlar, bilgisayarlar veya teknik sorunlar hakkında yardımcı olabilirim. 👋"
    
    elif intent == "goodbye":
        return "Görüşmek üzere! Teknolojiyle kalın. 🔌"
    
    elif intent == "ask_price" or intent == "ask_stock":
        found_row = None
        for index, row in df_products.iterrows():
            if row['Search_Name'] in query_lower: # Örn: "iphone 15" soruda geçiyor mu?
                found_row = row
                break
        
        if found_row is not None:
            stok_durum = "✅ Var" if str(found_row['Stok']) == "Var" else "❌ Tükendi"
            
            if intent == "ask_price":
                return f"🏷️ **{found_row['Urun_Adi']}** fiyatı: **{found_row['Fiyat']} TL**. (Marka: {found_row['Marka']})"
            else: # ask_stock
                return f"📦 **{found_row['Urun_Adi']}** stok durumu: **{stok_durum}**. ({found_row['Depolama']})"
        else:
            return "Sorduğunuz ürünü listemizde bulamadım. Tam adını yazar mısınız? (Örn: iPhone 15, Dyson V15)"

    elif intent == "tech_support":
        if rag_chain:
            with st.spinner("Teknik kılavuz inceleniyor..."):
                result = rag_chain.invoke({"input": query})
                return f"🔧 **Teknik Destek:**\n{result['answer']}"
        else:
            return "Teknik destek kılavuzuna şu an ulaşılamıyor."
            
    else:
        if rag_chain:
            result = rag_chain.invoke({"input": query})
            return result['answer']
        return "Ne demek istediğinizi tam anlayamadım. Fiyat mı soruyorsunuz yoksa teknik destek mi?"

st.title("🤖 TeknoMarket AI Asistanı")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Merhaba! iPhone fiyatlarını sorabilir veya 'Telefon suya düştü' gibi teknik sorular yöneltebilirsiniz."}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if user_input := st.chat_input("Sorunuzu yazın..."):
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    ai_response = get_response(user_input)
    
    st.chat_message("assistant").write(ai_response)
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

    with st.sidebar:
        st.subheader("🕵️ Arka Plan Analizi")
        if vectorizer and intent_model:
            vec = vectorizer.transform([user_input])
            pred = intent_model.predict(vec)[0]
            st.info(f"Algılanan Niyet (Intent): **{pred}**")