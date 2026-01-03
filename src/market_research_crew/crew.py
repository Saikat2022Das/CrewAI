from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

# We need to import the tools that we are going to use
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, SeleniumScrapingTool
# ScrapWebsiteTool is used to scrape websites for data on Static websites
# SerperDevTool is used to search the web for latest information
# MDXSearchTool is used to search through documents
# SeleniumScrapingTool is used to scrape dynamic websites  => For Use this tool need install "uv add selenium webdriver-manager"

from dotenv import load_dotenv
load_dotenv()

# Create the tools for the agents
web_search_tool = SerperDevTool()
web_scraping_tool = ScrapeWebsiteTool()
selenium_scraping_tool = SeleniumScrapingTool()

# We have to provide the tools to the agents as a list
toolkit = [
    web_search_tool,
    web_scraping_tool,
    selenium_scraping_tool
]

# Define the crew class
@CrewBase
class MarketResearchCrew():
    """MarketResearchCrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Provide the path for configuration files
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    ################### Agents ###################

    @agent     # Define an agent by using the @agent decorator
    def market_research_specialist(self) -> Agent:
        return Agent(
            config = self.agents_config['market_research_specialist'],
            tools = toolkit,  # Provide the tools to the agent       
        )

    @agent
    def competitive_intelligence_analyst(self) -> Agent:
        return Agent(
            config = self.agents_config['competitive_intelligence_analyst'],
            tools = toolkit
        )

    @agent
    def customer_insights_researcher(self) -> Agent:
        return Agent(
            config = self.agents_config['customer_insights_researcher'],
            tools = toolkit
        )

    @agent
    def product_strategy_advisor(self) -> Agent:
        return Agent(
            config = self.agents_config['product_strategy_advisor'],
            tools = toolkit
        )

    @agent
    def business_analyst(self) -> Agent:
        return Agent(
            config = self.agents_config['business_analyst'],
            tools = toolkit
        )
    
    ################### Tasks ###################
    # We have to mentain the order of tasks as they are dependent on each other

    @task
    def market_research_task(self) -> Task:
        return Task(
            config = self.tasks_config['market_research_task']  
        )
    
    @task
    def competitive_intelligence_task(self) -> Task:
        return Task(
            config = self.tasks_config['competitive_intelligence_task'],
            context = [self.market_research_task()]  # Dependent on market_research_task, once it is done, its output will be used as context
        )

    @task
    def customer_insights_task(self) -> Task:
        return Task(
            config = self.tasks_config['customer_insights_task'],
            context = [self.market_research_task(),
                       self.competitive_intelligence_task()] 
        )

    @task
    def product_strategy_task(self) -> Task:
        return Task(
            config = self.tasks_config['product_strategy_task'],
            context = [self.market_research_task(),
                       self.competitive_intelligence_task(),
                       self.customer_insights_task()]
        )

    @task
    def business_analyst_task(self) -> Task:
        return Task(
            config = self.tasks_config['business_analyst_task'],
            context = [self.market_research_task(),
                       self.competitive_intelligence_task(),
                       self.customer_insights_task(),
                       self.product_strategy_task()]
        )

    ################### Crew ###################

    # @crew
    # def crew(self) -> Crew:
    #     """Creates the MarketResearchCrew crew"""
    #     return Crew(
    #         agents=self.agents,  # Automatically created by the @agent decorator
    #         tasks=self.tasks,  # Automatically created by the @task decorator
    #         process=Process.sequential,
    #         verbose=True,
    #     )

    # from crewai import Crew, Process

    @crew
    def crew(self) -> Crew:
        """Creates the MarketResearchCrew crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            llm={
                "provider": "groq",
                "model": "llama-3.1-8b-instant",
                "temperature": 0.3,
            },
        )

