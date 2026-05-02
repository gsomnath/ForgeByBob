# Enhancement 1-D: Reviewer Agent with Self-Correction Loop

## Module Overview
This module implements the **key differentiator** - a Reviewer Agent with autonomous self-correction loop. This is **fully functional** and demonstrates true agentic behavior where the system improves content quality without human intervention.

## What This Module Delivers
- ✅ Reviewer Agent with multi-dimensional scoring
- ✅ Autonomous self-correction loop (max 3 iterations)
- ✅ Quality threshold enforcement (score ≥ 7.0)
- ✅ Detailed feedback generation for Writer Agent
- ✅ 4-agent pipeline with feedback loop
- ✅ Iteration tracking and improvement metrics

## Prerequisites
- Enhancement 1-A completed (Granite client working)
- Enhancement 1-B completed (Orchestration framework working)
- Enhancement 1-C completed (Research Agent working)
- Python 3.11+

## Implementation Time: 2-2.5 hours

---

## Part 1: Reviewer Agent Core (45 minutes)

### Step 1.1: Create Reviewer Agent

**File: `services/orchestration_service/agents/reviewer_agent.py`**

```python
"""
Reviewer Agent - Evaluates content quality and triggers self-correction loop
"""
from ..agent_base import BaseAgent, AgentResult
from services.watsonx_service.granite_client import get_granite_client
from typing import Dict, Any, List, Optional
import logging
import json

logger = logging.getLogger(__name__)


class ReviewScore:
    """Content review score"""
    
    def __init__(
        self,
        clarity: float,
        accuracy: float,
        engagement: float,
        seo_quality: float
    ):
        self.clarity = clarity
        self.accuracy = accuracy
        self.engagement = engagement
        self.seo_quality = seo_quality
        self.overall = (clarity + accuracy + engagement + seo_quality) / 4.0
    
    def passes_threshold(self, threshold: float = 7.0) -> bool:
        """Check if all scores meet threshold"""
        return all([
            self.clarity >= threshold,
            self.accuracy >= threshold,
            self.engagement >= threshold,
            self.seo_quality >= threshold
        ])
    
    def get_failing_dimensions(self, threshold: float = 7.0) -> List[str]:
        """Get list of dimensions below threshold"""
        failing = []
        if self.clarity < threshold:
            failing.append("clarity")
        if self.accuracy < threshold:
            failing.append("accuracy")
        if self.engagement < threshold:
            failing.append("engagement")
        if self.seo_quality < threshold:
            failing.append("seo_quality")
        return failing
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary"""
        return {
            "clarity": round(self.clarity, 2),
            "accuracy": round(self.accuracy, 2),
            "engagement": round(self.engagement, 2),
            "seo_quality": round(self.seo_quality, 2),
            "overall": round(self.overall, 2)
        }


class ReviewerAgent(BaseAgent):
    """Agent for reviewing and scoring content quality"""
    
    def __init__(self, agent_id=None):
        super().__init__(agent_id)
        self.granite = get_granite_client()
        self.system_prompt = """You are an expert content critic and editor. 
        Your role is to objectively evaluate content across multiple dimensions:
        
        1. CLARITY (1-10): Readability, structure, logical flow
           - Is the writing clear and easy to understand?
           - Are ideas presented in a logical order?
           - Are transitions smooth between sections?
        
        2. ACCURACY (1-10): Factual correctness, source quality
           - Are factual claims supported?
           - Are sources credible?
           - Are there any logical inconsistencies?
        
        3. ENGAGEMENT (1-10): Reader interest, storytelling, value
           - Does the introduction hook the reader?
           - Is the content interesting and valuable?
           - Is there a clear call-to-action?
        
        4. SEO QUALITY (1-10): Search engine optimization
           - Are keywords naturally integrated?
           - Is the heading structure SEO-friendly?
           - Is the content comprehensive enough?
        
        Provide scores (1-10) and specific, actionable feedback for improvement."""
        
        self.quality_threshold = 7.0
    
    async def execute(self, input_data: Dict[str, Any]) -> AgentResult:
        """
        Review content and determine if revision is needed
        
        Expected input_data:
        {
            "content": "Content to review",
            "topic": "Original topic",
            "research_brief": "Optional research context",
            "iteration": 0  # Current iteration number
        }
        
        Returns:
            AgentResult with review scores and feedback
        """
        try:
            content = input_data.get("content", "")
            topic = input_data.get("topic", "")
            research_brief = input_data.get("research_brief", "")
            iteration = input_data.get("iteration", 0)
            
            if not content:
                return AgentResult(
                    success=False,
                    error="No content provided for review"
                )
            
            logger.info(f"ReviewerAgent: Reviewing content (iteration {iteration})")
            
            # Step 1: Evaluate each dimension
            scores = await self._evaluate_content(content, topic, research_brief)
            logger.info(f"ReviewerAgent: Scores - {scores.to_dict()}")
            
            # Step 2: Check if revision is needed
            needs_revision = not scores.passes_threshold(self.quality_threshold)
            
            if needs_revision:
                # Generate improvement feedback
                feedback = await self._generate_feedback(
                    content, topic, scores, research_brief
                )
                logger.info(f"ReviewerAgent: Revision needed - {scores.get_failing_dimensions()}")
                
                return AgentResult(
                    success=True,
                    data={
                        "approved": False,
                        "needs_revision": True,
                        "scores": scores.to_dict(),
                        "feedback": feedback,
                        "failing_dimensions": scores.get_failing_dimensions(),
                        "iteration": iteration
                    },
                    metadata={
                        "quality_threshold": self.quality_threshold,
                        "overall_score": scores.overall
                    }
                )
            else:
                logger.info(f"ReviewerAgent: Content approved (score: {scores.overall:.2f})")
                
                return AgentResult(
                    success=True,
                    data={
                        "approved": True,
                        "needs_revision": False,
                        "scores": scores.to_dict(),
                        "feedback": "Content meets quality standards",
                        "iteration": iteration
                    },
                    metadata={
                        "quality_threshold": self.quality_threshold,
                        "overall_score": scores.overall
                    }
                )
            
        except Exception as e:
            logger.error(f"ReviewerAgent: Review failed: {str(e)}")
            return AgentResult(
                success=False,
                error=str(e)
            )
    
    async def _evaluate_content(
        self,
        content: str,
        topic: str,
        research_brief: str
    ) -> ReviewScore:
        """Evaluate content across all dimensions"""
        
        # Evaluate clarity
        clarity_score = await self._evaluate_clarity(content)
        
        # Evaluate accuracy
        accuracy_score = await self._evaluate_accuracy(content, research_brief)
        
        # Evaluate engagement
        engagement_score = await self._evaluate_engagement(content)
        
        # Evaluate SEO quality
        seo_score = await self._evaluate_seo(content, topic)
        
        return ReviewScore(
            clarity=clarity_score,
            accuracy=accuracy_score,
            engagement=engagement_score,
            seo_quality=seo_score
        )
    
    async def _evaluate_clarity(self, content: str) -> float:
        """Evaluate content clarity (1-10)"""
        prompt = f"""Evaluate the following content for CLARITY on a scale of 1-10.

Content:
{content[:2000]}  # Limit for token efficiency

Consider:
- Is the writing clear and easy to understand?
- Are ideas presented in a logical order?
- Are transitions smooth between sections?
- Is technical language explained appropriately?

Respond with ONLY a JSON object:
{{
  "score": <1-10>,
  "reasoning": "<brief explanation>"
}}"""
        
        try:
            response = self.granite.generate(
                prompt=prompt,
                system_prompt=self.system_prompt,
                max_tokens=200,
                temperature=0.3
            )
            
            result = json.loads(response.strip())
            return float(result.get("score", 5.0))
            
        except Exception as e:
            logger.warning(f"Clarity evaluation failed: {str(e)}, using default score")
            return 5.0
    
    async def _evaluate_accuracy(self, content: str, research_brief: str) -> float:
        """Evaluate content accuracy (1-10)"""
        prompt = f"""Evaluate the following content for ACCURACY on a scale of 1-10.

Content:
{content[:2000]}

Research Context:
{research_brief[:1000] if research_brief else "No research context provided"}

Consider:
- Are factual claims supported?
- Are there any logical inconsistencies?
- Does it align with the research context?

Respond with ONLY a JSON object:
{{
  "score": <1-10>,
  "reasoning": "<brief explanation>"
}}"""
        
        try:
            response = self.granite.generate(
                prompt=prompt,
                system_prompt=self.system_prompt,
                max_tokens=200,
                temperature=0.3
            )
            
            result = json.loads(response.strip())
            return float(result.get("score", 5.0))
            
        except Exception as e:
            logger.warning(f"Accuracy evaluation failed: {str(e)}, using default score")
            return 5.0
    
    async def _evaluate_engagement(self, content: str) -> float:
        """Evaluate content engagement (1-10)"""
        prompt = f"""Evaluate the following content for ENGAGEMENT on a scale of 1-10.

Content:
{content[:2000]}

Consider:
- Does the introduction hook the reader?
- Is the content interesting and valuable?
- Are there compelling examples or stories?
- Is there a clear call-to-action?

Respond with ONLY a JSON object:
{{
  "score": <1-10>,
  "reasoning": "<brief explanation>"
}}"""
        
        try:
            response = self.granite.generate(
                prompt=prompt,
                system_prompt=self.system_prompt,
                max_tokens=200,
                temperature=0.3
            )
            
            result = json.loads(response.strip())
            return float(result.get("score", 5.0))
            
        except Exception as e:
            logger.warning(f"Engagement evaluation failed: {str(e)}, using default score")
            return 5.0
    
    async def _evaluate_seo(self, content: str, topic: str) -> float:
        """Evaluate SEO quality (1-10)"""
        prompt = f"""Evaluate the following content for SEO QUALITY on a scale of 1-10.

Topic: {topic}

Content:
{content[:2000]}

Consider:
- Are keywords naturally integrated?
- Is the heading structure SEO-friendly?
- Is the content comprehensive enough?
- Is there good use of subheadings?

Respond with ONLY a JSON object:
{{
  "score": <1-10>,
  "reasoning": "<brief explanation>"
}}"""
        
        try:
            response = self.granite.generate(
                prompt=prompt,
                system_prompt=self.system_prompt,
                max_tokens=200,
                temperature=0.3
            )
            
            result = json.loads(response.strip())
            return float(result.get("score", 5.0))
            
        except Exception as e:
            logger.warning(f"SEO evaluation failed: {str(e)}, using default score")
            return 5.0
    
    async def _generate_feedback(
        self,
        content: str,
        topic: str,
        scores: ReviewScore,
        research_brief: str
    ) -> str:
        """Generate actionable improvement feedback"""
        
        failing_dims = scores.get_failing_dimensions(self.quality_threshold)
        
        prompt = f"""The following content needs improvement in these areas: {', '.join(failing_dims)}

Topic: {topic}

Current Scores:
- Clarity: {scores.clarity}/10
- Accuracy: {scores.accuracy}/10
- Engagement: {scores.engagement}/10
- SEO Quality: {scores.seo_quality}/10

Content:
{content[:1500]}

Research Context:
{research_brief[:800] if research_brief else "No research context"}

Generate specific, actionable feedback for improving the content. Focus on the failing dimensions.
Be concise but specific. Provide 3-5 concrete suggestions."""
        
        feedback = self.granite.generate(
            prompt=prompt,
            system_prompt=self.system_prompt,
            max_tokens=400,
            temperature=0.5
        )
        
        return feedback
```

