from tools.custom_template_tool import CustomTemplateTool
# SQL templates for each block
SQL_TEMPLATES = {
    "HEADER": """
-- Declaring all necessary variables
DECLARE @v_city_id INT;
DECLARE @v_people_id INT;
""",

    "CITY": """
SET @v_city_id = NEXT VALUE FOR CityID_Sequence;
INSERT INTO CITY (id,city_name,city_code,residents) VALUES (@v_city_id,'{{ city_name }}',{{ city_code }},{{ residents }});
""",
    "PEOPLE": """
SET @v_people_id = NEXT VALUE FOR PeopleID_Sequence;
INSERT INTO PEOPLE (id,id_city,first_name,last_name,age)
VALUES (@v_people_id,@v_city_id,'{{ first_name }}','{{ last_name }}',{{ age }});
"""
}
NUM_CITIES = 3
PEOPLE_PER_CITY = 10
customTemplateTool = CustomTemplateTool()
def generate_sql_script():
    full_script = []
    full_script.append(SQL_TEMPLATES["HEADER"])
    # Loop 1: CITY Generation (Outer Loop)
    for i in range(1, NUM_CITIES + 1):
        city_statement = SQL_TEMPLATES["CITY"]
        filled_city_statement = customTemplateTool.fill(city_statement)
        full_script.append(filled_city_statement)
        full_script.append("GO\n")
        # Loop 2: PEOPLE Generation (Nested Loop)
        for j in range(1, PEOPLE_PER_CITY + 1):
            # 2. Fill the PEOPLE template
            people_statement = SQL_TEMPLATES["PEOPLE"]
            # Invoking the fill function
            filled_people_statement = customTemplateTool.fill(people_statement)
            full_script.append(filled_people_statement)
            full_script.append("GO\n")

    return "\n".join(full_script)
if __name__ == "__main__":
    generated_sql = generate_sql_script()
    print(generated_sql)
