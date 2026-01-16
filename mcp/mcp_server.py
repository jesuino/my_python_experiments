from pydantic import Field
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base



mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

def doc_not_found(doc_id: str):
    raise ValueError(f"Document {doc_id} not found.")

# TODO: Write a tool to read a doc

@mcp.tool(name="read_doc",
          description="Read the contents of a document by its ID and returns the text. ")
def read_doc(
    doc_id: str = Field(description="The ID of the document to read")
) -> str:
    if doc_id in docs:
        return docs[doc_id]
    doc_not_found(doc_id)


# TODO: Write a tool to edit a doc
@mcp.tool(name="edit_doc",
          description="Edit the contents of a document by its ID and new content.")
def edit_doc(
    doc_id: str = Field(description="The ID of the document to edit"),
    old_content: str = Field(description="The old content for the document"),
    new_content: str = Field(description="The new content for the document")
) -> str:
    if doc_id in docs:
        docs[doc_id] = docs[doc_id].replace(old_content, new_content)
        return docs[doc_id]
    doc_not_found(doc_id)

# TODO: Write a resource to return all doc id's

@mcp.resource(
      uri="docs://documents",
      mime_type="application/json",
      description="Return a list of all document IDs available.")
def docs_ids() -> list[str]:
    return list(docs.keys())

# TODO: Write a resource to return the contents of a particular doc
@mcp.resource(
      uri="docs://document/{doc_id}",
      mime_type="text/plain",
      description="Return the contents of a document by its ID.")
def read_doc_resource(doc_id: str) -> str:
    if doc_id in docs:
        return docs[doc_id]
    doc_not_found(doc_id)
# TODO: Write a prompt to rewrite a doc in markdown format
@mcp.prompt(
    name="format",
    description="Rewrite the given document content in markdown format."
)
def format_doc(
    doc_id: str = Field(description="The ID of the document to format")
) -> list[base.Message]:
    prompt = f"""
    Your goal is to reformat a document to be written with markdown syntax.
    
    the id of the document you need to format is:
    
    <document_id>{doc_id}</document_id>
    
    Add in headers, bullet points, tables, etc as necessary. Feel free to add
    
    Use the 'edit_doc' tool to edit the document.
    """
    return [
        base.UserMessage(prompt)
    ]
# TODO: Write a prompt to summarize a doc




if __name__ == "__main__":
    mcp.run(transport="stdio")
