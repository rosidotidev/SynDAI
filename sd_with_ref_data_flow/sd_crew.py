from crewai import Agent, Crew, Process, Task, Flow
from crewai.project import CrewBase, agent, crew, task

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

@CrewBase
class SynDataCrew:
    """
    Crew responsabile della generazione dei dati sintetici.
    Questa classe NON è una Flow.
    """

    agents_config = "agents.yaml"
    tasks_config = "tasks.yaml"

    # =========================
    # AGENTS
    # =========================

    @agent
    def data_schema_scientist(self) -> Agent:
        return Agent(
            config=self.agents_config["data_schema_scientist"],
            verbose=True,
            tools=[fileReadTool, fileWriterTool],
        )

    @agent
    def data_script_planner(self) -> Agent:
        return Agent(
            config=self.agents_config["data_script_planner"],
            verbose=True,
            tools=[fileWriterTool],
        )

    @agent
    def template_injector(self) -> Agent:
        return Agent(
            config=self.agents_config["template_injector"],
            verbose=True,
            tools=[fileWriterTool],
        )

    @agent
    def python_data_layer_developer(self) -> Agent:
        return Agent(
            config=self.agents_config["python_data_layer_developer"],
            verbose=True,
        )

    # =========================
    # TASKS
    # =========================

    @task
    def task_analyze_schema(self) -> Task:
        return Task(
            config=self.tasks_config["task_analyze_schema"],
            output_pydantic=StructuredExecutionPlan,
        )

    @task
    def task_generate_sql_template(self) -> Task:
        return Task(
            config=self.tasks_config["task_generate_sql_template"],
            output_pydantic=SDFakerScientistResult,
        )

    @task
    def task_inject_templates(self) -> Task:
        return Task(
            config=self.tasks_config["task_inject_templates"],
        )

    @task
    def task_generate_final_python_script(self) -> Task:
        return Task(
            config=self.tasks_config["task_generate_final_python_script"],
            output_pydantic=SDFakerResult,
        )

    # =========================
    # CREW
    # =========================

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.data_schema_scientist(),
                self.data_script_planner(),
                self.template_injector(),
                self.python_data_layer_developer(),
            ],
            tasks=[
                self.task_analyze_schema(),
                self.task_generate_sql_template(),
                self.task_inject_templates(),
                self.task_generate_final_python_script(),
            ],
            process=Process.sequential,
            verbose=True,
        )
