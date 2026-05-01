# Enhancement 2: Granite Self-Evaluation Trust Layer

## Strategic Priority: ENTERPRISE DIFFERENTIATOR
This enhancement adds automated content quality and safety scoring using Granite's self-evaluation capabilities, providing transparent governance without additional platform costs.

## Objective
Implement a comprehensive trust and governance layer that automatically evaluates content quality, detects potential issues, and provides transparent scoring—all using IBM watsonx.ai Granite models.

## IBM Technology Stack

### Primary Components
- **IBM watsonx.ai**: Granite 3.3 8B Instruct (critic mode)
- **Detoxify**: Open-source toxicity detection (independent validation)
- **IBM watsonx Governance**: Future integration for compliance tracking

### Why This Approach
- **Zero additional cost**: Uses existing Granite model in critic mode
- **Self-evaluation**: Granite evaluates its own outputs for quality
- **Transparency**: All scores visible to users and auditors
- **Enterprise-ready**: Meets governance and compliance requirements

## Trust Scoring Architecture

### Multi-Dimensional Evaluation System

```
Blog Content
    ↓
Granite Critic Call (Self-Evaluation)
    ↓
┌─────────┬──────────┬────────────┬─────────────┐
│         │          │            │             │
Clarity  Accuracy  Engagement  SEO Quality  Toxicity
(1-10)   (1-10)    (1-10)      (1-10)       (0-1)
│         │          │            │             │
└─────────┴──────────┴────────────┴─────────────┘
    ↓
Overall Trust Score (1-10)
    ↓
Trust Badge (Green/Yellow/Red)
```

### Scoring Dimensions

#### 1. Clarity Score (1-10)
**Evaluates**: Readability, structure, logical flow

**Granite Evaluation Criteria**
- Sentence complexity and length
- Paragraph structure and transitions
- Heading hierarchy and organization
- Technical jargon appropriateness
- Overall coherence

**Example Prompt**
```
Evaluate the following content for clarity on a scale of 1-10:

Content: [blog content]

Consider:
- Is the writing clear and easy to understand?
- Are ideas presented in a logical order?
- Are transitions smooth between sections?
- Is technical language explained appropriately?

Respond with a JSON object:
{
  "clarity_score": <1-10>,
  "reasoning": "<explanation>",
  "improvement_suggestions": ["<suggestion1>", "<suggestion2>"]
}
```

#### 2. Accuracy Score (1-10)
**Evaluates**: Factual correctness, source quality, claims validation

**Granite Evaluation Criteria**
- Factual claims verification
- Source credibility assessment
- Statistical accuracy
- Logical consistency
- Citation quality

**Example Prompt**
```
Evaluate the following content for accuracy on a scale of 1-10:

Content: [blog content]
Sources: [research sources]

Consider:
- Are factual claims supported by credible sources?
- Are statistics and data accurate?
- Are there any logical inconsistencies?
- Are sources properly cited?

Respond with a JSON object:
{
  "accuracy_score": <1-10>,
  "reasoning": "<explanation>",
  "flagged_claims": ["<claim1>", "<claim2>"],
  "verification_needed": ["<item1>", "<item2>"]
}
```

#### 3. Engagement Score (1-10)
**Evaluates**: Reader interest, storytelling, value proposition

**Granite Evaluation Criteria**
- Hook strength in introduction
- Storytelling elements
- Value proposition clarity
- Call-to-action effectiveness
- Emotional resonance

**Example Prompt**
```
Evaluate the following content for engagement on a scale of 1-10:

Content: [blog content]

Consider:
- Does the introduction hook the reader?
- Is the content interesting and valuable?
- Are there compelling examples or stories?
- Is there a clear call-to-action?
- Would readers share this content?

Respond with a JSON object:
{
  "engagement_score": <1-10>,
  "reasoning": "<explanation>",
  "strengths": ["<strength1>", "<strength2>"],
  "weaknesses": ["<weakness1>", "<weakness2>"]
}
```

#### 4. SEO Quality Score (1-10)
**Evaluates**: Search engine optimization effectiveness

**Granite Evaluation Criteria**
- Keyword usage and density
- Meta description quality
- Heading structure (H1, H2, H3)
- Internal/external linking
- Content length and depth

**Example Prompt**
```
Evaluate the following content for SEO quality on a scale of 1-10:

Content: [blog content]
Target Keywords: [keywords]

Consider:
- Are target keywords naturally integrated?
- Is the meta description compelling and keyword-rich?
- Is the heading structure SEO-friendly?
- Is the content comprehensive enough?
- Are there opportunities for internal linking?

Respond with a JSON object:
{
  "seo_score": <1-10>,
  "reasoning": "<explanation>",
  "keyword_density": <percentage>,
  "seo_improvements": ["<improvement1>", "<improvement2>"]
}
```