---

## Part 2: Self-Correction Loop Implementation (45 minutes)

### Step 2.1: Create Loop-Aware Pipeline

**File: `services/orchestration_service/pipeline_manager.py`**

Add self-correction loop support:

```python
class SelfCorrectingPipeline(Pipeline):
    """Pipeline with self-correction loop capability"""
    
    def __init__(self, pipeline_id=None, name="Self-Correcting Pipeline", max_iterations=3):
        super().__init__(pipeline_id, name)
        self.max_iterations = max_iterations
        self.iteration_history = []
    
    async def execute_with_loop(
        self,
        initial_input: Dict[str, Any],
        writer_step_index: int,
        reviewer_step_index: int
    ) -> Dict[str, Any]:
        """
        Execute pipeline with self-correction loop
        
        Args:
            initial_input: Initial input data
            writer_step_index: Index of writer agent step
            reviewer_step_index: Index of reviewer agent step
            
        Returns:
            Pipeline execution result
        """
        self.state = "running"
        self.start_time = datetime.utcnow()
        self.context = {"initial_input": initial_input}
        
        iteration = 0
        
        try:
            # Execute steps before writer
            for i in range(writer_step_index):
                await self._execute_step(i, initial_input if i == 0 else None)
            
            # Self-correction loop
            while iteration < self.max_iterations:
                logger.info(f"Pipeline {self.name}: Starting iteration {iteration + 1}/{self.max_iterations}")
                
                # Execute writer
                writer_input = self._prepare_writer_input(
                    writer_step_index, iteration
                )
                await self._execute_step(writer_step_index, writer_input)
                
                # Execute reviewer
                reviewer_input = self._prepare_reviewer_input(
                    writer_step_index, reviewer_step_index, iteration
                )
                await self._execute_step(reviewer_step_index, reviewer_input)
                
                # Check review result
                reviewer_result = self.steps[reviewer_step_index].result
                
                if reviewer_result and reviewer_result.success:
                    review_data = reviewer_result.data
                    
                    # Record iteration
                    self.iteration_history.append({
                        "iteration": iteration + 1,
                        "scores": review_data.get("scores", {}),
                        "approved": review_data.get("approved", False)
                    })
                    
                    if review_data.get("approved", False):
                        logger.info(f"Pipeline {self.name}: Content approved on iteration {iteration + 1}")
                        break
                    else:
                        logger.info(f"Pipeline {self.name}: Revision needed, continuing loop")
                        iteration += 1
                else:
                    logger.error(f"Pipeline {self.name}: Reviewer failed")
                    break
            
            # Execute remaining steps (publisher, etc.)
            for i in range(reviewer_step_index + 1, len(self.steps)):
                await self._execute_step(i, None)
            
            self.state = "completed"
            logger.info(f"Pipeline {self.name}: Completed after {iteration + 1} iterations")
            
        except Exception as e:
            logger.error(f"Pipeline {self.name}: Failed: {str(e)}")
            self.state = "failed"
            self.context["error"] = str(e)
        
        finally:
            self.end_time = datetime.utcnow()
            duration = (self.end_time - self.start_time).total_seconds()
            self.context["duration_seconds"] = duration
            self.context["total_iterations"] = iteration + 1
            self.context["iteration_history"] = self.iteration_history
        
        return self.get_status()
    
    async def _execute_step(self, step_index: int, input_data: Optional[Dict[str, Any]]):
        """Execute a single pipeline step"""
        step = self.steps[step_index]
        
        # Create agent
        agent = agent_registry.create_agent(step.agent_name)
        step.agent_id = agent.agent_id
        
        # Prepare input
        if input_data is None:
            if step_index == 0:
                input_data = self.context["initial_input"]
            else:
                prev_result = self.steps[step_index - 1].result
                input_data = prev_result.data if prev_result and prev_result.success else {}
        
        # Execute
        result = await agent.run(input_data)
        step.result = result
        
        # Store in context
        self.context[f"step_{step_index}_{step.agent_name}"] = result.to_dict()
    
    def _prepare_writer_input(self, writer_index: int, iteration: int) -> Dict[str, Any]:
        """Prepare input for writer agent"""
        if iteration == 0:
            # First iteration: use research brief
            research_result = self.steps[writer_index - 1].result
            return research_result.data if research_result else {}
        else:
            # Subsequent iterations: include feedback
            reviewer_result = self.steps[writer_index + 1].result
            research_result = self.steps[writer_index - 1].result
            
            writer_input = research_result.data.copy() if research_result else {}
            
            if reviewer_result and reviewer_result.data:
                writer_input["feedback"] = reviewer_result.data.get("feedback", "")
                writer_input["previous_scores"] = reviewer_result.data.get("scores", {})
                writer_input["iteration"] = iteration
            
            return writer_input
    
    def _prepare_reviewer_input(
        self,
        writer_index: int,
        reviewer_index: int,
        iteration: int
    ) -> Dict[str, Any]:
        """Prepare input for reviewer agent"""
        writer_result = self.steps[writer_index].result
        research_result = self.steps[writer_index - 1].result
        
        reviewer_input = {}
        
        if writer_result and writer_result.data:
            reviewer_input["content"] = writer_result.data.get("content", "")
        
        if research_result and research_result.data:
            reviewer_input["topic"] = research_result.data.get("topic", "")
            reviewer_input["research_brief"] = research_result.data.get("research_brief", "")
        
        reviewer_input["iteration"] = iteration
        
        return reviewer_input
```

