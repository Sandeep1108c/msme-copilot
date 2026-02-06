"""
Agent 3: Web Researcher Agent
Executes web searches using Tavily and collects sources
"""
from tavily import TavilyClient
from typing import Dict, List, Any, Optional
import time

from config import TAVILY_API_KEY, MAX_SEARCH_RESULTS, MAX_SOURCES_PER_TASK


class WebResearcherAgent:
    """
    Performs autonomous web research using Tavily search API.
    Collects and formats sources for verification.
    """
    
    def __init__(self):
        self.client = TavilyClient(api_key=TAVILY_API_KEY)
        self.all_sources = []
        self.research_results = []
        
    def search_single_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute search for a single research task"""
        query = task.get('search_query', '')
        
        if not query:
            return {
                'task_id': task.get('task_id'),
                'status': 'error',
                'error': 'No search query provided'
            }
        
        try:
            # Execute Tavily search
            response = self.client.search(
                query=query,
                search_depth="advanced",
                max_results=MAX_SEARCH_RESULTS,
                include_answer=True,
                include_raw_content=False
            )
            
            # Extract and format results
            sources = []
            for result in response.get('results', [])[:MAX_SOURCES_PER_TASK]:
                source = {
                    'title': result.get('title', 'Unknown'),
                    'url': result.get('url', ''),
                    'content': result.get('content', '')[:500],  # Limit content length
                    'score': result.get('score', 0),
                    'query': query,
                    'task_id': task.get('task_id')
                }
                sources.append(source)
                self.all_sources.append(source)
            
            return {
                'task_id': task.get('task_id'),
                'task_type': task.get('task_type'),
                'query': query,
                'status': 'success',
                'answer': response.get('answer', ''),
                'sources': sources,
                'num_sources': len(sources)
            }
            
        except Exception as e:
            return {
                'task_id': task.get('task_id'),
                'query': query,
                'status': 'error',
                'error': str(e),
                'sources': []
            }
    
    def research_all_tasks(
        self, 
        tasks: List[Dict[str, Any]],
        progress_callback: Optional[callable] = None
    ) -> List[Dict[str, Any]]:
        """Execute research for all tasks with progress updates"""
        
        self.research_results = []
        self.all_sources = []
        
        for i, task in enumerate(tasks):
            if progress_callback:
                progress_callback(i + 1, len(tasks), task.get('search_query', ''))
            
            result = self.search_single_task(task)
            self.research_results.append(result)
            
            # Small delay to avoid rate limiting
            time.sleep(0.5)
        
        return self.research_results
    
    def get_all_sources(self) -> List[Dict[str, Any]]:
        """Get all collected sources across all searches"""
        return self.all_sources
    
    def get_sources_by_task(self, task_id: int) -> List[Dict[str, Any]]:
        """Get sources for a specific task"""
        return [s for s in self.all_sources if s.get('task_id') == task_id]
    
    def format_sources_for_display(self) -> List[Dict[str, str]]:
        """Format sources for UI sidebar display"""
        formatted = []
        seen_urls = set()
        
        for source in self.all_sources:
            url = source.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                formatted.append({
                    'title': source.get('title', 'Unknown Source'),
                    'url': url,
                    'snippet': source.get('content', '')[:150] + '...' if source.get('content') else '',
                    'query': source.get('query', '')
                })
        
        return formatted
    
    def get_research_summary(self) -> str:
        """Get a text summary of all research for LLM consumption"""
        if not self.research_results:
            return "No research has been conducted yet."
        
        summary = "=== WEB RESEARCH FINDINGS ===\n\n"
        
        for result in self.research_results:
            if result.get('status') == 'success':
                summary += f"📌 RESEARCH TASK: {result.get('query')}\n"
                summary += f"Answer: {result.get('answer', 'No direct answer')}\n"
                summary += f"Sources Found: {result.get('num_sources', 0)}\n"
                
                for source in result.get('sources', []):
                    summary += f"  - [{source.get('title')}]({source.get('url')})\n"
                    summary += f"    Key info: {source.get('content', '')[:200]}...\n"
                
                summary += "\n"
        
        summary += f"\n📊 TOTAL SOURCES INVESTIGATED: {len(self.all_sources)}\n"
        
        return summary
    
    def run(
        self,
        research_tasks: List[Dict[str, Any]],
        progress_callback: Optional[callable] = None
    ) -> Dict[str, Any]:
        """Run the web researcher agent"""
        
        results = self.research_all_tasks(research_tasks, progress_callback)
        
        successful = sum(1 for r in results if r.get('status') == 'success')
        failed = sum(1 for r in results if r.get('status') == 'error')
        
        return {
            'total_searches': len(results),
            'successful': successful,
            'failed': failed,
            'total_sources': len(self.all_sources),
            'results': results,
            'formatted_sources': self.format_sources_for_display()
        }
