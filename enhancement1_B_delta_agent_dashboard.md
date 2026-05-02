# Enhancement 1-B Delta: Agent Performance Dashboard for Demo

## Overview
This delta enhancement adds a real-time agent performance dashboard to visualize the agentic AI orchestration for demo purposes. This was not included in the original enhancement1_B plan but is essential for demonstrating the multi-agent system in action.

## What This Delivers
- ✅ Real-time agent performance dashboard
- ✅ Live pipeline execution visualization
- ✅ Agent metrics and statistics
- ✅ Step-by-step execution tracking
- ✅ Historical pipeline view
- ✅ Demo-ready UI for showcasing agentic AI

## Implementation Time: 1-2 hours

---

## Current State Analysis

### Available Data from Orchestration Service
The orchestration service already provides:
1. **Pipeline Status** (`GET /pipelines/{pipeline_id}`)
   - Pipeline state (idle, running, completed, failed)
   - Current step number
   - Total steps
   - Start/end times
   - Duration

2. **Pipeline List** (`GET /pipelines`)
   - All pipelines with their status
   - Pipeline names and IDs

3. **Agent Registry** (`GET /agents`)
   - Registered agent classes
   - Active agent instances

4. **Pipeline Execution Results**
   - Step-by-step results
   - Agent outputs
   - Success/failure status

### What's Missing for Demo
1. ❌ UI page to visualize agent performance
2. ❌ Real-time updates during pipeline execution
3. ❌ Visual representation of agent workflow
4. ❌ Metrics aggregation (success rate, avg duration, etc.)
5. ❌ Easy access from main navigation

---

## Part 1: Add Agent Metrics Endpoint (15 minutes)

### Step 1.1: Enhance Pipeline Manager with Metrics

**File: `services/orchestration_service/pipeline_manager.py`**

Add after the `PipelineManager` class definition:

```python
def get_metrics(self) -> Dict[str, Any]:
    """Get aggregated metrics across all pipelines"""
    total_pipelines = len(self.pipelines)
    completed = sum(1 for p in self.pipelines.values() if p.state == "completed")
    failed = sum(1 for p in self.pipelines.values() if p.state == "failed")
    running = sum(1 for p in self.pipelines.values() if p.state == "running")
    
    # Calculate average duration for completed pipelines
    durations = []
    for pipeline in self.pipelines.values():
        if pipeline.state == "completed" and pipeline.start_time and pipeline.end_time:
            duration = (pipeline.end_time - pipeline.start_time).total_seconds()
            durations.append(duration)
    
    avg_duration = sum(durations) / len(durations) if durations else 0
    
    # Agent usage statistics
    agent_usage = {}
    for pipeline in self.pipelines.values():
        for step in pipeline.steps:
            agent_name = step.agent_name
            if agent_name not in agent_usage:
                agent_usage[agent_name] = {"total": 0, "success": 0, "failed": 0}
            
            agent_usage[agent_name]["total"] += 1
            if step.result:
                if step.result.success:
                    agent_usage[agent_name]["success"] += 1
                else:
                    agent_usage[agent_name]["failed"] += 1
    
    return {
        "total_pipelines": total_pipelines,
        "completed": completed,
        "failed": failed,
        "running": running,
        "success_rate": (completed / total_pipelines * 100) if total_pipelines > 0 else 0,
        "avg_duration_seconds": round(avg_duration, 2),
        "agent_usage": agent_usage
    }
```

### Step 1.2: Add Metrics Endpoint

**File: `services/orchestration_service/main.py`**

Add new endpoint:

```python
@app.get("/metrics")
async def get_metrics():
    """Get orchestration metrics"""
    return {
        "success": True,
        "data": pipeline_manager.get_metrics()
    }
```

---

## Part 2: Create Agent Dashboard UI (30 minutes)

### Step 2.1: Create Dashboard Template

**File: `services/ui_service/templates/agent_dashboard.html`**

