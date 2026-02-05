import json
from tools.github_tool import GitHubTool
from tools.weather_tool import WeatherTool
from tools.news_tool import NewsTool
from tools.media_tool import MediaTool

class ExecutorAgent:
    def __init__(self):
        # Initialize only the verified working tools
        self.tools = {
            "github_tool": GitHubTool(),
            "weather_tool": WeatherTool(),
            "news_tool": NewsTool(),
            "media_tool": MediaTool()
        }

    def execute_plan(self, plan_json):
        """
        Iterates through the steps in the plan and collects tool data.
        """
        results_report = []
        
        # Handle cases where plan might be a string or a dict
        plan = json.loads(plan_json) if isinstance(plan_json, str) else plan_json
        steps = plan.get("plan", [])

        if not steps:
            return [{"error": "No steps found in the generated plan."}]

        for step in steps:
            tool_name = step.get("tool")
            args = step.get("args", {})
            
            if tool_name in self.tools:
                tool_instance = self.tools[tool_name]
                result = self._route_to_tool(tool_instance, tool_name, args)
                
                results_report.append({
                    "step": step.get("step"),
                    "tool": tool_name,
                    "status": "SUCCESS" if "error" not in result else "FAILED",
                    "data": result
                })
            else:
                results_report.append({
                    "step": step.get("step"),
                    "tool": tool_name,
                    "status": "FAILED",
                    "error": f"Tool '{tool_name}' is not integrated."
                })

        return results_report

    def _route_to_tool(self, instance, tool_name, args):
        """
        Maps specific tool names to their respective class methods.
        """
        try:
            # Flexible argument extraction
            query = args.get("query") or args.get("movie_name") or args.get("repo_name") or args.get("city") or args.get("topic")

            if tool_name == "github_tool":
                return instance.get_repo_details(query)
            
            elif tool_name == "weather_tool":
                return instance.get_current_weather(query)
            
            elif tool_name == "news_tool":
                return instance.get_latest_news(query)
            
            elif tool_name == "media_tool":
                # Check if it's music or a movie
                arg_str = str(args).lower()
                if "song" in arg_str or "music" in arg_str or "artist" in arg_str:
                    return instance.search_music(query)
                return instance.search_movies(query)

            return {"error": f"Logic for {tool_name} not implemented in router."}
        
        except Exception as e:
            return {"error": f"Tool execution failed: {str(e)}"}