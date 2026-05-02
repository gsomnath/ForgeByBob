# Enhancement 1-C: Research Agent Implementation

## Module Overview
This module adds an intelligent Research Agent that autonomously gathers information, validates sources, and creates structured research briefs. This is **fully functional** and enhances the Writer Agent with factual, well-researched context.

## What This Module Delivers
- ✅ Research Agent with web search capabilities
- ✅ Source credibility assessment
- ✅ Fact extraction and summarization
- ✅ Structured research brief generation
- ✅ 3-agent pipeline (Research → Writer → Publisher)
- ✅ Research caching for efficiency

## Prerequisites
- Enhancement 1-A completed (Granite client working)
- Enhancement 1-B completed (Orchestration framework working)
- Python 3.11+

## Implementation Time: 1.5-2 hours

---

## Part 1: Web Search Integration (30 minutes)

### Step 1.1: Choose Search Provider

**Options:**

**Option A: DuckDuckGo (Recommended for Hackathon)**
- ✅ No API key required
- ✅ Free unlimited searches
- ✅ Privacy-focused
- ✅ Easy to implement

**Option B: Google Custom Search**
- Requires API key
- 100 free searches/day
- More comprehensive results

**Option C: Bing Search API**
- Requires Azure account
- 1000 free searches/month
- Good quality results

**We'll use DuckDuckGo for simplicity.**

### Step 1.2: Install Search Dependencies

```bash
# Add to requirements.txt
duckduckgo-search>=4.0.0
beautifulsoup4>=4.12.0
requests>=2.31.0
```

```bash
# Install dependencies
pip install duckduckgo-search beautifulsoup4 requests
```

### Step 1.3: Create Search Tool

**File: `services/orchestration_service/tools/web_search.py`**

```python
"""
Web search tool using DuckDuckGo
"""
from duckduckgo_search import DDGS
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime
import hashlib
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class WebSearchTool:
    """Tool for performing web searches"""
    
    def __init__(self, cache_dir: str = "data/search_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ddgs = DDGS()
        logger.info("Web search tool initialized")
    
    def _get_cache_key(self, query: str) -> str:
        """Generate cache key for query"""
        return hashlib.md5(query.encode()).hexdigest()
    
    def _get_cached_results(self, query: str) -> Optional[List[Dict[str, Any]]]:
        """Get cached search results"""
        cache_key = self._get_cache_key(query)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cached = json.load(f)
                    # Check if cache is less than 24 hours old
                    cache_time = datetime.fromisoformat(cached['timestamp'])
                    age_hours = (datetime.utcnow() - cache_time).total_seconds() / 3600
                    
                    if age_hours < 24:
                        logger.info(f"Using cached results for query: {query[:50]}...")
                        return cached['results']
            except Exception as e:
                logger.warning(f"Failed to load cache: {str(e)}")
        
        return None
    
    def _cache_results(self, query: str, results: List[Dict[str, Any]]):
        """Cache search results"""
        cache_key = self._get_cache_key(query)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        try:
            cache_data = {
                'query': query,
                'timestamp': datetime.utcnow().isoformat(),
                'results': results
            }
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Cached results for query: {query[:50]}...")
        except Exception as e:
            logger.warning(f"Failed to cache results: {str(e)}")
    
    def search(
        self,
        query: str,
        max_results: int = 10,
        use_cache: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Perform web search
        
        Args:
            query: Search query
            max_results: Maximum number of results
            use_cache: Whether to use cached results
            
        Returns:
            List of search results with title, url, snippet
        """
        try:
            # Check cache first
            if use_cache:
                cached = self._get_cached_results(query)
                if cached:
                    return cached[:max_results]
            
            logger.info(f"Searching web for: {query}")
            
            # Perform search
            results = []
            search_results = self.ddgs.text(query, max_results=max_results)
            
            for result in search_results:
                results.append({
                    'title': result.get('title', ''),
                    'url': result.get('href', ''),
                    'snippet': result.get('body', ''),
                    'source': self._extract_domain(result.get('href', ''))
                })
            
            logger.info(f"Found {len(results)} results")
            
            # Cache results
            if use_cache:
                self._cache_results(query, results)
            
            return results
            
        except Exception as e:
            logger.error(f"Search failed: {str(e)}")
            return []
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL"""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            return parsed.netloc
        except:
            return url
    
    def search_multiple_queries(
        self,
        queries: List[str],
        max_results_per_query: int = 5
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Search multiple queries
        
        Args:
            queries: List of search queries
            max_results_per_query: Max results per query
            
        Returns:
            Dictionary mapping queries to results
        """
        results = {}
        for query in queries:
            results[query] = self.search(query, max_results=max_results_per_query)
        return results


# Global search tool instance
_search_tool: Optional[WebSearchTool] = None


def get_search_tool() -> WebSearchTool:
    """Get or create global search tool instance"""
    global _search_tool
    if _search_tool is None:
        _search_tool = WebSearchTool()
    return _search_tool
```

