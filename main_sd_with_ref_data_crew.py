import warnings
from sd_with_ref_data_crew.sd_with_ref_data_crew import SDWithRefDataCrew

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

    output = SDWithRefDataCrew().crew().kickoff(inputs=inputs)
    print("##################################")
    print("##################################")
    print("##################################")
    print(output.tasks_output[0])
    print("##################################")
    print(output.tasks_output[1])
    print("##################################")
    print(output.tasks_output[2])
    print("##################################")
    #print(output.pydantic.python_code)
    #print(output.pydantic.planned_statements_description)
    #print(output.pydantic.description)
    #print(output.pydantic.sql_script)
    print(output.raw)
    print(output.token_usage)

if __name__ == "__main__":
    load_dotenv()
    instructions="""
    create other 10 classrooms for 3 schools, 15 students for that classes, 2 activity for that students
    - school table is reference data you MUST use a cursor to extract 3 rows
    """

    instructions_v1 = """
        create 1000 schools, create 10 classrooms for that schools, 15 students for that classes, 2 activity for that students
        """

    instructions_v2 = """
           create 10 invoices, create 3 invoice items for each invoice; 
           product table is reference data you must use a cursor to extract 20 rows and use them;
           customer table is reference data you must use a cursor to extract 10 rows;
           """
    #run_sd("Create 3 authors 4 books for each author and 2 comment for each book", schema_file='./data/schema_x1.sql')
    #run_sd("Create a school, 3 classroom for that school, 5 students for each class, 2 activity for each student", schema_file='./data/school_schema_v1.sql')
    #run_sd("Create a school, 3 classroom for that school, 5 students for each class, 2 activity for each student", schema_file='./data/school_schema_v1.sql')
    run_sd(instructions_v2,schema_file='./data/invoice_schema_v1.sql')