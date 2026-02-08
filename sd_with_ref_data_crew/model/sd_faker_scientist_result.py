from pydantic import BaseModel, Field
from typing import List, Optional
class SDFakerScientistResult(BaseModel):
    description: str = Field(description="""
        A detailed, structured summary of the generation plan. This summary MUST explicitly list:
    1. The name of the Root Table (e.g., 'Author') and its PK field (e.g., 'author_id').
    2. for all other tables: The name of Table (e.g., 'Book'), its PK (e.g., 'book_id'), and its FK field (e.g., 'author_id').
    3. A confirmation of the sequential generation order required to maintain referential integrity.
        """)
    sql_script: str = Field(description="""
        The sql Script generated
        """)

class SDFakerResult(BaseModel):
    python_code: str = Field(description="""
      python code
        """)
    planned_statements_description: str = Field(description="""
        A calculation of INSERT statements for each tables
        """)


class StructuredExecutionPlan(BaseModel):
    """
    Model for an agent's output that provides a clear, sequential plan
    and the final generated content.
    """

    instructions: List[str] = Field(
        description="""
        A structured list of sequential instructions required to complete the task. 
        Each list element represents a single logical step or specific action 
        that was executed, for example: 
        1. 'Verify table dependency order (Client -> Order).'
        2. 'Process Reference Data for Client table.'
        3. 'Execute the nested generation loop for Order inserts.'
        """
    )

    generated_content: Optional[str]  = Field(
        description="""
        The final technical artifact produced by the agent, such as the complete 
        SQL script, the resulting Python code, or a complex configuration file.
        """
    )

    summary_report: Optional[str] = Field(
        description="""
        A concise summary of the key results and metrics from the execution, 
        for example: '150 total records generated across 5 tables, with 
        10 Reference Data lookups and 140 New Data inserts.'
        """
    )