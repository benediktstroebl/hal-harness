from tau_bench.envs import get_env
from tau_bench.agents.base import Agent
from tau_bench.types import EnvRunResult, RunConfig, Action

from tau_bench.agents.tool_calling_agent import ToolCallingAgent

from openai import OpenAI
def run(input: dict[str, dict], **kwargs) -> dict[str, str]:

    assert 'model_name' in kwargs, 'model_name is required'
    client = OpenAI()
    task_id = list(input.keys())[0]
    
    ### ENV SETUP (usually this should be untouched) ###
    isolated_env = get_env(
        input[task_id]['env'],
        input[task_id]['user_strategy'],
        input[task_id]['user_model'],
        input[task_id]['task_split'],
        input[task_id]['user_provider'],
        input[task_id]['task_index'],
            )
    # get instruction from environment
    instruction = isolated_env.reset(input[task_id]['task_index']).observation
    
    
    ### YOUR AGENT CODE HERE ###
    agent = ToolCallingAgent(
        tools_info=isolated_env.tools_info,
        wiki=isolated_env.wiki,
        model=kwargs['model_name'],
        provider="openai",
        temperature=0.5,
    )
    
    output = agent.solve(isolated_env, task_index=input[task_id]['task_index'])
        
    ### WHEN DONE WE RETURN THE ENV STATE ###
    return {task_id: isolated_env.calculate_reward().model_dump()}

