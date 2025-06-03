import os
from crewai import Agent, Crew, Process, Task
from crewai_tools import MCPServerAdapter
from mcp import StreamableHTTPServerParameters


def build_crew(query: str) -> Crew:
    """Builds a CrewAI crew with MCP tools for the request."""
    server_url = os.environ.get("MCP_SERVER_URL", "http://localhost:8000/mcp")
    server_params = StreamableHTTPServerParameters(url=server_url)
    with MCPServerAdapter(server_params) as mcp_tools:
        agent = Agent(
            role="SAP data quality and migration expert",
            goal="Write SQL queries and define data migration rules",
            backstory=(
                "You are an experienced consultant specializing in SAP data "
                "quality and migration. You help users craft SQL queries and "
                "migration rules to move data between systems."),
            llm="gpt-4.1",
            tools=mcp_tools,
            verbose=True,
        )

        task = Task(
            description="{query}",
            agent=agent,
        )

        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
        )
        crew.inputs = {"query": query}
        return crew
