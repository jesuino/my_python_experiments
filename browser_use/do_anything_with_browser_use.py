import os
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from browser_use import Agent,Browser, BrowserConfig
from pydantic import SecretStr
import asyncio

api_key=os.environ['DEEPSEEK_API_KEY']
browser = Browser(
    config=BrowserConfig(
         
         chrome_instance_path='/usr/bin/chromium-browser',
         disable_security=True,
         headless=True
    )

)
llm = ChatOpenAI(base_url='https://api.deepseek.com/v1', 
                 model='deepseek-chat', 
                 api_key=SecretStr(api_key))

agent = Agent(
    task=input('Enter what you want to do with browser_use: '),
    llm=llm,
    browser=browser,
    use_vision=False
)

async def main():
    await agent.run()

    input('Done! Press enter to finish.')
    await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
