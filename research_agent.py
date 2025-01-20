from typing import Any, Callable, Dict, List, Optional, Union
from smolagents import Tool, CodeAgent
from smolagents.agents import ActionStep
from smolagents.models import ChatMessage

from entities import Memory


class ResearchAgent(CodeAgent):
    """
    This agent uses JSON-like tool calls, using method `model.get_tool_call` to leverage the LLM engine's tool calling capabilities.
    """

    def __init__(
        self,
        tools: List[Tool],
        model: Callable[[List[Dict[str, str]]], ChatMessage],
        system_prompt: Optional[str] = None,
        grammar: Optional[Dict[str, str]] = None,
        additional_authorized_imports: Optional[List[str]] = None,
        planning_interval: Optional[int] = None,
        use_e2b_executor: bool = False,
        add_base_tools: bool = True,
        short_term_memory: List[Memory] = [],
        long_term_memory: List[Memory] = [],
        **kwargs,
    ):
        super().__init__(
            tools=tools,
            model=model,
            system_prompt=system_prompt,
            grammar=grammar,
            additional_authorized_imports=additional_authorized_imports,
            planning_interval=planning_interval,
            use_e2b_executor=use_e2b_executor,
            add_base_tools=add_base_tools,
            **kwargs,
        )
        self.short_term_memory = short_term_memory
        self.long_term_memory = long_term_memory

    def step(self, log_entry: ActionStep) -> Union[None, Any]:
        return super().step(log_entry)

    def run(
        self,
        task: str,
        stream: bool = False,
        reset: bool = True,
        single_step: bool = False,
        additional_args: Optional[Dict] = None,
    ):
        if self.short_term_memory:
            task = (
                task
                + "\nShort term memory:\n"
                + self._format_memories(self.short_term_memory)
            )
        if self.long_term_memory:
            task = (
                task
                + "\nLong term memory:\n"
                + self._format_memories(self.long_term_memory)
            )
        return super().run(
            task=task,
            stream=stream,
            reset=reset,
            single_step=single_step,
            additional_args=additional_args,
        )

    def _format_memories(self, memories: List[Memory]) -> str:
        return "\n".join([str(memory) for memory in memories])
