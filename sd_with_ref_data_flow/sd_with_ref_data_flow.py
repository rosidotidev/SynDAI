from crewai import Agent, Crew, Process, Task, Flow
from crewai.flow.flow import listen, start, router
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import FileReadTool, FileWriterTool
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


from tools.custom_template_tool import CustomTemplateTool


# Pydantic models for structured outputs
class ValidationReport(BaseModel):
    is_valid: bool
    issues_found: List[str]
    suggestions: List[str]
    severity: str  # "critical", "warning", "pass"


class CodeFixResult(BaseModel):
    fixed_code: str
    changes_applied: List[str]


class StructuredExecutionPlan(BaseModel):
    """Output from data_schema_scientist"""
    pass  # Define based on your needs


class SDFakerScientistResult(BaseModel):
    """Output from data_script_planner"""
    pass  # Define based on your needs


class SDFakerResult(BaseModel):
    """Output from python_data_layer_developer"""
    pass  # Define based on your needs

fileReadTool = FileReadTool()
customTemplateTool = CustomTemplateTool()
fileWriterTool=FileWriterTool()

class CodeValidationState(BaseModel):
    code: str = ""
    syntax_status: str = ""

class SynDataFlow(Flow[CodeValidationState]):
    agents_config = 'agents.yaml'
    tasks_config = 'tasks.yaml'

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def data_schema_scientist(self) -> Agent:
        return Agent(
            config=self.agents_config['data_schema_scientist'],  # type: ignore[index]
            verbose=True,
            tools=[fileReadTool, fileWriterTool],
            # output_pydantic = SDBaseFullGenerationScript
        )

    @agent
    def data_script_planner(self) -> Agent:
        return Agent(
            config=self.agents_config['data_script_planner'],  # type: ignore[index]
            verbose=True,
            tools=[fileWriterTool],
            # output_pydantic = SDBaseFullGenerationScript
        )

    @agent
    def template_injector(self) -> Agent:
        return Agent(
            config=self.agents_config['template_injector'],  # type: ignore[index]
            verbose=True,
            tools=[fileWriterTool],

        )

    @agent
    def python_data_layer_developer(self) -> Agent:
        return Agent(
            config=self.agents_config['python_data_layer_developer'],  # type: ignore[index]
            verbose=True,
        )

    @agent
    def python_data_layer_architect(self) -> Agent:
        return Agent(
            config=self.agents_config['python_data_layer_architect'],  # type: ignore[index]
            verbose=True,
            tools=[fileWriterTool],

        )

    @agent
    def python_data_layer_architect(self) -> Agent:
        return Agent(
            config=self.agents_config['python_data_layer_architect'],  # type: ignore[index]
            verbose=True,
            tools=[fileWriterTool],

        )

    @agent
    def python_code_fixer(self) -> Agent:
        return Agent(
            config=self.agents_config['python_code_fixer'],  # type: ignore[index]
            verbose=True,
            tools=[fileWriterTool],

        )

    @task
    def task_analyze_schema(self) -> Task:
        return Task(
            config=self.tasks_config['task_analyze_schema'],  # type: ignore[index]
            output_pydantic=StructuredExecutionPlan
        )

    @task
    def task_generate_sql_template(self) -> Task:
        return Task(
            config=self.tasks_config['task_generate_sql_template'],  # type: ignore[index]
            output_pydantic=SDFakerScientistResult
        )

    @task
    def task_inject_templates(self) -> Task:
        return Task(
            config=self.tasks_config['task_inject_templates'],  # type: ignore[index]
            # output_pydantic=SDFakerResult
        )

    @task
    def task_generate_final_python_script(self) -> Task:
        return Task(
            config=self.tasks_config['task_generate_final_python_script'],  # type: ignore[index]
            output_pydantic=SDFakerResult
        )

    @task
    def task_review_python_code(self) -> Task:
        return Task(
            config=self.tasks_config['task_review_python_code'],  # type: ignore[index]
            output_pydantic=ValidationReport
        )

    @task
    def task_fix_python_code(self) -> Task:
        return Task(
            config=self.tasks_config['task_fix_python_code'],  # type: ignore[index]
            output_pydantic=CodeFixResult
        )

    @crew
    def crew(self) -> Crew:
        self.agents=[self.data_schema_scientist(),self.data_script_planner(),self.template_injector()]
        self.tasks =[self.task_analyze_schema(),self.task_generate_sql_template(),self.task_inject_templates()]
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True

        )

    @start("try_again")
    def start_generate(self):
        """Starts the workflow, sends the code to the analyzer."""
        print(f"Starting code analysis...\n ")
        result = self.crew().kickoff()
        syntax_status = result.raw

if __name__ == "__main__":
    flow=SynDataFlow()
    flow.kickoff(inputs={"code": "ciao"})