```html
{% extends "base.html" %}

{% block title %}Agent Performance Dashboard{% endblock %}

{% block content %}
<div style="margin-bottom: 2rem;">
    <h2>🤖 Agent Performance Dashboard</h2>
    <p style="color: #666;">Real-time monitoring of agentic AI orchestration</p>
</div>

<!-- Metrics Overview -->
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem;">
    <div class="card" style="text-align: center; padding: 1.5rem;">
        <div style="font-size: 2rem; font-weight: bold; color: #3498db;" id="total-pipelines">0</div>
        <div style="color: #666; margin-top: 0.5rem;">Total Pipelines</div>
    </div>
    <div class="card" style="text-align: center; padding: 1.5rem;">
        <div style="font-size: 2rem; font-weight: bold; color: #2ecc71;" id="completed-pipelines">0</div>
        <div style="color: #666; margin-top: 0.5rem;">Completed</div>
    </div>
    <div class="card" style="text-align: center; padding: 1.5rem;">
        <div style="font-size: 2rem; font-weight: bold; color: #e74c3c;" id="failed-pipelines">0</div>
        <div style="color: #666; margin-top: 0.5rem;">Failed</div>
    </div>
    <div class="card" style="text-align: center; padding: 1.5rem;">
        <div style="font-size: 2rem; font-weight: bold; color: #f39c12;" id="running-pipelines">0</div>
        <div style="color: #666; margin-top: 0.5rem;">Running</div>
    </div>
    <div class="card" style="text-align: center; padding: 1.5rem;">
        <div style="font-size: 2rem; font-weight: bold; color: #9b59b6;" id="success-rate">0%</div>
        <div style="color: #666; margin-top: 0.5rem;">Success Rate</div>
    </div>
    <div class="card" style="text-align: center; padding: 1.5rem;">
        <div style="font-size: 2rem; font-weight: bold; color: #1abc9c;" id="avg-duration">0s</div>
        <div style="color: #666; margin-top: 0.5rem;">Avg Duration</div>
    </div>
</div>

<!-- Agent Usage Statistics -->
<div class="card" style="margin-bottom: 2rem;">
    <h3 style="margin-bottom: 1rem;">Agent Usage Statistics</h3>
    <div id="agent-stats" style="display: grid; gap: 1rem;">
        <!-- Agent stats will be populated here -->
    </div>
</div>

<!-- Active Pipelines -->
<div class="card" style="margin-bottom: 2rem;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
        <h3>Active Pipelines</h3>
        <button onclick="refreshDashboard()" class="btn" style="font-size: 0.9rem; padding: 0.5rem 1rem;">
            🔄 Refresh
        </button>
    </div>
    <div id="pipelines-list">
        <!-- Pipelines will be populated here -->
    </div>
</div>

<!-- Recent Pipeline Executions -->
<div class="card">
    <h3 style="margin-bottom: 1rem;">Recent Pipeline Executions</h3>
    <div id="recent-pipelines">
        <!-- Recent pipelines will be populated here -->
    </div>
</div>

<script>
// Auto-refresh every 3 seconds
let autoRefreshInterval;

async function fetchMetrics() {
    try {
        const response = await fetch('http://localhost:8004/metrics');
        const data = await response.json();
        return data.data;
    } catch (error) {
        console.error('Error fetching metrics:', error);
        return null;
    }
}

async function fetchPipelines() {
    try {
        const response = await fetch('http://localhost:8004/pipelines');
        const data = await response.json();
        return data.data;
    } catch (error) {
        console.error('Error fetching pipelines:', error);
        return null;
    }
}

async function fetchAgents() {
    try {
        const response = await fetch('http://localhost:8004/agents');
        const data = await response.json();
        return data.data;
    } catch (error) {
        console.error('Error fetching agents:', error);
        return null;
    }
}

function updateMetrics(metrics) {
    if (!metrics) return;
    
    document.getElementById('total-pipelines').textContent = metrics.total_pipelines;
    document.getElementById('completed-pipelines').textContent = metrics.completed;
    document.getElementById('failed-pipelines').textContent = metrics.failed;
    document.getElementById('running-pipelines').textContent = metrics.running;
    document.getElementById('success-rate').textContent = metrics.success_rate.toFixed(1) + '%';
    document.getElementById('avg-duration').textContent = metrics.avg_duration_seconds.toFixed(1) + 's';
    
    // Update agent stats
    const agentStatsDiv = document.getElementById('agent-stats');
    agentStatsDiv.innerHTML = '';
    
    for (const [agentName, stats] of Object.entries(metrics.agent_usage)) {
        const successRate = stats.total > 0 ? (stats.success / stats.total * 100).toFixed(1) : 0;
        const agentCard = `
            <div style="border: 1px solid #ddd; border-radius: 8px; padding: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <strong style="text-transform: capitalize;">${agentName} Agent</strong>
                    <span style="background: #3498db; color: white; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.8rem;">
                        ${successRate}% success
                    </span>
                </div>
                <div style="display: flex; gap: 1rem; font-size: 0.9rem; color: #666;">
                    <span>Total: ${stats.total}</span>
                    <span style="color: #2ecc71;">✓ ${stats.success}</span>
                    <span style="color: #e74c3c;">✗ ${stats.failed}</span>
                </div>
            </div>
        `;
        agentStatsDiv.innerHTML += agentCard;
    }
}

function updatePipelines(pipelines) {
    if (!pipelines) return;
    
    const pipelinesDiv = document.getElementById('pipelines-list');
    const recentDiv = document.getElementById('recent-pipelines');
    
    const pipelineArray = Object.entries(pipelines);
    
    if (pipelineArray.length === 0) {
        pipelinesDiv.innerHTML = '<p style="color: #666; text-align: center; padding: 2rem;">No pipelines yet</p>';
        recentDiv.innerHTML = '<p style="color: #666; text-align: center; padding: 2rem;">No recent executions</p>';
        return;
    }
    
    // Show running pipelines
    const runningPipelines = pipelineArray.filter(([_, p]) => p.state === 'running');
    if (runningPipelines.length > 0) {
        pipelinesDiv.innerHTML = runningPipelines.map(([id, pipeline]) => {
            const progress = pipeline.total_steps > 0 ? 
                ((pipeline.current_step + 1) / pipeline.total_steps * 100).toFixed(0) : 0;
            
            return `
                <div style="border: 1px solid #f39c12; border-radius: 8px; padding: 1rem; margin-bottom: 1rem; background: #fff9e6;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <strong>${pipeline.name}</strong>
                        <span style="background: #f39c12; color: white; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.8rem;">
                            RUNNING
                        </span>
                    </div>
                    <div style="margin-bottom: 0.5rem;">
                        <div style="background: #ecf0f1; height: 8px; border-radius: 4px; overflow: hidden;">
                            <div style="background: #f39c12; height: 100%; width: ${progress}%; transition: width 0.3s;"></div>
                        </div>
                    </div>
                    <div style="font-size: 0.9rem; color: #666;">
                        Step ${pipeline.current_step + 1} of ${pipeline.total_steps} • ${progress}% complete
                    </div>
                </div>
            `;
        }).join('');
    } else {
        pipelinesDiv.innerHTML = '<p style="color: #666; text-align: center; padding: 1rem;">No active pipelines</p>';
    }
    
    // Show recent completed/failed pipelines
    const recentPipelines = pipelineArray
        .filter(([_, p]) => p.state === 'completed' || p.state === 'failed')
        .slice(0, 5);
    
    if (recentPipelines.length > 0) {
        recentDiv.innerHTML = recentPipelines.map(([id, pipeline]) => {
            const stateColor = pipeline.state === 'completed' ? '#2ecc71' : '#e74c3c';
            const stateText = pipeline.state === 'completed' ? 'COMPLETED' : 'FAILED';
            
            return `
                <div style="border: 1px solid ${stateColor}; border-radius: 8px; padding: 1rem; margin-bottom: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <strong>${pipeline.name}</strong>
                        <span style="background: ${stateColor}; color: white; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.8rem;">
                            ${stateText}
                        </span>
                    </div>
                    <div style="font-size: 0.9rem; color: #666;">
                        ${pipeline.total_steps} steps • ${pipeline.duration_seconds ? pipeline.duration_seconds.toFixed(2) + 's' : 'N/A'}
                    </div>
                </div>
            `;
        }).join('');
    } else {
        recentDiv.innerHTML = '<p style="color: #666; text-align: center; padding: 1rem;">No recent executions</p>';
    }
}

async function refreshDashboard() {
    const metrics = await fetchMetrics();
    const pipelines = await fetchPipelines();
    
    updateMetrics(metrics);
    updatePipelines(pipelines);
}

// Initial load
refreshDashboard();

// Auto-refresh every 3 seconds
autoRefreshInterval = setInterval(refreshDashboard, 3000);

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
    }
});
</script>
{% endblock %}
```

