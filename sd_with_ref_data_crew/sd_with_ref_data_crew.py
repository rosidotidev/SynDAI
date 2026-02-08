from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import FileReadTool, FileWriterTool
from sd_with_ref_data_crew.model.sd_faker_scientist_result import SDFakerScientistResult,SDFakerResult,StructuredExecutionPlan
from tools.custom_template_tool import CustomTemplateTool

fileReadTool = FileReadTool()
customTemplateTool = CustomTemplateTool()
fileWriterTool=FileWriterTool()

@CrewBase
class SDWithRefDataCrew:

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def data_schema_scientist(self) -> Agent:

        return Agent(
            config=self.agents_config['data_schema_scientist'],  # type: ignore[index]
            verbose=True,
            tools=[fileReadTool,fileWriterTool],
            #output_pydantic = SDBaseFullGenerationScript
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
            #output_pydantic=SDFakerResult
        )

    @task
    def task_generate_final_python_script(self) -> Task:
        return Task(
            config=self.tasks_config['task_generate_final_python_script'],  # type: ignore[index]
            output_pydantic=SDFakerResult
        )

    @task
    def task_review_and_save_final_python_script(self) -> Task:
        return Task(
            config=self.tasks_config['task_review_and_save_final_python_script'],  # type: ignore[index]
            output_pydantic=SDFakerResult
        )
    @crew
    def crew(self) -> Crew:
        #self.agents=self.agents[:3]
        #self.tasks = self.tasks[:3]
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True

        )

