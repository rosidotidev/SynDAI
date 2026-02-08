from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from faker import Faker
import random

# Initialize Faker globally (or locally in the _run method if preferred)
fake = Faker()


# --- 1. Input Schema (Pydantic) ---
class FakerInput(BaseModel):
    """Input schema for the FakerTool."""
    field_name: str = Field(
        description="The name of the field to call (e.g., 'name', 'address', 'email', 'date_of_birth')."
    )


# --- 2. Custom Tool Class ---
class FakerTool(BaseTool):
    """
    A tool to generate random synthetic data using the Faker library.
    It accepts the name of the Faker method to call.
    """
    name: str = "Faker Data Generator"
    description: str = (
        "Useful for generating random and realistic data like names, addresses, emails, and dates. "
        "Pass the desired Faker method name (e.g., 'name', 'city','address') and it returns a fake value for that request"
    )
    # Link the Pydantic schema
    args_schema: Type[BaseModel] = FakerInput

    def _run(self, field_name: str) -> str:
        """
        Logic that uses the getattr method to dynamically call the Faker provider.
        """

        def faker_wrapper(placeholder: str) -> str:
            """
            Genera un valore realistico in base al placeholder usando Faker.
            """
            mapping = {
                "school_name": fake.company,
                "school_address": lambda: fake.address().replace("\n", " "),
                "room_number": lambda: f"R{fake.random_int(min=100, max=999)}",
                "capacity": lambda: str(fake.random_int(min=20, max=40)),
                "first_name": fake.first_name,
                "last_name": fake.last_name,
                "enrollment_date": lambda: fake.date_this_decade().strftime("%Y-%m-%d"),
                "activity_name": fake.word,
                "activity_date": lambda: fake.date_this_year().strftime("%Y-%m-%d")
            }

            key = placeholder.strip("{} ").replace(" ", "_")  # Normalizza il placeholder
            if key in mapping:
                generator = mapping[key]
                return generator() if callable(generator) else generator()
            else:
                return f"<UNKNOWN:{placeholder}>"
        return faker_wrapper(field_name)


# --- 3. Usage Example ---
if __name__ == '__main__':
    # Create the Tool instance
    faker_tool_instance = FakerTool()

    # Example of a direct call (simulating the Agent calling the Tool)

    # Agent requests a name
    name_result = faker_tool_instance._run(field_name="first_name")
    print(f"Generated Name: {name_result}")

    # Agent requests an address
    address_result = faker_tool_instance._run(field_name="school_address")
    print(f"Generated Address: {address_result}")

    # Agent requests an invalid provider
    error_result = faker_tool_instance._run(field_name="not_a_provider")
    print(f"Error result: {error_result}")