### Step 2.2: Update Writer Agent for Feedback

**File: `services/orchestration_service/agents/writer_agent.py`**

Update to handle feedback:

```python
async def execute(self, input_data: Dict[str, Any]) -> AgentResult:
    """Generate blog content with optional feedback incorporation"""
    try:
        prompt = input_data.get("prompt", "") or input_data.get("topic", "")
        research_brief = input_data.get("research_brief", "")
        tone = input_data.get("tone", "professional")
        feedback = input_data.get("feedback", "")
        previous_scores = input_data.get("previous_scores", {})
        iteration = input_data.get("iteration", 0)
        
        if not prompt:
            return AgentResult(success=False, error="No prompt provided")
        
        # Construct prompt based on iteration
        if iteration == 0:
            # First iteration: normal generation
            full_prompt = f"Topic: {prompt}\n\n"
            if research_brief:
                full_prompt += f"Research Context:\n{research_brief}\n\n"
            full_prompt += f"Tone: {tone}\n\n"
            full_prompt += "Write a complete blog post with title, introduction, body, and conclusion."
            
            logger.info(f"WriterAgent: Generating content (iteration {iteration})")
        else:
            # Revision iteration: incorporate feedback
            full_prompt = f"Topic: {prompt}\n\n"
            full_prompt += f"Previous Quality Scores:\n"
            for dim, score in previous_scores.items():
                full_prompt += f"- {dim}: {score}/10\n"
            full_prompt += f"\nImprovement Feedback:\n{feedback}\n\n"
            if research_brief:
                full_prompt += f"Research Context:\n{research_brief}\n\n"
            full_prompt += f"Tone: {tone}\n\n"
            full_prompt += "Revise and improve the blog post based on the feedback. Address the specific issues mentioned."
            
            logger.info(f"WriterAgent: Revising content (iteration {iteration})")
        
        # Generate content
        content = self.granite.generate(
            prompt=full_prompt,
            system_prompt=self.system_prompt,
            max_tokens=2048,
            temperature=0.7
        )
        
        logger.info(f"WriterAgent: Generated {len(content)} characters")
        
        return AgentResult(
            success=True,
            data={
                "content": content,
                "word_count": len(content.split()),
                "char_count": len(content),
                "model": "ibm/granite-3-8b-instruct",
                "iteration": iteration
            },
            metadata={
                "prompt": prompt,
                "tone": tone,
                "has_feedback": bool(feedback)
            }
        )
        
    except Exception as e:
        logger.error(f"WriterAgent: Failed: {str(e)}")
        return AgentResult(success=False, error=str(e))
```

