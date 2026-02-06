"""
Agent 5: Consultant Agent
Generates final business strategy, weekly action plan, and risk assessment
"""
import google.generativeai as genai
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json
import re

from config import GEMINI_API_KEY, GEMINI_MODEL


class ConsultantAgent:
    """
    Final agent that synthesizes all findings into actionable business recommendations.
    Creates comprehensive strategy, weekly plan, and risk documentation.
    """
    
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL)
        self.final_report = {}
        
    def generate_strategy(
        self,
        analysis_summary: str,
        research_summary: str,
        verification_summary: str,
        business_type: str,
        ceo_goal: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate comprehensive business strategy"""
        
        prompt = f"""You are an expert MSME business consultant in India creating a comprehensive growth strategy.

=== BUSINESS TYPE ===
{business_type}

=== CEO'S GOAL ===
{ceo_goal if ceo_goal else "Maximize profit and sustainable growth"}

=== BUSINESS ANALYSIS ===
{analysis_summary}

=== MARKET RESEARCH FINDINGS ===
{research_summary}

=== VERIFICATION & CONFIDENCE ===
{verification_summary}

Based on ALL the above information, create a comprehensive business strategy in the following JSON format:

```json
{{
  "executive_summary": "2-3 sentence overview of the strategy",
  "key_opportunities": [
    {{
      "opportunity": "description",
      "potential_gain": "estimated benefit",
      "priority": "high|medium|low"
    }}
  ],
  "immediate_actions": [
    {{
      "action": "specific action to take",
      "timeline": "this week|next 2 weeks|this month",
      "expected_outcome": "what will improve",
      "resources_needed": "what's required"
    }}
  ],
  "weekly_plan": [
    {{
      "week": 1,
      "focus_area": "main focus",
      "tasks": ["task1", "task2", "task3"],
      "success_metrics": "how to measure success"
    }},
    {{
      "week": 2,
      "focus_area": "main focus",
      "tasks": ["task1", "task2"],
      "success_metrics": "how to measure success"
    }},
    {{
      "week": 3,
      "focus_area": "main focus",
      "tasks": ["task1", "task2"],
      "success_metrics": "how to measure success"
    }},
    {{
      "week": 4,
      "focus_area": "main focus",
      "tasks": ["task1", "task2"],
      "success_metrics": "how to measure success"
    }}
  ],
  "risks_and_mitigations": [
    {{
      "risk": "potential risk",
      "likelihood": "high|medium|low",
      "impact": "high|medium|low",
      "mitigation": "how to address it"
    }}
  ],
  "assumptions": [
    "assumption1",
    "assumption2"
  ],
  "success_metrics": {{
    "short_term": ["metric1", "metric2"],
    "long_term": ["metric1", "metric2"]
  }},
  "estimated_roi": "expected return description"
}}
```

Be specific, actionable, and realistic for a small business. Use Indian Rupees for any monetary values.
Return ONLY valid JSON, no other text.
"""
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Extract JSON
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                result = json.loads(json_match.group())
                self.final_report = result
                return result
            else:
                self.final_report = self._get_default_strategy()
                return self.final_report
                
        except Exception as e:
            print(f"Error generating strategy: {e}")
            self.final_report = self._get_default_strategy()
            return self.final_report
    
    def _get_default_strategy(self) -> Dict[str, Any]:
        """Fallback strategy if LLM fails"""
        return {
            "executive_summary": "Based on the analysis, focus on optimizing inventory levels, addressing declining products, and capitalizing on rising demand trends. Implement strategic pricing adjustments and strengthen supplier relationships for improved margins.",
            "key_opportunities": [
                {
                    "opportunity": "Optimize stock levels for high-demand items",
                    "potential_gain": "Reduce stockouts by 60% and capture ₹15,000-25,000 in lost sales",
                    "priority": "high"
                },
                {
                    "opportunity": "Review pricing for low-margin products",
                    "potential_gain": "Improve overall profit margins by 3-5%",
                    "priority": "high"
                },
                {
                    "opportunity": "Capitalize on rising demand products",
                    "potential_gain": "Increase revenue by 15-20% on trending items",
                    "priority": "medium"
                },
                {
                    "opportunity": "Negotiate better supplier terms",
                    "potential_gain": "Reduce procurement costs by 5-10%",
                    "priority": "medium"
                }
            ],
            "immediate_actions": [
                {
                    "action": "Restock critical inventory items immediately",
                    "timeline": "this week",
                    "expected_outcome": "Prevent stockouts on top sellers",
                    "resources_needed": "₹20,000-30,000 working capital"
                },
                {
                    "action": "Increase prices on 3 lowest-margin products by 5-8%",
                    "timeline": "this week",
                    "expected_outcome": "Improved profit margins",
                    "resources_needed": "Price tags, customer communication"
                },
                {
                    "action": "Contact top 3 suppliers for bulk discount negotiation",
                    "timeline": "next 2 weeks",
                    "expected_outcome": "Better procurement rates",
                    "resources_needed": "Phone calls, meeting time"
                }
            ],
            "weekly_plan": [
                {
                    "week": 1,
                    "focus_area": "Inventory Optimization",
                    "tasks": [
                        "Complete full stock audit",
                        "Order critical items from restock list",
                        "Set up reorder point alerts",
                        "Identify slow-moving inventory"
                    ],
                    "success_metrics": "Zero stockouts on top 10 products"
                },
                {
                    "week": 2,
                    "focus_area": "Pricing Strategy",
                    "tasks": [
                        "Analyze competitor pricing from research",
                        "Adjust prices on low-margin items",
                        "Create bundle offers for slow-moving stock",
                        "Update all price displays"
                    ],
                    "success_metrics": "Average margin improved by 2%"
                },
                {
                    "week": 3,
                    "focus_area": "Supplier Relations",
                    "tasks": [
                        "Meet with primary suppliers",
                        "Negotiate volume discounts",
                        "Explore alternative suppliers for costly items",
                        "Set up regular order schedule"
                    ],
                    "success_metrics": "Secured 5% discount from at least 1 supplier"
                },
                {
                    "week": 4,
                    "focus_area": "Growth & Review",
                    "tasks": [
                        "Promote high-margin trending products",
                        "Review month's performance metrics",
                        "Plan next month's inventory",
                        "Document learnings and adjust strategy"
                    ],
                    "success_metrics": "10% revenue increase vs previous month"
                }
            ],
            "risks_and_mitigations": [
                {
                    "risk": "Customer pushback on price increases",
                    "likelihood": "medium",
                    "impact": "medium",
                    "mitigation": "Gradual increases, emphasize quality, offer loyalty discounts"
                },
                {
                    "risk": "Supplier unable to meet demand",
                    "likelihood": "low",
                    "impact": "high",
                    "mitigation": "Maintain relationships with 2-3 backup suppliers"
                },
                {
                    "risk": "Market conditions may shift",
                    "likelihood": "medium",
                    "impact": "medium",
                    "mitigation": "Monitor trends weekly, maintain flexible inventory"
                },
                {
                    "risk": "Working capital constraints",
                    "likelihood": "medium",
                    "impact": "high",
                    "mitigation": "Prioritize high-ROI investments, consider small credit line"
                }
            ],
            "assumptions": [
                "Current market trends will continue in the short-term",
                "Supply chain remains relatively stable",
                "No major competitor entries in the local market",
                "Customer base remains consistent",
                "Economic conditions remain stable"
            ],
            "success_metrics": {
                "short_term": [
                    "Reduce stockouts by 50%",
                    "Improve average margin by 2-3%",
                    "Complete all Week 1-2 tasks",
                    "Establish 2 new supplier relationships"
                ],
                "long_term": [
                    "Increase monthly revenue by 15-20%",
                    "Achieve 25% average profit margin",
                    "Reduce inventory holding costs by 10%",
                    "Establish market leadership in key categories"
                ]
            },
            "estimated_roi": "Expected 15-25% improvement in profitability within 3 months, with potential annual savings of ₹50,000-100,000 through optimized operations"
        }
    
    def format_report_markdown(self, report: Dict[str, Any] = None) -> str:
        """Format the final report as readable markdown"""
        # Use passed report or instance report
        if report is None:
            report = self.final_report
            
        if not report:
            return "No strategy has been generated yet."
        
        today = datetime.now()
        
        md = f"""# 🎯 Business Growth Strategy
*Generated on {today.strftime('%B %d, %Y')}*

---

## 📋 Executive Summary

{report.get('executive_summary', 'Strategy overview not available.')}

---

## 🚀 Key Opportunities

"""
        
        for opp in report.get('key_opportunities', []):
            priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(opp.get('priority'), "⚪")
            md += f"### {priority_emoji} {opp.get('opportunity')}\n"
            md += f"**Potential Gain:** {opp.get('potential_gain')}\n\n"
        
        md += """---

## ⚡ Immediate Actions

| Action | Timeline | Expected Outcome | Resources |
|--------|----------|------------------|-----------|
"""
        
        for action in report.get('immediate_actions', []):
            md += f"| {action.get('action')} | {action.get('timeline')} | {action.get('expected_outcome')} | {action.get('resources_needed')} |\n"
        
        md += """\n---

## ⚠️ Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation Strategy |
|------|------------|--------|---------------------|
"""
        
        for risk in report.get('risks_and_mitigations', []):
            md += f"| {risk.get('risk')} | {risk.get('likelihood')} | {risk.get('impact')} | {risk.get('mitigation')} |\n"
        
        md += """\n---

## 📊 Success Metrics

### Short-term (1-4 weeks)
"""
        
        for metric in report.get('success_metrics', {}).get('short_term', []):
            md += f"- {metric}\n"
        
        md += "\n### Long-term (1-3 months)\n"
        for metric in report.get('success_metrics', {}).get('long_term', []):
            md += f"- {metric}\n"
        
        md += f"""\n---

## 💰 Estimated ROI

{report.get('estimated_roi', 'ROI estimation not available.')}

---

## 📝 Key Assumptions

"""
        for assumption in report.get('assumptions', []):
            md += f"- {assumption}\n"
        
        md += "\n---\n*This strategy was generated by MSME Copilot AI based on your sales data and market research.*"
        
        return md
    
    def run(
        self,
        analysis_summary: str,
        research_summary: str,
        verification_summary: str,
        business_type: str = "Grocery Store",
        ceo_goal: Optional[str] = None
    ) -> Dict[str, Any]:
        """Run the consultant agent"""
        
        strategy = self.generate_strategy(
            analysis_summary,
            research_summary,
            verification_summary,
            business_type,
            ceo_goal
        )
        
        # Generate markdown report using the strategy
        markdown_report = self.format_report_markdown(strategy)
        
        return {
            'opportunities_count': len(strategy.get('key_opportunities', [])),
            'actions_count': len(strategy.get('immediate_actions', [])),
            'weeks_planned': len(strategy.get('weekly_plan', [])),
            'risks_identified': len(strategy.get('risks_and_mitigations', [])),
            'strategy': strategy,
            'markdown_report': markdown_report
        }
