"""
Agent 2: Planner Agent
Creates research sub-tasks based on data analysis and business goals
"""
import google.generativeai as genai
from typing import Dict, List, Any, Optional
import json
import re

from config import GEMINI_API_KEY, GEMINI_MODEL


class PlannerAgent:
    """
    Takes analysis results and CEO goals to create actionable research tasks.
    Generates specific queries for web research agent.
    """
    
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL)
        self.research_tasks = []
        
    def create_research_plan(
        self, 
        analysis_summary: str,
        business_type: str,
        ceo_goal: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Generate research sub-tasks based on analysis"""
        
        prompt = f"""You are a business research planner for a {business_type} in India.

Based on the following business analysis, create 5-7 specific research tasks that will help improve the business.

=== BUSINESS ANALYSIS ===
{analysis_summary}

=== CEO'S GOAL ===
{ceo_goal if ceo_goal else "Maximize profit and growth while reducing losses"}

Create research tasks in the following JSON format. Each task should be specific and actionable:

```json
[
  {{
    "task_id": 1,
    "task_type": "competitor_pricing|market_trend|seasonal_demand|best_practices|supplier_research",
    "priority": "high|medium|low",
    "search_query": "specific search query to use",
    "target_product": "product name or category if applicable",
    "expected_insight": "what we expect to learn from this research"
  }}
]
```

Focus on:
1. Competitor pricing for weak/declining products
2. Market trends for rising products (to capitalize on demand)
3. Seasonal demand patterns for low-margin products
4. Best practices for inventory management
5. Alternative suppliers for high-cost products

Return ONLY valid JSON array, no other text.
"""
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Extract JSON from response
            json_match = re.search(r'\[[\s\S]*\]', response_text)
            if json_match:
                tasks = json.loads(json_match.group())
                self.research_tasks = tasks
                return tasks
            else:
                # Fallback to default tasks
                return self._get_default_tasks(business_type)
                
        except Exception as e:
            print(f"Error generating research plan: {e}")
            return self._get_default_tasks(business_type)
    
    def _get_default_tasks(self, business_type: str) -> List[Dict]:
        """Fallback research tasks if LLM fails"""
        return [
            {
                "task_id": 1,
                "task_type": "competitor_pricing",
                "priority": "high",
                "search_query": f"{business_type} product pricing trends India 2024",
                "target_product": "general",
                "expected_insight": "Understanding current market pricing"
            },
            {
                "task_id": 2,
                "task_type": "market_trend",
                "priority": "high", 
                "search_query": f"{business_type} market trends consumer behavior India",
                "target_product": "general",
                "expected_insight": "Current market trends and consumer preferences"
            },
            {
                "task_id": 3,
                "task_type": "best_practices",
                "priority": "medium",
                "search_query": f"{business_type} inventory management best practices small business",
                "target_product": "general",
                "expected_insight": "Inventory optimization strategies"
            },
            {
                "task_id": 4,
                "task_type": "seasonal_demand",
                "priority": "medium",
                "search_query": f"{business_type} seasonal demand patterns India",
                "target_product": "general",
                "expected_insight": "Seasonal sales patterns to prepare for"
            },
            {
                "task_id": 5,
                "task_type": "supplier_research",
                "priority": "low",
                "search_query": f"wholesale suppliers {business_type} India best prices",
                "target_product": "general",
                "expected_insight": "Alternative supplier options for cost reduction"
            }
        ]
    
    def prioritize_tasks(self, tasks: List[Dict]) -> List[Dict]:
        """Sort tasks by priority"""
        priority_order = {"high": 0, "medium": 1, "low": 2}
        return sorted(tasks, key=lambda x: priority_order.get(x.get('priority', 'low'), 2))
    
    def run(
        self,
        analysis_summary: str,
        business_type: str = "Grocery Store",
        ceo_goal: Optional[str] = None
    ) -> Dict[str, Any]:
        """Run the planner agent"""
        
        tasks = self.create_research_plan(analysis_summary, business_type, ceo_goal)
        prioritized_tasks = self.prioritize_tasks(tasks)
        
        return {
            'total_tasks': len(prioritized_tasks),
            'high_priority': sum(1 for t in prioritized_tasks if t.get('priority') == 'high'),
            'medium_priority': sum(1 for t in prioritized_tasks if t.get('priority') == 'medium'),
            'low_priority': sum(1 for t in prioritized_tasks if t.get('priority') == 'low'),
            'tasks': prioritized_tasks
        }
    
    def get_search_queries(self) -> List[str]:
        """Extract just the search queries from tasks"""
        return [task.get('search_query', '') for task in self.research_tasks if task.get('search_query')]