---

## Part 3: Self-Correcting Blog Generation (30 minutes)

### Step 3.1: Register Reviewer Agent

**File: `services/orchestration_service/agents/__init__.py`**

```python
from .writer_agent import WriterAgent
from .publisher_agent import PublisherAgent
from .research_agent import ResearchAgent
from .reviewer_agent import ReviewerAgent

__all__ = ['WriterAgent', 'PublisherAgent', 'ResearchAgent', 'ReviewerAgent']
```

### Step 3.2: Update Orchestration Service

**File: `services/orchestration_service/main.py`**

```python
# Update imports
from .agents import WriterAgent, PublisherAgent, ResearchAgent, ReviewerAgent
from .pipeline_manager import pipeline_manager, SelfCorrectingPipeline

# Update startup
@app.on_event("startup")
async def startup_event():
    """Register agents on startup"""
    logger.info("Registering agents...")
    agent_registry.register_agent_class("research", ResearchAgent)
    agent_registry.register_agent_class("writer", WriterAgent)
    agent_registry.register_agent_class("reviewer", ReviewerAgent)
    agent_registry.register_agent_class("publisher", PublisherAgent)
    logger.info("Agents registered successfully")


class SelfCorrectingBlogRequest(BaseModel):
    topic: str
    focus_areas: Optional[List[str]] = []
    tone: Optional[str] = "professional"
    blog_id: Optional[str] = None
    max_iterations: Optional[int] = 3
    quality_threshold: Optional[float] = 7.0


@app.post("/blog/generate-self-correcting")
async def generate_self_correcting_blog(request: SelfCorrectingBlogRequest):
    """
    Generate blog with self-correction loop
    
    Pipeline: Research → Writer ⟲ Reviewer → Publisher
    
    The Writer and Reviewer agents form a self-correction loop that
    automatically improves content quality until it meets the threshold
    or reaches max iterations.
    """
    try:
        # Create self-correcting pipeline
        pipeline = SelfCorrectingPipeline(
            name="Self-Correcting Blog Pipeline",
            max_iterations=request.max_iterations
        )
        
        # Add steps
        pipeline.add_step("research")      # Step 0
        pipeline.add_step("writer")        # Step 1 (loop start)
        pipeline.add_step("reviewer")      # Step 2 (loop decision)
        pipeline.add_step("publisher")     # Step 3
        
        # Prepare input
        input_data = {
            "topic": request.topic,
            "focus_areas": request.focus_areas,
            "tone": request.tone,
            "blog_id": request.blog_id,
            "max_sources": 10,
            "quality_threshold": request.quality_threshold
        }
        
        logger.info(f"Starting self-correcting blog generation: {request.topic}")
        
        # Execute with loop
        result = await pipeline.execute_with_loop(
            initial_input=input_data,
            writer_step_index=1,
            reviewer_step_index=2
        )
        
        return {
            "success": True,
            "message": "Self-correcting blog generated successfully",
            "data": result
        }
        
    except Exception as e:
        logger.error(f"Self-correcting blog generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
```

