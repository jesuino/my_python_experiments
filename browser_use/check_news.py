from langchain_ollama import ChatOllama
from browser_use import Agent,Browser, BrowserConfig
from pydantic import SecretStr
import asyncio

browser = Browser(
    config=BrowserConfig(
         chrome_instance_path='/usr/bin/chromium-browser'
    )
)
# Initialize the model
llm=ChatOllama(model="qwen2.5", num_ctx=16000)

# Create agent with the model
agent = Agent(
    task="Open the website https://news.google.com and summarize the headlines in Google News website",
    llm=llm,
    browser=browser
)

async def main():
    await agent.run()

    input('Press Enter to close the browser...')
    await browser.close()

if __name__ == '__main__':
    asyncio.run(main())