---

## Part 2: Research Agent Implementation (45 minutes)

### Step 2.1: Create Research Agent

**File: `services/orchestration_service/agents/research_agent.py`**

```python
"""
Research Agent - Gathers and validates information using web search and Granite
"""
from ..agent_base import BaseAgent, AgentResult
from ..tools.web_search import get_search_tool
from services.watsonx_service.granite_client import get_granite_client
from typing import Dict, Any, List
import logging
import json

logger = logging.getLogger(__name__)


class ResearchAgent(BaseAgent):
    """Agent for researching topics and gathering information"""
    
    def __init__(self, agent_id=None):
        super().__init__(agent_id)
        self.search_tool = get_search_tool()
        self.granite = get_granite_client()
        self.system_prompt = """You are a research analyst specializing in gathering 
        and validating information. Your role is to:
        1. Analyze search results for credibility and relevance
        2. Extract key facts and statistics
        3. Identify authoritative sources
        4. Synthesize information into a coherent research brief
        5. Flag any conflicting information or gaps
        
        Be objective, thorough, and cite sources appropriately."""
    
    async def execute(self, input_data: Dict[str, Any]) -> AgentResult:
        """
        Research a topic
        
        Expected input_data:
        {
            "topic": "Topic to research",
            "focus_areas": ["Optional list of specific areas to focus on"],
            "max_sources": 10
        }
        
        Returns:
            AgentResult with research brief
        """
        try:
            topic = input_data.get("topic", "")
            focus_areas = input_data.get("focus_areas", [])
            max_sources = input_data.get("max_sources", 10)
            
            if not topic:
                return AgentResult(
                    success=False,
                    error="No topic provided"
                )
            
            logger.info(f"ResearchAgent: Researching topic: {topic}")
            
            # Step 1: Generate search queries
            search_queries = await self._generate_search_queries(topic, focus_areas)
            logger.info(f"ResearchAgent: Generated {len(search_queries)} search queries")
            
            # Step 2: Perform web searches
            search_results = self._perform_searches(search_queries, max_sources)
            logger.info(f"ResearchAgent: Found {sum(len(r) for r in search_results.values())} total results")
            
            # Step 3: Evaluate source credibility
            evaluated_sources = await self._evaluate_sources(search_results)
            logger.info(f"ResearchAgent: Evaluated {len(evaluated_sources)} sources")
            
            # Step 4: Extract key facts
            key_facts = await self._extract_key_facts(evaluated_sources, topic)
            logger.info(f"ResearchAgent: Extracted {len(key_facts)} key facts")
            
            # Step 5: Generate research brief
            research_brief = await self._generate_research_brief(
                topic, evaluated_sources, key_facts
            )
            logger.info(f"ResearchAgent: Generated research brief ({len(research_brief)} chars)")
            
            return AgentResult(
                success=True,
                data={
                    "topic": topic,
                    "research_brief": research_brief,
                    "sources": evaluated_sources,
                    "key_facts": key_facts,
                    "search_queries": search_queries,
                    "total_sources": len(evaluated_sources)
                },
                metadata={
                    "focus_areas": focus_areas,
                    "max_sources": max_sources
                }
            )
            
        except Exception as e:
            logger.error(f"ResearchAgent: Research failed: {str(e)}")
            return AgentResult(
                success=False,
                error=str(e)
            )
    
    async def _generate_search_queries(
        self,
        topic: str,
        focus_areas: List[str]
    ) -> List[str]:
        """Generate effective search queries"""
        prompt = f"""Generate 3-5 effective search queries for researching this topic:

Topic: {topic}

{f"Focus on these areas: {', '.join(focus_areas)}" if focus_areas else ""}

Generate queries that will find:
- Authoritative sources
- Recent information
- Statistical data
- Expert opinions

Respond with a JSON array of search queries:
["query1", "query2", "query3"]"""
        
        try:
            response = self.granite.generate(
                prompt=prompt,
                system_prompt=self.system_prompt,
                max_tokens=200,
                temperature=0.5
            )
            
            # Parse JSON response
            queries = json.loads(response.strip())
            
            # Ensure we have a list
            if isinstance(queries, list):
                return queries[:5]  # Max 5 queries
            else:
                # Fallback to simple query
                return [topic]
                
        except Exception as e:
            logger.warning(f"Failed to generate queries: {str(e)}, using topic as query")
            return [topic]
    
    def _perform_searches(
        self,
        queries: List[str],
        max_sources: int
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Perform web searches for all queries"""
        results_per_query = max(3, max_sources // len(queries))
        return self.search_tool.search_multiple_queries(queries, results_per_query)
    
    async def _evaluate_sources(
        self,
        search_results: Dict[str, List[Dict[str, Any]]]
    ) -> List[Dict[str, Any]]:
        """Evaluate source credibility"""
        all_sources = []
        
        for query, results in search_results.items():
            for result in results:
                all_sources.append(result)
        
        # Remove duplicates by URL
        unique_sources = {}
        for source in all_sources:
            url = source['url']
            if url not in unique_sources:
                unique_sources[url] = source
        
        evaluated = []
        
        for source in list(unique_sources.values())[:15]:  # Evaluate top 15
            credibility = await self._assess_credibility(source)
            source['credibility_score'] = credibility
            evaluated.append(source)
        
        # Sort by credibility
        evaluated.sort(key=lambda x: x['credibility_score'], reverse=True)
        
        return evaluated[:10]  # Return top 10
    
    async def _assess_credibility(self, source: Dict[str, Any]) -> float:
        """Assess source credibility (0-1)"""
        # Simple heuristic-based credibility scoring
        score = 0.5  # Base score
        
        domain = source.get('source', '').lower()
        
        # High credibility domains
        high_cred = ['.edu', '.gov', '.org', 'wikipedia', 'nature.com', 
                     'science.org', 'ieee.org', 'acm.org']
        if any(d in domain for d in high_cred):
            score += 0.3
        
        # Medium credibility domains
        med_cred = ['medium.com', 'forbes.com', 'techcrunch.com', 'wired.com']
        if any(d in domain for d in med_cred):
            score += 0.15
        
        # Penalize certain domains
        low_cred = ['blogspot', 'wordpress.com', 'tumblr']
        if any(d in domain for d in low_cred):
            score -= 0.2
        
        # Bonus for HTTPS
        if source.get('url', '').startswith('https'):
            score += 0.05
        
        return max(0.0, min(1.0, score))
    
    async def _extract_key_facts(
        self,
        sources: List[Dict[str, Any]],
        topic: str
    ) -> List[Dict[str, Any]]:
        """Extract key facts from sources"""
        # Prepare source summaries
        source_text = "\n\n".join([
            f"Source: {s['title']}\nURL: {s['url']}\n{s['snippet']}"
            for s in sources[:5]  # Use top 5 sources
        ])
        
        prompt = f"""Extract 5-7 key facts about this topic from the provided sources:

Topic: {topic}

Sources:
{source_text}

For each fact, provide:
1. The fact statement
2. Source URL
3. Confidence level (high/medium/low)

Respond with JSON array:
[
  {{
    "fact": "fact statement",
    "source_url": "url",
    "confidence": "high"
  }}
]"""
        
        try:
            response = self.granite.generate(
                prompt=prompt,
                system_prompt=self.system_prompt,
                max_tokens=500,
                temperature=0.3
            )
            
            facts = json.loads(response.strip())
            return facts if isinstance(facts, list) else []
            
        except Exception as e:
            logger.warning(f"Failed to extract facts: {str(e)}")
            return []
    
    async def _generate_research_brief(
        self,
        topic: str,
        sources: List[Dict[str, Any]],
        key_facts: List[Dict[str, Any]]
    ) -> str:
        """Generate comprehensive research brief"""
        # Prepare sources summary
        sources_summary = "\n".join([
            f"- {s['title']} ({s['source']}) - Credibility: {s['credibility_score']:.2f}"
            for s in sources[:5]
        ])
        
        # Prepare facts summary
        facts_summary = "\n".join([
            f"- {f['fact']} (Confidence: {f.get('confidence', 'medium')})"
            for f in key_facts
        ])
        
        prompt = f"""Create a comprehensive research brief for this topic:

Topic: {topic}

Top Sources:
{sources_summary}

Key Facts:
{facts_summary}

Generate a research brief that includes:
1. Overview of the topic
2. Key findings and insights
3. Important statistics or data points
4. Current trends or developments
5. Recommended angles for blog content

Write in a clear, professional style suitable for a content writer."""
        
        research_brief = self.granite.generate(
            prompt=prompt,
            system_prompt=self.system_prompt,
            max_tokens=1000,
            temperature=0.6
        )
        
        return research_brief
```