---

## Part 4: Testing Self-Correction Loop (15 minutes)

### Step 4.1: Test Self-Correcting Generation

```bash
# Test self-correcting blog generation
curl -X POST http://localhost:8004/blog/generate-self-correcting \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "The Impact of AI on Software Development",
    "focus_areas": ["productivity", "code quality", "automation"],
    "tone": "professional",
    "max_iterations": 3,
    "quality_threshold": 7.0
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Self-correcting blog generated successfully",
  "data": {
    "pipeline_id": "...",
    "state": "completed",
    "total_iterations": 2,
    "iteration_history": [
      {
        "iteration": 1,
        "scores": {
          "clarity": 6.5,
          "accuracy": 7.2,
          "engagement": 6.8,
          "seo_quality": 6.3,
          "overall": 6.7
        },
        "approved": false
      },
      {
        "iteration": 2,
        "scores": {
          "clarity": 7.8,
          "accuracy": 7.5,
          "engagement": 7.3,
          "seo_quality": 7.1,
          "overall": 7.4
        },
        "approved": true
      }
    ],
    "duration_seconds": 45.2
  }
}
```

### Step 4.2: Verify Improvement

```bash
# Check published blog with iteration history
cat data/published_blogs/blog_*.json | jq '.metadata.iteration_history'
```

