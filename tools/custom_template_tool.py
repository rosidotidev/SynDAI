from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from faker import Faker
from typing import Type, Callable
from jinja2 import Environment, BaseLoader
from itertools import count

MAX=3
counter = count(start=1)
def next_line_number():
    n = next(counter)
    return ((n - 1) % MAX) + 1

fake = Faker()

class TemplateModel(BaseModel):
    template: str = Field(..., description="A Jinja2 template string with placeholders")

class CustomTemplateTool(BaseTool):
    """
    A powerful tool that takes a template and automatically fills it
    using a word generator. Useful for generating SQL insert scripts, JSON payloads,
    test fixtures, and synthetic datasets.
    """

    name: str = "custom_template_tool"
    description: str = (
        "Compiles a template and automatically fills all placeholders "
        "using an internal generator. It is able to intercept placeholders marked with {{}} and replace with value."
    )

    args_schema: Type[BaseModel] = TemplateModel

    # Optional override mapping (custom generators)
    custom_mapping: dict[str, Callable] = {
        "school_name": lambda: f"{fake.company()} School",
        "school_address": lambda: fake.address().replace("\n", " "),
        "room_number": lambda: f"R{fake.random_int(min=100, max=999)}",
        "quantity": lambda: f"{fake.random_int(min=1, max=12)}",
        "capacity": lambda: str(fake.random_int(min=20, max=40)),
        "unit_price": lambda: str(fake.random_int(min=20, max=120)),
        "activity_date": lambda: fake.date_this_year().strftime("%Y-%m-%d"),
        "activity_name": lambda:  f"Do something {fake.random_int(min=10, max=80)} times",
        "line_number": lambda: next_line_number(),
    }

    def resolve_placeholder(self, key: str) -> str:
        """
        Resolve a placeholder using custom_mapping and Faker, supporting fuzzy matching.
        """
        normalized = key.strip().replace(" ", "_")

        # 1. Fuzzy match custom mapping
        for map_key, gen in self.custom_mapping.items():
            if map_key in normalized:
                return gen() if callable(gen) else gen

        # 2. Fuzzy match Faker methods
        for attr_name in dir(fake):
            if attr_name in normalized:
                method = getattr(fake, attr_name)
                if callable(method):
                    return str(method())

        # 3. If unresolved
        return f"<UNRESOLVED:{normalized}>"

    def fill(self, template: str) -> str:
        return self._run(template)

    def _run(self, template: str) -> str:
        try:
            """
            Render Jinja2 template intercepting placeholders dynamically.
            """

            # Environment that resolves every variable using our resolver
            env = Environment(loader=BaseLoader())

            # Create a custom function accessible inside Jinja2
            env.globals['fake'] = self.resolve_placeholder

            # Replace {{ field }} → {{ fake('field') }}
            # This allows resolving any placeholder via our tool
            preprocessed = template

            # Finds {{ something }} and rewrites it to {{ fake('something') }}
            # Keeps Jinja2 fully compatible
            import re
            def repl(match):
                expr = match.group(1).strip()
                return "{{ fake('" + expr + "') }}"

            preprocessed = re.sub(r"{{\s*(.*?)\s*}}", repl, preprocessed)

            # Render final template
            compiled = env.from_string(preprocessed)
            return compiled.render()
        except Exception as e:
            print(f"Failed to render {template}: {e}")
            raise e
if __name__ == "__main__":
    tool = CustomTemplateTool()

    template_sql = """
    INSERT INTO student (first_name, last_name, room_number, school_name)
    VALUES ('{{ first_name_1_ee }}',
            '{{ last_name_34 }}',
            '{{ ee_room_number }}',
            '{{ school_name_33 }}');
            
DECLARE @student_id INT;
SET @student_id = NEXT VALUE FOR StudentID_Sequence;
-- classroom_id obtained by matching classroom parameters
INSERT INTO Student (student_id, first_name, last_name, enrollment_date, classroom_id)
VALUES (@student_id, '{{ first_name_1_1_1 }}', '{{ last_name_1_1_1 }}', '{{ enrollment_date_1_1_1 }}', @classroom_id);
GO
    """

    print("=== TEMPLATE ORIGINALE ===")
    print(template_sql)

    # Simula esattamente la chiamata CrewAI → passa un dict
    input_payload = template_sql

    print("\n=== OUTPUT GENERATO ===")
    output = tool._run(input_payload)
    print(output)
    output = tool._run(output)
    print(output)