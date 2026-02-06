"""
Agent Orchestrator
Coordinates all agents in the MSME Copilot pipeline
"""
from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass

from .data_analyst import DataAnalystAgent
from .planner import PlannerAgent
from .web_researcher import WebResearcherAgent
from .critic import CriticAgent
from .consultant import ConsultantAgent


@dataclass
class PipelineState:
    """Tracks the state of the agent pipeline"""
    current_agent: str = ""
    progress: float = 0.0
    status: str = "idle"
    analysis_complete: bool = False
    planning_complete: bool = False
    research_complete: bool = False
    verification_complete: bool = False
    strategy_complete: bool = False


class AgentOrchestrator:
    """
    Orchestrates the 5-agent pipeline for MSME business analysis.
    
    Pipeline:
    1. Data Analyst → Analyze sales data
    2. Planner → Create research tasks
    3. Web Researcher → Gather market intelligence
    4. Critic → Verify and validate findings
    5. Consultant → Generate final strategy
    """
    
    def __init__(self):
        self.data_analyst = DataAnalystAgent()
        self.planner = PlannerAgent()
        self.web_researcher = WebResearcherAgent()
        self.critic = CriticAgent()
        self.consultant = ConsultantAgent()
        
        self.state = PipelineState()
        self.results = {}
        
    def run_pipeline(
        self,
        sales_file,
        business_type: str = "Grocery Store",
        ceo_goal: Optional[str] = None,
        progress_callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        Execute the complete agent pipeline.
        
        Args:
            sales_file: CSV file path or file object
            business_type: Type of business
            ceo_goal: Optional CEO's specific goal
            progress_callback: Optional callback for progress updates
                               Signature: callback(agent_name, progress_pct, status_message)
        """
        
        def update_progress(agent: str, progress: float, status: str):
            self.state.current_agent = agent
            self.state.progress = progress
            self.state.status = status
            if progress_callback:
                progress_callback(agent, progress, status)
        
        try:
            # ===== AGENT 1: DATA ANALYST =====
            update_progress("Data Analyst", 0.05, "📊 Analyzing sales data...")
            
            analysis_results = self.data_analyst.run(sales_file)
            analysis_summary = self.data_analyst.get_analysis_summary_text()
            
            self.results['analysis'] = analysis_results
            self.results['analysis_summary'] = analysis_summary
            self.state.analysis_complete = True
            
            update_progress("Data Analyst", 0.20, "✅ Sales analysis complete!")
            
            # ===== AGENT 2: PLANNER =====
            update_progress("Planner", 0.25, "📋 Creating research plan...")
            
            planning_results = self.planner.run(
                analysis_summary=analysis_summary,
                business_type=business_type,
                ceo_goal=ceo_goal
            )
            
            self.results['planning'] = planning_results
            self.state.planning_complete = True
            
            update_progress("Planner", 0.35, f"✅ Created {planning_results['total_tasks']} research tasks")
            
            # ===== AGENT 3: WEB RESEARCHER =====
            update_progress("Web Researcher", 0.40, "🔍 Researching market intelligence...")
            
            def research_progress(current, total, query):
                pct = 0.40 + (current / total) * 0.25
                update_progress("Web Researcher", pct, f"🔍 Searching: {query[:50]}...")
            
            research_results = self.web_researcher.run(
                research_tasks=planning_results['tasks'],
                progress_callback=research_progress
            )
            
            research_summary = self.web_researcher.get_research_summary()
            
            self.results['research'] = research_results
            self.results['research_summary'] = research_summary
            self.results['sources'] = self.web_researcher.format_sources_for_display()
            self.state.research_complete = True
            
            update_progress("Web Researcher", 0.65, f"✅ Found {research_results['total_sources']} sources")
            
            # ===== AGENT 4: CRITIC =====
            update_progress("Critic", 0.70, "🔎 Verifying research quality...")
            
            critic_results = self.critic.run(
                analysis_summary=analysis_summary,
                research_summary=research_summary,
                business_type=business_type
            )
            
            verification_summary = self.critic.get_verification_summary()
            
            self.results['verification'] = critic_results
            self.results['verification_summary'] = verification_summary
            self.state.verification_complete = True
            
            update_progress("Critic", 0.80, f"✅ Verified {critic_results['verified_count']} recommendations")
            
            # ===== AGENT 5: CONSULTANT =====
            update_progress("Consultant", 0.85, "📝 Generating final strategy...")
            
            consultant_results = self.consultant.run(
                analysis_summary=analysis_summary,
                research_summary=research_summary,
                verification_summary=verification_summary,
                business_type=business_type,
                ceo_goal=ceo_goal
            )
            
            self.results['strategy'] = consultant_results
            self.results['final_report'] = consultant_results['markdown_report']
            self.state.strategy_complete = True
            
            update_progress("Consultant", 1.0, "🎉 Strategy generation complete!")
            
            return {
                'success': True,
                'results': self.results,
                'state': self.state
            }
            
        except Exception as e:
            update_progress(self.state.current_agent, self.state.progress, f"❌ Error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'results': self.results,
                'state': self.state
            }
    
    def get_sources(self) -> list:
        """Get all collected sources"""
        return self.results.get('sources', [])
    
    def get_final_report(self) -> str:
        """Get the final markdown report"""
        return self.results.get('final_report', '')
    
    def get_analysis_results(self) -> Dict:
        """Get raw analysis results"""
        return self.results.get('analysis', {})