Should show score improvements across iterations.

---

## Part 5: Monitoring & Metrics (15 minutes)

### Step 5.1: Add Metrics Endpoint

**File: `services/orchestration_service/main.py`**

```python
@app.get("/metrics/self-correction")
async def get_self_correction_metrics():
    """Get metrics about self-correction loop performance"""
    pipelines = pipeline_manager.list_pipelines()
    
    metrics = {
        "total_pipelines": 0,
        "avg_iterations": 0,
        "approval_rate_by_iteration": {},
        "avg_score_improvement": 0
    }
    
    iteration_counts = []
    score_improvements = []
    
    for pipeline_data in pipelines.values():
        if "iteration_history" in pipeline_data:
            history = pipeline_data["iteration_history"]
            metrics["total_pipelines"] += 1
            iteration_counts.append(len(history))
            
            # Track approval by iteration
            for iter_data in history:
                iter_num = iter_data["iteration"]
                if iter_num not in metrics["approval_rate_by_iteration"]:
                    metrics["approval_rate_by_iteration"][iter_num] = {"approved": 0, "total": 0}
                
                metrics["approval_rate_by_iteration"][iter_num]["total"] += 1
                if iter_data.get("approved"):
                    metrics["approval_rate_by_iteration"][iter_num]["approved"] += 1
            
            # Calculate score improvement
            if len(history) > 1:
                first_score = history[0]["scores"]["overall"]
                last_score = history[-1]["scores"]["overall"]
                improvement = last_score - first_score
                score_improvements.append(improvement)
    
    if iteration_counts:
        metrics["avg_iterations"] = sum(iteration_counts) / len(iteration_counts)
    
    if score_improvements:
        metrics["avg_score_improvement"] = sum(score_improvements) / len(score_improvements)
    
    return {
        "success": True,
        "data": metrics
    }
```