### Step 2.2: Add Dashboard Route

**File: `services/ui_service/main.py`**

Add new route after the home route:

```python
@app.get("/agents", response_class=HTMLResponse)
async def agent_dashboard(request: Request):
    """Agent performance dashboard."""
    return templates.TemplateResponse("agent_dashboard.html", {"request": request})
```

### Step 2.3: Update Navigation

**File: `services/ui_service/templates/base.html`**

Update the navigation section to include the dashboard link:

```html
<nav style="display: flex; gap: 2rem; align-items: center;">
    <a href="/" style="color: white; text-decoration: none;">Home</a>
    <a href="/create" style="color: white; text-decoration: none;">Create Blog</a>
    <a href="/agents" style="color: white; text-decoration: none;">🤖 Agent Dashboard</a>
    <a href="/settings" style="color: white; text-decoration: none;">Settings</a>
</nav>
```

---

## Part 3: Enhance Create Page with Orchestration Option (15 minutes)

### Step 3.1: Update Create Template

**File: `services/ui_service/templates/create.html`**

Add orchestration checkbox before the submit button:

```html
<!-- Add this before the submit button -->
<div style="margin-bottom: 1.5rem; padding: 1rem; background: #e8f4f8; border-radius: 8px; border: 1px solid #3498db;">
    <label style="display: flex; align-items: center; cursor: pointer;">
        <input type="checkbox" name="use_orchestration" value="true" style="margin-right: 0.5rem; width: 18px; height: 18px;">
        <div>
            <strong style="color: #2c3e50;">🤖 Use Agentic AI Orchestration</strong>
            <p style="margin: 0.25rem 0 0 0; font-size: 0.9rem; color: #666;">
                Enable multi-agent workflow with Writer → Publisher pipeline
            </p>
        </div>
    </label>
</div>
```