### Step 2.2: Register Research Agent

**File: `services/orchestration_service/agents/__init__.py`**

```python
"""
Agent implementations
"""
from .writer_agent import WriterAgent
from .publisher_agent import PublisherAgent
from .research_agent import ResearchAgent

__all__ = ['WriterAgent', 'PublisherAgent', 'ResearchAgent']
```

### Step 2.3: Update Orchestration Service

**File: `services/orchestration_service/main.py`**

Add research agent registration:

```python
# Update imports
from .agents import WriterAgent, PublisherAgent, ResearchAgent

# Update startup event
@app.on_event("startup")
async def startup_event():
    """Register agents on startup"""
    logger.info("Registering agents...")
    agent_registry.register_agent_class("research", ResearchAgent)
    agent_registry.register_agent_class("writer", WriterAgent)
    agent_registry.register_agent_class("publisher", PublisherAgent)
    logger.info("Agents registered successfully")
```

---

## Part 3: Enhanced Blog Generation Pipeline (30 minutes)

### Step 3.1: Create 3-Agent Pipeline Endpoint

**File: `services/orchestration_service/main.py`**

Add new endpoint:

```python
class ResearchedBlogRequest(BaseModel):
    topic: str
    focus_areas: Optional[List[str]] = []
    tone: Optional[str] = "professional"
    blog_id: Optional[str] = None


@app.post("/blog/generate-researched")
async def generate_researched_blog(request: ResearchedBlogRequest):
    """
    Generate blog with research using Research → Writer → Publisher pipeline
    
    This creates a 3-agent pipeline that:
    1. Research Agent: Gathers information and creates research brief
    2. Writer Agent: Uses research brief to write content
    3. Publisher Agent: Publishes the final content
    """
    try:
        # Create pipeline
        pipeline = pipeline_manager.create_pipeline("Researched Blog Generation Pipeline")
        
        # Add agents
        pipeline.add_step("research")
        pipeline.add_step(
            "writer",
            input_mapping={
                "prompt": "topic",
                "research_brief": "research_brief"
            }
        )
        pipeline.add_step("publisher")
        
        # Execute pipeline
        input_data = {
            "topic": request.topic,
            "focus_areas": request.focus_areas,
            "tone": request.tone,
            "blog_id": request.blog_id,
            "max_sources": 10
        }
        
        logger.info(f"Starting researched blog generation for topic: {request.topic}")
        result = await pipeline.execute(input_data)
        
        return {
            "success": True,
            "message": "Researched blog generated successfully",
            "data": result
        }
        
    except Exception as e:
        logger.error(f"Researched blog generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/research")
async def research_topic(request: Dict[str, Any]):
    """
    Research a topic without generating blog
    
    Useful for previewing research before writing
    """
    try:
        agent = agent_registry.create_agent("research")
        result = await agent.run(request)
        
        return {
            "success": result.success,
            "data": result.data if result.success else None,
            "error": result.error if not result.success else None
        }
        
    except Exception as e:
        logger.error(f"Research failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
```