---

## Success Criteria

### ✅ Module Complete When:
1. Reviewer Agent evaluates all 4 dimensions
2. Self-correction loop executes automatically
3. Content improves across iterations
4. Loop terminates when quality threshold met
5. Maximum iterations respected
6. Iteration history tracked
7. Metrics show improvement

### 📊 Quality Metrics:
- **Approval rate**: >80% within 3 iterations
- **Score improvement**: Average +1.0 per iteration
- **First-pass approval**: ~20-30%
- **Second-pass approval**: ~60-70%
- **Third-pass approval**: ~90%+

---

## Troubleshooting

### Issue: "Loop never approves content"
**Solution:**
- Lower quality_threshold (try 6.5 instead of 7.0)
- Check Granite scoring consistency
- Verify feedback is actionable

### Issue: "No improvement across iterations"
**Solution:**
- Verify Writer Agent receives feedback
- Check feedback quality and specificity
- Increase Writer Agent temperature for more variation

### Issue: "Loop takes too long"
**Solution:**
- Reduce max_iterations to 2
- Optimize Granite token usage
- Enable result caching

---

## Next Steps

After completing this module:
- **Enhancement 1-E**: Real-time Agent Dashboard with SSE

The self-correction loop is the **key differentiator** that demonstrates true agentic behavior and autonomous quality improvement.