---

## Part 4: Fix API Gateway Integration (15 minutes)

### Step 4.1: Add Orchestration Endpoint to API Gateway

**File: `services/api_gateway/main.py`**

Add new endpoint:

```python
@app.post("/api/blogs/generate-orchestrated")
async def generate_blog_orchestrated(request: dict):
    """Generate blog using orchestration service"""
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"http://localhost:8004/blog/generate",
                json=request
            )
            return response.json()
    except Exception as e:
        logger.error(f"Orchestration request failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
```

---

## Part 5: Testing the Dashboard (10 minutes)

### Step 5.1: Test Workflow

1. **Start all services:**
   ```bash
   python start_all_services.py
   ```

2. **Access the dashboard:**
   - Open browser: http://localhost:8003/agents
   - Verify metrics show 0 initially

3. **Create a blog with orchestration:**
   - Go to: http://localhost:8003/create
   - Fill in blog details
   - Check "Use Agentic AI Orchestration"
   - Submit

4. **Watch the dashboard:**
   - Refresh or wait for auto-refresh
   - See pipeline execution in real-time
   - Verify metrics update
   - Check agent statistics

5. **Create multiple blogs:**
   - Create 2-3 more blogs with orchestration
   - Watch metrics accumulate
   - Verify success rates calculate correctly

### Step 5.2: Demo Script

**For presenting the agentic AI:**

1. **Show the dashboard first** (http://localhost:8003/agents)
   - "This is our agent performance dashboard"
   - "Currently showing 0 pipelines as we haven't run any yet"

2. **Navigate to Create Blog** (http://localhost:8003/create)
   - "Let's create a blog using our multi-agent system"
   - Fill in: Title, Description, Prompt
   - **Check the orchestration checkbox**
   - "Notice the 'Use Agentic AI Orchestration' option"
   - "This enables our Writer → Publisher agent pipeline"

3. **Submit and return to dashboard**
   - "Now let's watch our agents work"
   - Show the running pipeline with progress bar
   - "You can see the Writer agent is processing the content"
   - Wait for completion
   - "Now the Publisher agent takes over"

4. **Show the results**
   - Point out the metrics:
     - Total pipelines: 1
     - Completed: 1
     - Success rate: 100%
     - Average duration
   - Show agent usage statistics
   - "Each agent tracks its own performance"

5. **Create another blog to show scalability**
   - Create a second blog with orchestration
   - Show how metrics update in real-time
   - Demonstrate the auto-refresh feature

---

## Part 6: Optional Enhancements (If Time Permits)

### 6.1: Add Pipeline Detail View

Create a detailed view for individual pipelines showing:
- Step-by-step execution timeline
- Agent inputs and outputs
- Error messages if any
- Execution logs

### 6.2: Add Export Functionality

Add ability to export metrics as JSON or CSV for analysis.

### 6.3: Add Filtering

Add filters to view:
- Only completed pipelines
- Only failed pipelines
- Pipelines by date range
- Pipelines by agent type

---

## Summary

This delta enhancement adds:

1. **Real-time Dashboard** - Live view of agent performance
2. **Metrics Tracking** - Success rates, durations, agent usage
3. **Visual Feedback** - Progress bars, status indicators
4. **Auto-refresh** - Updates every 3 seconds
5. **Demo-ready UI** - Professional presentation for hackathon

**Total Implementation Time:** 1-2 hours

**Demo Impact:** HIGH - Clearly shows the multi-agent orchestration in action

**Technical Debt:** LOW - All code follows existing patterns and is production-ready

---

## Files Modified/Created

### New Files:
- `services/ui_service/templates/agent_dashboard.html`
- `enhancement1_B_delta_agent_dashboard.md` (this file)

### Modified Files:
- `services/orchestration_service/pipeline_manager.py` (add metrics method)
- `services/orchestration_service/main.py` (add metrics endpoint)
- `services/ui_service/main.py` (add dashboard route)
- `services/ui_service/templates/base.html` (add navigation link)
- `services/ui_service/templates/create.html` (add orchestration checkbox)
- `services/api_gateway/main.py` (add orchestration endpoint)

---

## Next Steps

After implementing this delta:
1. Test the complete workflow
2. Practice the demo script
3. Consider adding more agents (Research, Reviewer) from enhancement1_C and 1_D
4. Add the real-time dashboard from enhancement1_E for even more visual impact

---

**Made with Bob** 🤖