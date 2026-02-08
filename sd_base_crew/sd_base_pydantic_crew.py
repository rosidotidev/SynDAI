from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import FileReadTool
from sd_base_crew.model.sd_base_result import SDBaseFullGenerationScript
from tools.faker_tool import FakerTool


fileReadTool = FileReadTool()
fakerTool = FakerTool()

@CrewBase
class SDBasePydanticCrew:

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def schema_analyzer(self) -> Agent:

        return Agent(
            config=self.agents_config['schema_analyzer'],  # type: ignore[index]
            verbose=True,
            tools=[fileReadTool,fakerTool],
            #output_pydantic = SDBaseFullGenerationScript
        )

    @task
    def task_analyze_model(self) -> Task:
        return Task(
            config=self.tasks_config['task_analyze_model'],  # type: ignore[index]
            output_pydantic=SDBaseFullGenerationScript
        )

    @crew
    def crew(self) -> Crew:

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True

        )

