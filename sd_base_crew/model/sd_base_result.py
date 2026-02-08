from pydantic import BaseModel, Field
class SDBaseFullGenerationScript(BaseModel):
    description: str = Field(description="""
        A detailed, structured summary of the generation plan. This summary MUST explicitly list:
    1. The name of the Root Table (e.g., 'Author') and its PK field (e.g., 'author_id').
    2. for all other tables: The name of Table (e.g., 'Book'), its PK (e.g., 'book_id'), and its FK field (e.g., 'author_id').
    3. A confirmation of the sequential generation order required to maintain referential integrity.
        """)
    sql_script: str = Field(description="""
        The sql Script generated
        """)
