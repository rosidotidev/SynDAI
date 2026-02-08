import warnings
from sd_base_crew.sd_base_crew import SDBaseCrew
from sd_base_crew.sd_base_pydantic_crew import SDBasePydanticCrew

from dotenv import load_dotenv

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run_sd(instruction='create 3 authors and 2 books for each author, produce insert statements', schema_file='./data/schema.sql'):
    """
    Run the crew.
    """
    load_dotenv()
    inputs = {
        'instruction': instruction,
        'schema_file': schema_file
    }

    output = SDBaseCrew().crew().kickoff(inputs=inputs)
    print(output.token_usage)

def run_pydantic_base_sd(instruction='create 3 authors and 2 books for each author, produce insert statements', schema_file='./data/schema.sql'):
    """
    Run the crew.
    """
    load_dotenv()
    inputs = {
        'instruction': instruction,
        'schema_file': schema_file
    }

    output = SDBasePydanticCrew().crew().kickoff(inputs=inputs)
    print(output.pydantic.description)
    print(output.pydantic.sql_script)
    print(output.token_usage)

if __name__ == "__main__":
    load_dotenv()
    run_sd("For DBMS H2, Create 3 authors 4 books for each author and 2 comment for each book", schema_file='./data/schema_x1_h2.sql')
    #run_sd("Create a school, 3 classroom for that school, 5 students for each class, 2 activity for each student", schema_file='./data/school_schema_v1.sql')
    #run_pydantic_base_sd("Create a school, 3 classroom for that school, 5 students for each class, 2 activity for each student", schema_file='./data/school_schema_v1.sql')