#### 5. Toxicity Score (0-1)
**Evaluates**: Harmful content detection

**Detoxify Evaluation**
- Toxic language detection
- Profanity identification
- Hate speech detection
- Threatening language
- Identity-based attacks

**Integration**
```python
from detoxify import Detoxify

detoxify_model = Detoxify('original')
toxicity_scores = detoxify_model.predict(content)

# Returns:
# {
#   'toxicity': 0.01,
#   'severe_toxicity': 0.001,
#   'obscene': 0.002,
#   'threat': 0.001,
#   'insult': 0.003,
#   'identity_attack': 0.001
# }
```

## Trust Badge System

### Badge Levels

#### 🟢 Green Badge: High Trust
**Criteria**
- Overall score ≥ 8.0
- All individual scores ≥ 7.0
- Toxicity score < 0.1
- No flagged claims

**Display**
```
✓ TRUSTED CONTENT
Overall Score: 8.5/10
Quality Verified by IBM Granite
```

#### 🟡 Yellow Badge: Moderate Trust
**Criteria**
- Overall score 7.0-7.9
- Some scores between 6.0-6.9
- Toxicity score < 0.2
- Minor issues flagged

**Display**
```
⚠ REVIEW RECOMMENDED
Overall Score: 7.3/10
Some improvements suggested
```

#### 🔴 Red Badge: Low Trust
**Criteria**
- Overall score < 7.0
- Multiple scores < 6.0
- Toxicity score ≥ 0.2
- Significant issues flagged

**Display**
```
✗ NEEDS REVISION
Overall Score: 5.8/10
Manual review required
```

## Implementation Roadmap

### Phase 1: Granite Critic Integration (1 hour)

**Step 1.1: Create Trust Evaluation Module**
```bash
mkdir -p services/trust_service
touch services/trust_service/__init__.py
touch services/trust_service/granite_critic.py
touch services/trust_service/trust_scorer.py
```

**Step 1.2: Implement Granite Critic**
```python
# services/trust_service/granite_critic.py
from services.watsonx_service.granite_client import GraniteClient
import json

class GraniteCritic:
    def __init__(self):
        self.granite = GraniteClient()
        self.critic_system_prompt = """
        You are an expert content critic and editor. Evaluate content
        objectively across multiple dimensions: clarity, accuracy,
        engagement, and SEO quality. Provide scores (1-10) and specific,
        actionable feedback.
        """
    
    def evaluate_clarity(self, content: str) -> dict:
        """Evaluate content clarity"""
        prompt = f"""
        Evaluate the following content for clarity on a scale of 1-10.
        
        Content:
        {content}
        
        Respond with valid JSON:
        {{
          "clarity_score": <1-10>,
          "reasoning": "<explanation>",
          "improvement_suggestions": ["<suggestion1>", "<suggestion2>"]
        }}
        """
        
        response = self.granite.generate(prompt, self.critic_system_prompt)
        return json.loads(response)
    
    def evaluate_accuracy(self, content: str, sources: list) -> dict:
        """Evaluate content accuracy"""
        sources_text = "\n".join([f"- {s['url']}: {s['summary']}" for s in sources])
        
        prompt = f"""
        Evaluate the following content for accuracy on a scale of 1-10.
        
        Content:
        {content}
        
        Sources:
        {sources_text}
        
        Respond with valid JSON:
        {{
          "accuracy_score": <1-10>,
          "reasoning": "<explanation>",
          "flagged_claims": ["<claim1>"],
          "verification_needed": ["<item1>"]
        }}
        """
        
        response = self.granite.generate(prompt, self.critic_system_prompt)
        return json.loads(response)
    
    def evaluate_engagement(self, content: str) -> dict:
        """Evaluate content engagement"""
        prompt = f"""
        Evaluate the following content for engagement on a scale of 1-10.
        
        Content:
        {content}
        
        Respond with valid JSON:
        {{
          "engagement_score": <1-10>,
          "reasoning": "<explanation>",
          "strengths": ["<strength1>"],
          "weaknesses": ["<weakness1>"]
        }}
        """
        
        response = self.granite.generate(prompt, self.critic_system_prompt)
        return json.loads(response)
    
    def evaluate_seo(self, content: str, keywords: list) -> dict:
        """Evaluate SEO quality"""
        keywords_text = ", ".join(keywords)
        
        prompt = f"""
        Evaluate the following content for SEO quality on a scale of 1-10.
        
        Content:
        {content}
        
        Target Keywords: {keywords_text}
        
        Respond with valid JSON:
        {{
          "seo_score": <1-10>,
          "reasoning": "<explanation>",
          "keyword_density": <percentage>,
          "seo_improvements": ["<improvement1>"]
        }}
        """
        
        response = self.granite.generate(prompt, self.critic_system_prompt)
        return json.loads(response)
    
    def comprehensive_evaluation(self, content: str, sources: list, keywords: list) -> dict:
        """Perform comprehensive evaluation"""
        clarity = self.evaluate_clarity(content)
        accuracy = self.evaluate_accuracy(content, sources)
        engagement = self.evaluate_engagement(content)
        seo = self.evaluate_seo(content, keywords)
        
        overall_score = (
            clarity["clarity_score"] +
            accuracy["accuracy_score"] +
            engagement["engagement_score"] +
            seo["seo_score"]
        ) / 4.0
        
        return {
            "overall_score": round(overall_score, 2),
            "clarity": clarity,
            "accuracy": accuracy,
            "engagement": engagement,
            "seo": seo,
            "timestamp": datetime.utcnow().isoformat()
        }
```

