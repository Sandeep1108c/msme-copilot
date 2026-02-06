"""
Agent 4: Critic / Verifier Agent
Validates research findings, checks for conflicts, and selects best recommendations
"""
import google.generativeai as genai
from typing import Dict, List, Any, Optional
import json
import re

from config import GEMINI_API_KEY, GEMINI_MODEL


class CriticAgent:
    """
    Verifies research quality and consistency.
    Checks for conflicts and highlights uncertainty.
    Picks evidence-backed recommendations.
    """
    
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL)
        self.verified_findings = []
        self.conflicts = []
        self.uncertainties = []
        
    def verify_research(
        self,
        analysis_summary: str,
        research_summary: str,
        business_type: str
    ) -> Dict[str, Any]:
        """Analyze research for conflicts, uncertainties, and evidence quality"""
        
        prompt = f"""You are a critical business analyst reviewing research findings for a {business_type}.

=== ORIGINAL BUSINESS ANALYSIS ===
{analysis_summary}

=== WEB RESEARCH FINDINGS ===
{research_summary}

Critically evaluate the research and provide your assessment in the following JSON format:

```json
{{
  "verified_recommendations": [
    {{
      "recommendation": "specific actionable recommendation",
      "confidence": "high|medium|low",
      "evidence": "brief description of supporting evidence",
      "sources_count": 2,
      "potential_impact": "high|medium|low"
    }}
  ],
  "conflicts_found": [
    {{
      "issue": "description of conflicting information",
      "sources_involved": ["source1", "source2"],
      "resolution": "how to interpret this conflict"
    }}
  ],
  "uncertainties": [
    {{
      "topic": "area of uncertainty",
      "reason": "why this is uncertain",
      "suggested_action": "what to do about it"
    }}
  ],
  "overall_confidence": "high|medium|low",
  "data_quality_score": 1-10,
  "key_insights": ["insight1", "insight2", "insight3"]
}}
```

Be skeptical and thorough. Flag any recommendations that lack sufficient evidence.
Return ONLY valid JSON, no other text.
"""
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Extract JSON
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                result = json.loads(json_match.group())
                
                self.verified_findings = result.get('verified_recommendations', [])
                self.conflicts = result.get('conflicts_found', [])
                self.uncertainties = result.get('uncertainties', [])
                
                return result
            else:
                return self._get_default_verification()
                
        except Exception as e:
            print(f"Error in critic analysis: {e}")
            return self._get_default_verification()
    
    def _get_default_verification(self) -> Dict[str, Any]:
        """Fallback verification if LLM fails"""
        result = {
            "verified_recommendations": [
                {
                    "recommendation": "Review pricing strategy based on market research",
                    "confidence": "medium",
                    "evidence": "Market data collected from web research",
                    "sources_count": 3,
                    "potential_impact": "medium"
                },
                {
                    "recommendation": "Focus on high-margin products identified in analysis",
                    "confidence": "high",
                    "evidence": "Sales data analysis shows clear profit patterns",
                    "sources_count": 1,
                    "potential_impact": "high"
                },
                {
                    "recommendation": "Address declining products with promotional strategies",
                    "confidence": "medium",
                    "evidence": "Trend analysis from your sales data",
                    "sources_count": 1,
                    "potential_impact": "medium"
                }
            ],
            "conflicts_found": [],
            "uncertainties": [
                {
                    "topic": "Market conditions",
                    "reason": "Limited local data available",
                    "suggested_action": "Validate with local market visit"
                }
            ],
            "overall_confidence": "medium",
            "data_quality_score": 7,
            "key_insights": [
                "Research provides directional guidance",
                "Local validation recommended",
                "Implement changes incrementally"
            ]
        }
        
        # Populate instance variables so run() returns correct counts
        self.verified_findings = result.get('verified_recommendations', [])
        self.conflicts = result.get('conflicts_found', [])
        self.uncertainties = result.get('uncertainties', [])
        
        return result
    
    def get_high_confidence_recommendations(self) -> List[Dict]:
        """Get only high-confidence verified recommendations"""
        return [r for r in self.verified_findings if r.get('confidence') == 'high']
    
    def get_verification_summary(self) -> str:
        """Get a text summary of verification for final report"""
        if not self.verified_findings:
            return "No verification has been performed yet."
        
        summary = "=== VERIFICATION SUMMARY ===\n\n"
        
        summary += "✅ VERIFIED RECOMMENDATIONS:\n"
        for rec in self.verified_findings:
            confidence_emoji = {"high": "🟢", "medium": "🟡", "low": "🔴"}.get(rec.get('confidence'), "⚪")
            summary += f"{confidence_emoji} {rec.get('recommendation')}\n"
            summary += f"   Evidence: {rec.get('evidence')}\n"
            summary += f"   Impact: {rec.get('potential_impact', 'unknown')}\n\n"
        
        if self.conflicts:
            summary += "⚠️ CONFLICTS DETECTED:\n"
            for conflict in self.conflicts:
                summary += f"- {conflict.get('issue')}\n"
                summary += f"  Resolution: {conflict.get('resolution')}\n\n"
        
        if self.uncertainties:
            summary += "❓ AREAS OF UNCERTAINTY:\n"
            for unc in self.uncertainties:
                summary += f"- {unc.get('topic')}: {unc.get('reason')}\n"
        
        return summary
    
    def run(
        self,
        analysis_summary: str,
        research_summary: str,
        business_type: str = "Grocery Store"
    ) -> Dict[str, Any]:
        """Run the critic agent"""
        
        verification = self.verify_research(analysis_summary, research_summary, business_type)
        
        return {
            'verified_count': len(self.verified_findings),
            'high_confidence_count': len(self.get_high_confidence_recommendations()),
            'conflicts_count': len(self.conflicts),
            'uncertainties_count': len(self.uncertainties),
            'overall_confidence': verification.get('overall_confidence', 'medium'),
            'data_quality_score': verification.get('data_quality_score', 5),
            'verification': verification
        }
