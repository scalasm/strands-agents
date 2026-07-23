"""A graph"""

import logging

from strands import Agent
from strands.multiagent import GraphBuilder
from strands.multiagent.graph import Graph
from strands_tools import http_request

from my_strands_agents.utils.agent_factory import create_openai_model

# Enable debug logs and print them to stderr
logging.getLogger("strands.multiagent").setLevel(logging.DEBUG)
logging.basicConfig(format="%(levelname)s | %(name)s | %(message)s", handlers=[logging.StreamHandler()])


# Create specialized agents
RESEARCHER_PROMPT = (
    "You are a Researcher Agent that gathers information from the web. "
    "1. Determine if the input is a research query or factual claim "
    "2. Use your research tools (http_request, retrieve) to find relevant information "
    "3. Include source URLs and keep findings under 500 words"
)
researcher = Agent(name="researcher", system_prompt=RESEARCHER_PROMPT, tools=[http_request], model=create_openai_model())

ANALYST_PROMPT = (
    "You are an Analyst Agent that verifies information. "
    "1. For factual claims: Rate accuracy from 1-5 and correct if needed "
    "2. For research queries: Identify 3-5 key insights "
    "3. Evaluate source reliability and keep analysis under 400 words"
)
analyst = Agent(name="analyst", system_prompt=ANALYST_PROMPT, model=create_openai_model())

FACT_CHECKER_PROMPT = (
    "You are a Fact Checker Agent that verifies the accuracy of research findings. "
    "1. Cross-reference the research data with reliable sources "
    "2. Identify any discrepancies or unsupported claims "
    "3. Provide a clear verdict on the validity of the information"
)
fact_checker = Agent(name="fact_checker", system_prompt=FACT_CHECKER_PROMPT, model=create_openai_model())

REPORT_WRITER_PROMPT = (
    "You are a Writer Agent that creates clear reports. "
    "1. For fact-checks: State whether claims are true or false "
    "2. For research: Present key insights in a logical structure "
    "3. Keep reports under 1000 words with brief source mentions"
)
report_writer = Agent(name="report_writer", system_prompt=REPORT_WRITER_PROMPT, model=create_openai_model())


def _build_graph() -> Graph:
    # Build the graph
    builder = GraphBuilder()

    # Add nodes
    builder.add_node(researcher, "research")
    builder.add_node(analyst, "analysis")
    builder.add_node(fact_checker, "fact_check")
    builder.add_node(report_writer, "report")

    # Add edges (dependencies)
    builder.add_edge("research", "analysis")
    builder.add_edge("research", "fact_check")
    builder.add_edge("analysis", "report")
    builder.add_edge("fact_check", "report")

    # Set entry points (optional - will be auto-detected if not specified)
    builder.set_entry_point("research")

    # Optional: Configure execution limits for safety
    builder.set_execution_timeout(600)  # 10 minute timeout

    # Build the graph
    return builder.build()


def app() -> None:
    """Run a multi-agent research graph demo."""
    graph = _build_graph()

    # Execute the graph on a task
    result = graph("Research the impact of AI on healthcare and create a comprehensive report")
    # Or use invoke_async for async execution: result = await graph.invoke_async(...)

    # Access the results
    logging.info(f"\nStatus: {result.status}")
    logging.info(f"Execution order: {[node.node_id for node in result.execution_order]}")
