import requests
from bs4 import BeautifulSoup
import  streamlit as st
from langchain_ollama import OllamaLLM


#Load AI Model
llm = OllamaLLM(model = 'mistral')

# Write a function to scrape the website
def scrape_website(url):
	try:
		st.write("scrapping website :{url}")
		headers = {"User-Agent": "Mozilla/5.0"}
		response = requests.get(url , headers = headers)

		if response.status_code != 200:
			return f"Failed to fetch {url}"

		# Extract the tech content
		soup = BeautifulSoup(response.text , "html.parser")
		paragraphs = soup.find_all("p")
		text = "".join([p.get_text() for p in paragraphs])

		return text[:2000] # Limit character to avoid overloading ai
	except Exception as e:
		return f" Error {str(e)}"

# Function to summarise content using Ai
def summarize_content(content):
	st.write("summarizeing Content...")
	return llm.invoke(f"summarize the following content\n\n{content[:1000]}")

#Streamlit Web Ui
st.title("AI Powered web scrapper")
st.write("Enter the website URL below and get the summarised version")

# User unput

url =st.text_input("Enter Website URL")
if url:
	content =scrape_website(url)

	if "Failed" in content or "Error" in content:
		st.write(content)
	else:
		summary = summarize_content(content)
		st.subheader("Website summarise")
		st.write(summary)