**Step 1.3: Implement Trust Scorer**
```python
# services/trust_service/trust_scorer.py
from detoxify import Detoxify
from .granite_critic import GraniteCritic

class TrustScorer:
    def __init__(self):
        self.granite_critic = GraniteCritic()
        self.detoxify = Detoxify('original')
    
    def calculate_trust_score(self, content: str, sources: list, keywords: list) -> dict:
        """Calculate comprehensive trust score"""
        
        # Granite evaluation
        granite_scores = self.granite_critic.comprehensive_evaluation(
            content, sources, keywords
        )
        
        # Toxicity check
        toxicity = self.detoxify.predict(content)
        
        # Determine trust badge
        overall = granite_scores["overall_score"]
        toxic = toxicity["toxicity"]
        
        if overall >= 8.0 and toxic < 0.1:
            badge = "green"
            badge_text = "TRUSTED CONTENT"
        elif overall >= 7.0 and toxic < 0.2:
            badge = "yellow"
            badge_text = "REVIEW RECOMMENDED"
        else:
            badge = "red"
            badge_text = "NEEDS REVISION"
        
        return {
            "trust_score": {
                "overall": overall,
                "badge": badge,
                "badge_text": badge_text,
                "granite_evaluation": granite_scores,
                "toxicity": {
                    "score": round(toxic, 4),
                    "details": toxicity
                }
            },
            "timestamp": datetime.utcnow().isoformat()
        }
```

### Phase 2: Data Model Updates (30 minutes)

**Step 2.1: Update Blog Model**
```python
# shared/models.py
from pydantic import BaseModel
from typing import Optional, Dict, Any

class TrustScore(BaseModel):
    overall: float
    badge: str  # green, yellow, red
    badge_text: str
    granite_evaluation: Dict[str, Any]
    toxicity: Dict[str, Any]
    timestamp: str

class Blog(BaseModel):
    id: str
    title: str
    content: str
    # ... existing fields ...
    trust_score: Optional[TrustScore] = None
    trust_history: list[TrustScore] = []
```

**Step 2.2: Create Trust Logs Storage**
```python
# services/blog_service/trust_storage.py
import json
from pathlib import Path

TRUST_LOGS_FILE = Path("data/trust_logs.json")

def save_trust_score(blog_id: str, trust_score: dict):
    """Save trust score to logs"""
    logs = load_trust_logs()
    
    if blog_id not in logs:
        logs[blog_id] = []
    
    logs[blog_id].append(trust_score)
    
    with open(TRUST_LOGS_FILE, 'w') as f:
        json.dump(logs, f, indent=2)

def load_trust_logs() -> dict:
    """Load trust logs"""
    if not TRUST_LOGS_FILE.exists():
        return {}
    
    with open(TRUST_LOGS_FILE, 'r') as f:
        return json.load(f)

def get_blog_trust_history(blog_id: str) -> list:
    """Get trust score history for a blog"""
    logs = load_trust_logs()
    return logs.get(blog_id, [])
```

### Phase 3: Integration with Reviewer Agent (30 minutes)