---

## Part 4: Testing Research Agent (15 minutes)

### Step 4.1: Test Research Endpoint

```bash
# Test research only
curl -X POST http://localhost:8004/research \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Artificial Intelligence in Healthcare",
    "focus_areas": ["diagnosis", "treatment", "patient care"],
    "max_sources": 10
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "data": {
    "topic": "Artificial Intelligence in Healthcare",
    "research_brief": "...",
    "sources": [
      {
        "title": "...",
        "url": "...",
        "credibility_score": 0.85
      }
    ],
    "key_facts": [
      {
        "fact": "...",
        "source_url": "...",
        "confidence": "high"
      }
    ],
    "total_sources": 10
  }
}
```

### Step 4.2: Test Full 3-Agent Pipeline

```bash
# Test researched blog generation
curl -X POST http://localhost:8004/blog/generate-researched \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "The Future of Quantum Computing",
    "focus_areas": ["applications", "challenges", "timeline"],
    "tone": "professional"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Researched blog generated successfully",
  "data": {
    "pipeline_id": "...",
    "state": "completed",
    "steps": [
      {
        "agent_name": "research",
        "completed": true,
        "success": true
      },
      {
        "agent_name": "writer",
        "completed": true,
        "success": true
      },
      {
        "agent_name": "publisher",
        "completed": true,
        "success": true
      }
    ],
    "duration_seconds": 25.3
  }
}
```

