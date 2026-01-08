import os
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from browser_use import Agent,Browser, BrowserConfig
from pydantic import SecretStr
from datetime import datetime
import asyncio

api_key = os.environ['ALIBABA_API_KEY']
api_base_url = 'https://dashscope-intl.aliyuncs.com/compatible-mode/v1'
api_model = 'qwen-plus'
browser_config = BrowserConfig(
                    chrome_instance_path='/usr/bin/chromium-browser',
                    disable_security=True,
                    headless=True
                )

def saveContent(user_input, agent_run_result):
    filename = datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ".txt"
    output_content = f"{user_input}\n--\n\n{agent_run_result.history[-1].result[-1].extracted_content}"
    with open(filename, 'w') as file:
        file.write(output_content)
async def main():
    while True:
        user_input = input("Enter your task or enter to leave: ")
        if (user_input == ''):
            break
        browser = Browser(config=browser_config)
        agent = Agent(
                    task=user_input,
                    use_vision=False,
                    browser=browser,
                    llm=ChatOpenAI(
                            base_url=api_base_url,
                            model=api_model,
                            api_key=SecretStr(api_key)
                        )
                )
        agent_run_result = await agent.run()
        await browser.close()
        save = input("Would you like to save the result screenshots and text? (y/N)")
        if save == 'y':
            saveContent(user_input, agent_run_result)

    print('Closing application')

if __name__ == '__main__':
    asyncio.run(main())