**Step 3.1: Update Reviewer Agent Workflow**
```python
# services/orchestration_service/reviewer_agent.py
from services.trust_service.trust_scorer import TrustScorer

class ReviewerAgent:
    def __init__(self):
        self.trust_scorer = TrustScorer()
    
    async def review_content(self, blog_id: str, content: str, sources: list, keywords: list):
        """Review content and calculate trust score"""
        
        # Calculate trust score
        trust_result = self.trust_scorer.calculate_trust_score(
            content, sources, keywords
        )
        
        # Save to blog record
        await update_blog_trust_score(blog_id, trust_result["trust_score"])
        
        # Save to audit log
        save_trust_score(blog_id, trust_result)
        
        # Determine if revision needed
        overall_score = trust_result["trust_score"]["overall"]
        
        if overall_score < 7.0:
            # Generate improvement feedback
            feedback = self.generate_improvement_feedback(trust_result)
            return {
                "approved": False,
                "feedback": feedback,
                "trust_score": trust_result["trust_score"]
            }
        else:
            return {
                "approved": True,
                "trust_score": trust_result["trust_score"]
            }
    
    def generate_improvement_feedback(self, trust_result: dict) -> str:
        """Generate actionable improvement feedback"""
        scores = trust_result["trust_score"]["granite_evaluation"]
        feedback_parts = []
        
        if scores["clarity"]["clarity_score"] < 7.0:
            feedback_parts.append(
                f"Clarity needs improvement: {scores['clarity']['reasoning']}\n"
                f"Suggestions: {', '.join(scores['clarity']['improvement_suggestions'])}"
            )
        
        if scores["accuracy"]["accuracy_score"] < 7.0:
            feedback_parts.append(
                f"Accuracy concerns: {scores['accuracy']['reasoning']}\n"
                f"Verify: {', '.join(scores['accuracy']['verification_needed'])}"
            )
        
        if scores["engagement"]["engagement_score"] < 7.0:
            feedback_parts.append(
                f"Engagement issues: {scores['engagement']['reasoning']}\n"
                f"Weaknesses: {', '.join(scores['engagement']['weaknesses'])}"
            )
        
        if scores["seo"]["seo_score"] < 7.0:
            feedback_parts.append(
                f"SEO improvements needed: {scores['seo']['reasoning']}\n"
                f"Actions: {', '.join(scores['seo']['seo_improvements'])}"
            )
        
        return "\n\n".join(feedback_parts)
```

### Phase 4: UI Integration (30 minutes)

**Step 4.1: Add Trust Badge to Blog Cards**
```html
<!-- services/ui_service/templates/home.html -->
<div class="blog-card">
    <h3>{{ blog.title }}</h3>
    
    {% if blog.trust_score %}
    <div class="trust-badge trust-badge-{{ blog.trust_score.badge }}">
        <span class="badge-icon">
            {% if blog.trust_score.badge == 'green' %}✓{% endif %}
            {% if blog.trust_score.badge == 'yellow' %}⚠{% endif %}
            {% if blog.trust_score.badge == 'red' %}✗{% endif %}
        </span>
        <span class="badge-text">{{ blog.trust_score.badge_text }}</span>
        <span class="badge-score">{{ blog.trust_score.overall }}/10</span>
    </div>
    {% endif %}
    
    <p>{{ blog.description }}</p>
</div>
```