### Step 4.3: Verify Research Quality

```bash
# Check published blog
cat data/published_blogs/blog_*.json | jq '.metadata'
```

Should show research sources and facts used.

---

## Part 5: UI Integration (15 minutes)

### Step 5.1: Update Create Blog Form

**File: `services/ui_service/templates/create.html`**

```html
<form method="post" action="/create">
    <div class="form-group">
        <label for="title">Blog Title</label>
        <input type="text" id="title" name="title" required>
    </div>
    
    <div class="form-group">
        <label for="initial_prompt">Topic or Prompt</label>
        <textarea id="initial_prompt" name="initial_prompt" rows="4" required></textarea>
    </div>
    
    <div class="form-group">
        <label for="focus_areas">Focus Areas (comma-separated, optional)</label>
        <input type="text" id="focus_areas" name="focus_areas" 
               placeholder="e.g., applications, benefits, challenges">
    </div>
    
    <div class="form-group">
        <label>Generation Mode:</label>
        <div class="radio-group">
            <label>
                <input type="radio" name="generation_mode" value="simple" checked>
                Simple (Writer only)
            </label>
            <label>
                <input type="radio" name="generation_mode" value="researched">
                Researched (Research → Writer → Publisher)
            </label>
        </div>
    </div>
    
    <button type="submit">Create Blog</button>
</form>
```

### Step 5.2: Update UI Service Handler

**File: `services/ui_service/main.py`**

```python
@app.post("/create")
async def create_blog_submit(
    request: Request,
    title: str = Form(...),
    initial_prompt: str = Form(...),
    focus_areas: str = Form(""),
    generation_mode: str = Form("simple"),
    # ... other fields
):
    """Handle blog creation with research option"""
    try:
        if generation_mode == "researched":
            # Use researched blog generation
            focus_list = [f.strip() for f in focus_areas.split(",") if f.strip()]
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"http://localhost:8004/blog/generate-researched",
                    json={
                        "topic": initial_prompt,
                        "focus_areas": focus_list,
                        "tone": "professional"
                    },
                    timeout=120.0  # Longer timeout for research
                )
                
                if response.status_code == 200:
                    return RedirectResponse(url="/", status_code=303)
        else:
            # Use simple generation (existing code)
            # ...
            pass
            
    except Exception as e:
        return templates.TemplateResponse("create.html", {
            "request": request,
            "error": str(e)
        })
```

---

## Success Criteria

### ✅ Module Complete When:
1. Research Agent successfully searches web
2. Source credibility assessment works
3. Key facts are extracted correctly
4. Research brief is comprehensive
5. 3-agent pipeline executes successfully
6. Blog content includes researched information
7. UI allows choosing research mode

### 📊 Quality Metrics:
- **Research time**: 15-20 seconds
- **Source quality**: Average credibility > 0.6
- **Fact extraction**: 5-7 relevant facts
- **Content quality**: Noticeably better with research

---

## Troubleshooting

### Issue: "No search results found"
**Solution:**
```python
# Test search tool directly
from services.orchestration_service.tools.web_search import get_search_tool

search = get_search_tool()
results = search.search("artificial intelligence")
print(f"Found {len(results)} results")
```

### Issue: "Search too slow"
**Solution:**
- Enable caching (default)
- Reduce max_sources
- Use fewer search queries

### Issue: "Low credibility scores"
**Solution:**
- Adjust credibility heuristics in `_assess_credibility`
- Add more high-credibility domains
- Consider using Granite to assess credibility

---

## Next Steps

After completing this module:
- **Enhancement 1-D**: Reviewer Agent with Self-Correction Loop
- **Enhancement 1-E**: Real-time Agent Dashboard

The Research Agent significantly improves content quality by providing factual, well-sourced information to the Writer Agent.