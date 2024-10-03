### Llama-index starter tutorial
Official documentation ```https://docs.llamaindex.ai/en/stable/index.html```

### Setup
1. Fork and clone the repo ```https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo```
2. Rename ```.env.temlplate``` to ```.env``` and the the values of api keys for OpenAi and Traceloop
3. Create virtual environment ```python -m venv venv``` and activate it ```venv\scripts\activate\``` (this is windows command)
4. Install all the dependencies  ```pip install -r requirements.txt```
5. Run the server ```python main.py```
6. Make a POST request to ```http://localhost:8000/api/chat```. Example of json body:
```
{
  "messages": [
    {
      "role": "user",
      "content": "how many employees are there?"
    }
  ]
}
```

### What is llama-index
Llama-Index is a data framework for building applications based on LLM for input, structuring, and accessing private data.

### Why llama-index
Available LLMs are trained on large amounts of data but not on private data or custom knowledge bases. 
It is possible to fine-tune LLMs on your data, but:

- It can be expensive,
- Fine-tuning with new data can be challenging,
- Observability is lacking. When you ask a language model a question, it's not clear how the model arrived at its answer.
- It requires a significant amount of time.

Llama-index takes a different approach called the RAG system (Retrieval-Augmented Generation).

### What is RAG?
RAG (Retreival-Augmented Generation) is a system in which information is retrieved from its own source based on relevance compared to the question.
Procedure:

- Own data sources are loaded (documents, SQL tables, API, etc.).
- Relevant information is retrieved based on the question.
- The question is added as context.
- An answer (result) is sought from the LLM based on the entire query.

![RAG architecture](./image/basic_rag.png "RAG architecture")


Comparison with model training:

- No model training, so it is not expensive and requires less time.
- Data retrieval is on-demand, making the data always up-to-date.
- Llama-index has the ability to display the sources of retrieved information, making observation more reliable.

### Stages within RAG system
1. **Loading:** this refers to getting your data from where it lives – whether it’s text files, PDFs, another website, a database, or an API – into your pipeline. LlamaHub provides hundreds of connectors to choose from.

2. **Indexing:** this means creating a data structure that allows for querying the data. For LLMs this nearly always means creating vector embeddings, numerical representations of the meaning of your data, as well as numerous other metadata strategies to make it easy to accurately find contextually relevant data.

3. **Storing:** once your data is indexed you will almost always want to store your index, as well as other metadata, to avoid having to re-index it.

4. **Querying:** for any given indexing strategy there are many ways you can utilize LLMs and LlamaIndex data structures to query, including sub-queries, multi-step queries and hybrid strategies.

5. **Evaluation:** a critical step in any pipeline is checking how effective it is relative to other strategies, or when you make changes. Evaluation provides objective measures of how accurate, faithful and fast your responses to queries are.

Throughout this tutorial we will go through each stage of the RAG system and much more! For more information, visit the official Llama-index documentation```https://docs.llamaindex.ai/en/stable/index.html```