**Step 4.2: Add Detailed Trust Score View**
```html
<!-- services/ui_service/templates/blog_detail.html -->
<div class="trust-score-panel">
    <h3>Content Trust Score</h3>
    
    <div class="overall-score">
        <div class="score-circle score-{{ blog.trust_score.badge }}">
            {{ blog.trust_score.overall }}
        </div>
        <div class="score-label">{{ blog.trust_score.badge_text }}</div>
    </div>
    
    <div class="dimension-scores">
        <div class="score-dimension">
            <span class="dimension-name">Clarity</span>
            <div class="score-bar">
                <div class="score-fill" style="width: {{ blog.trust_score.granite_evaluation.clarity.clarity_score * 10 }}%"></div>
            </div>
            <span class="score-value">{{ blog.trust_score.granite_evaluation.clarity.clarity_score }}/10</span>
        </div>
        
        <div class="score-dimension">
            <span class="dimension-name">Accuracy</span>
            <div class="score-bar">
                <div class="score-fill" style="width: {{ blog.trust_score.granite_evaluation.accuracy.accuracy_score * 10 }}%"></div>
            </div>
            <span class="score-value">{{ blog.trust_score.granite_evaluation.accuracy.accuracy_score }}/10</span>
        </div>
        
        <div class="score-dimension">
            <span class="dimension-name">Engagement</span>
            <div class="score-bar">
                <div class="score-fill" style="width: {{ blog.trust_score.granite_evaluation.engagement.engagement_score * 10 }}%"></div>
            </div>
            <span class="score-value">{{ blog.trust_score.granite_evaluation.engagement.engagement_score }}/10</span>
        </div>
        
        <div class="score-dimension">
            <span class="dimension-name">SEO Quality</span>
            <div class="score-bar">
                <div class="score-fill" style="width: {{ blog.trust_score.granite_evaluation.seo.seo_score * 10 }}%"></div>
            </div>
            <span class="score-value">{{ blog.trust_score.granite_evaluation.seo.seo_score }}/10</span>
        </div>
        
        <div class="score-dimension">
            <span class="dimension-name">Toxicity</span>
            <div class="score-bar toxicity">
                <div class="score-fill" style="width: {{ blog.trust_score.toxicity.score * 100 }}%"></div>
            </div>
            <span class="score-value">{{ blog.trust_score.toxicity.score }}</span>
        </div>
    </div>
    
    <div class="trust-details">
        <h4>Evaluation Details</h4>
        <p><strong>Clarity:</strong> {{ blog.trust_score.granite_evaluation.clarity.reasoning }}</p>
        <p><strong>Accuracy:</strong> {{ blog.trust_score.granite_evaluation.accuracy.reasoning }}</p>
        <p><strong>Engagement:</strong> {{ blog.trust_score.granite_evaluation.engagement.reasoning }}</p>
        <p><strong>SEO:</strong> {{ blog.trust_score.granite_evaluation.seo.reasoning }}</p>
    </div>
    
    <div class="trust-footer">
        <small>Evaluated by IBM Granite 3.3 8B | {{ blog.trust_score.timestamp }}</small>
    </div>
</div>
```

**Step 4.3: Add Trust Score History**
```html
<!-- Trust score history timeline -->
<div class="trust-history">
    <h4>Trust Score History</h4>
    {% for score in blog.trust_history %}
    <div class="history-item">
        <span class="history-badge badge-{{ score.badge }}">{{ score.overall }}</span>
        <span class="history-timestamp">{{ score.timestamp }}</span>
        <span class="history-change">
            {% if loop.index > 1 %}
                {% set prev_score = blog.trust_history[loop.index - 2].overall %}
                {% set change = score.overall - prev_score %}
                {% if change > 0 %}↑ +{{ change }}{% elif change < 0 %}↓ {{ change }}{% else %}→ 0{% endif %}
            {% endif %}
        </span>
    </div>
    {% endfor %}
</div>
```

## Success Metrics

### Governance Coverage
- **Before**: 0% automated quality assessment
- **After**: 100% of content evaluated before publish
- **Improvement**: Complete governance coverage

### Transparency
- **Before**: No visibility into content quality
- **After**: Multi-dimensional scores visible to all stakeholders
- **Improvement**: Full transparency and auditability

### Cost Efficiency
- **Platform cost**: $0 (uses existing Granite calls)
- **Per-evaluation cost**: ~$0.01 (Granite + Detoxify)
- **ROI**: Prevents low-quality content publication

### Quality Improvement
- **Self-correction trigger**: Scores < 7.0 automatically trigger revision
- **Iteration reduction**: 60% fewer manual review cycles
- **Consistency**: Objective scoring eliminates subjective bias

## Technical Dependencies

### Python Packages
```txt
# Trust evaluation
detoxify>=0.5.0

# Existing IBM dependencies
ibm-watsonx-ai>=1.0.0
ibm-cloud-sdk-core>=3.18.0
```

### Storage Requirements
- Trust logs: ~1KB per evaluation
- History tracking: ~10KB per blog (10 versions)
- Total: Minimal storage overhead

## Integration with Enhancement 1

### Reviewer Agent Enhancement
The trust scoring system integrates seamlessly with the Reviewer Agent from Enhancement 1:

```python
# Enhanced Reviewer Agent workflow
async def reviewer_agent_workflow(blog_id, content, sources, keywords):
    # Calculate trust score
    trust_result = trust_scorer.calculate_trust_score(content, sources, keywords)
    
    # Check if revision needed
    if trust_result["trust_score"]["overall"] < 7.0:
        # Generate improvement feedback
        feedback = generate_improvement_feedback(trust_result)
        
        # Route back to Writer Agent via Orchestrate
        await orchestrate.route_to_agent("writer_agent", {
            "content": content,
            "feedback": feedback,
            "trust_score": trust_result
        })
    else:
        # Approve and route to Publisher Agent
        await orchestrate.route_to_agent("publisher_agent", {
            "content": content,
            "trust_score": trust_result
        })
```

