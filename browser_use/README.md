Browser Use tests
--

My tests with [Browser Use](https://browser-use.com/) API.

To run locally you must have the following tools:

* python 3 and pip
* [ollama](https://ollama.com/) if running local models

Also make sure to install the required dependencies:

```
pip install -r requirements.txt 
```


Modify the code according your environment:


* The Browser class muust point the browse that will be used by `browser_use`. I use linux and have a local Chromium, you may have to edit it accordingly
* The `llm` object contains the LLM configuration. It can be a ollama service running locally or a remote LLM provide such as Qwen, DeepSeek and others. If you are using ollama make sure that you point to a llm that you have pulled locally
* The Agent class lets you configure the prompt


