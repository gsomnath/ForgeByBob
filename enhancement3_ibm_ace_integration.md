# Enhancement 3: IBM App Connect Enterprise Integration

## Strategic Priority: ENTERPRISE INTEGRATION SHOWCASE
This enhancement integrates IBM App Connect Enterprise (ACE) to provide enterprise-grade notification and integration capabilities, demonstrating IBM's complete integration platform.

## Objective
Implement IBM ACE as the central integration hub for notifications, webhooks, and enterprise system connectivity—showcasing how IBM's integration platform complements the agentic AI workflow.

## IBM Technology Stack

### Primary Components
- **IBM App Connect Enterprise (ACE)**: Developer Edition for integration flows
- **ACE REST API**: HTTP endpoints for triggering flows
- **ACE Toolkit**: Visual flow designer for integration patterns

### Why IBM ACE
- **Enterprise-grade**: Production-ready integration platform
- **Visual design**: No-code/low-code flow creation
- **Extensive connectors**: 100+ pre-built connectors for enterprise systems
- **Scalability**: Handles high-volume message processing
- **Reliability**: Built-in error handling and retry logic

## Integration Architecture

### Current State: Manual Notifications
```
Blog Published → Manual Email → Manual Slack Post
    (manual)        (manual)         (manual)
```

### Target State: ACE-Orchestrated Integration
```
Blog Published Event
        ↓
Notifier Agent (Orchestrate)
        ↓
IBM ACE REST API
        ↓
┌───────┴────────┬──────────┬──────────┬──────────┐
│                │          │          │          │
SMTP           Slack      Teams      Webhook    Custom
Connector      Connector  Connector  Connector  Integration
│                │          │          │          │
└────────────────┴──────────┴──────────┴──────────┘
        ↓
Stakeholder Notifications + Audit Log
```

## ACE Integration Flows

### Flow 1: Email Notification
**Purpose**: Send formatted email notifications to stakeholders

**Flow Design**
```
HTTP Input → Transform Message → SMTP Output → Log Event
```

**Input Schema**
```json
{
  "notification_type": "blog_published",
  "blog_id": "blog-123",
  "blog_title": "The Future of Agentic AI",
  "blog_url": "https://medium.com/@user/future-of-agentic-ai",
  "trust_score": 8.5,
  "recipients": ["editor@company.com", "marketing@company.com"],
  "metadata": {
    "author": "AI Agent",
    "publish_time": "2024-01-15T10:30:00Z",
    "word_count": 1240
  }
}
```

**Email Template**
```html
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; }
        .header { background: #0f62fe; color: white; padding: 20px; }
        .content { padding: 20px; }
        .trust-badge { display: inline-block; padding: 5px 10px; border-radius: 5px; }
        .trust-green { background: #24a148; color: white; }
        .footer { background: #f4f4f4; padding: 10px; text-align: center; }
    </style>
</head>
<body>
    <div class="header">
        <h2>📝 New Blog Published</h2>
    </div>
    <div class="content">
        <h3>{{ blog_title }}</h3>
        <p><strong>Published URL:</strong> <a href="{{ blog_url }}">{{ blog_url }}</a></p>
        <p><strong>Trust Score:</strong> <span class="trust-badge trust-green">{{ trust_score }}/10</span></p>
        <p><strong>Word Count:</strong> {{ word_count }} words</p>
        <p><strong>Published:</strong> {{ publish_time }}</p>
        
        <h4>Agent Pipeline Summary</h4>
        <ul>
            <li>✓ Research Agent: Sources analyzed</li>
            <li>✓ Writer Agent: Content generated</li>
            <li>✓ Reviewer Agent: Quality approved</li>
            <li>✓ Publisher Agent: Published successfully</li>
        </ul>
    </div>
    <div class="footer">
        <p>Powered by IBM watsonx & IBM App Connect Enterprise</p>
    </div>
</body>
</html>
```

**ACE Flow Configuration**
```xml
<!-- ACE Message Flow XML -->
<MessageFlow name="BlogPublishedEmail">
    <HTTPInput path="/api/notify/email">
        <Property name="method" value="POST"/>
    </HTTPInput>
    
    <Compute name="TransformToEmail">
        <ESQL>
            SET OutputRoot.EmailEnvelope.To = InputRoot.JSON.Data.recipients;
            SET OutputRoot.EmailEnvelope.Subject = 'Blog Published: ' || InputRoot.JSON.Data.blog_title;
            SET OutputRoot.EmailEnvelope.Body = CALL FormatEmailTemplate(InputRoot.JSON.Data);
        </ESQL>
    </Compute>
    
    <EmailOutput name="SendEmail">
        <Property name="smtpServer" value="${SMTP_SERVER}"/>
        <Property name="smtpPort" value="${SMTP_PORT}"/>
        <Property name="username" value="${SMTP_USERNAME}"/>
        <Property name="password" value="${SMTP_PASSWORD}"/>
    </EmailOutput>
    
    <Compute name="LogEvent">
        <ESQL>
            CALL LogNotificationEvent(InputRoot.JSON.Data, 'email', 'success');
        </ESQL>
    </Compute>
    
    <HTTPReply>
        <Property name="statusCode" value="200"/>
    </HTTPReply>
</MessageFlow>
```

### Flow 2: Slack Notification
**Purpose**: Post formatted messages to Slack channels

**Flow Design**
```
HTTP Input → Transform to Slack Format → Slack Webhook → Log Event
```

**Slack Message Format**
```json
{
  "channel": "#content-updates",
  "username": "BlogAgent Pro",
  "icon_emoji": ":robot_face:",
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "📝 New Blog Published"
      }
    },
    {
      "type": "section",
      "fields": [
        {
          "type": "mrkdwn",
          "text": "*Title:*\nThe Future of Agentic AI"
        },
        {
          "type": "mrkdwn",
          "text": "*Trust Score:*\n8.5/10 ✓"
        }
      ]
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Published URL:* <https://medium.com/@user/future-of-agentic-ai|View Blog>"
      }
    },
    {
      "type": "context",
      "elements": [
        {
          "type": "mrkdwn",
          "text": "Powered by IBM watsonx | 12 minutes from idea to publish"
        }
      ]
    }
  ]
}
```

**ACE Flow Configuration**
```xml
<MessageFlow name="BlogPublishedSlack">
    <HTTPInput path="/api/notify/slack">
        <Property name="method" value="POST"/>
    </HTTPInput>
    
    <Compute name="TransformToSlack">
        <ESQL>
            DECLARE slackWebhook CHARACTER '${SLACK_WEBHOOK_URL}';
            SET OutputRoot.JSON.Data = CALL FormatSlackMessage(InputRoot.JSON.Data);
        </ESQL>
    </Compute>
    
    <HTTPRequest name="PostToSlack">
        <Property name="url" value="${SLACK_WEBHOOK_URL}"/>
        <Property name="method" value="POST"/>
        <Property name="contentType" value="application/json"/>
    </HTTPRequest>
    
    <Compute name="LogEvent">
        <ESQL>
            CALL LogNotificationEvent(InputRoot.JSON.Data, 'slack', 'success');
        </ESQL>
    </Compute>
    
    <HTTPReply>
        <Property name="statusCode" value="200"/>
    </HTTPReply>
</MessageFlow>
```

### Flow 3: Microsoft Teams Notification
**Purpose**: Post adaptive cards to Teams channels

**Flow Design**
```
HTTP Input → Transform to Teams Format → Teams Webhook → Log Event
```

**Teams Adaptive Card**
```json
{
  "@type": "MessageCard",
  "@context": "https://schema.org/extensions",
  "summary": "New Blog Published",
  "themeColor": "0078D4",
  "title": "📝 New Blog Published",
  "sections": [
    {
      "activityTitle": "The Future of Agentic AI",
      "activitySubtitle": "Published by AI Agent Pipeline",
      "facts": [
        {
          "name": "Trust Score:",
          "value": "8.5/10 ✓"
        },
        {
          "name": "Word Count:",
          "value": "1,240 words"
        },
        {
          "name": "Time to Publish:",
          "value": "12 minutes"
        }
      ]
    }
  ],
  "potentialAction": [
    {
      "@type": "OpenUri",
      "name": "View Blog",
      "targets": [
        {
          "os": "default",
          "uri": "https://medium.com/@user/future-of-agentic-ai"
        }
      ]
    }
  ]
}
```

### Flow 4: Webhook Integration
**Purpose**: Generic webhook for custom integrations

**Flow Design**
```
HTTP Input → Transform Payload → HTTP Request → Retry Logic → Log Event
```

**Webhook Payload**
```json
{
  "event": "blog.published",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {
    "blog_id": "blog-123",
    "title": "The Future of Agentic AI",
    "url": "https://medium.com/@user/future-of-agentic-ai",
    "trust_score": 8.5,
    "metadata": {
      "word_count": 1240,
      "agent_pipeline": {
        "research": "completed",
        "writing": "completed",
        "review": "approved",
        "publish": "success"
      }
    }
  }
}
```

## Implementation Roadmap

### Phase 1: ACE Installation & Setup (1 hour)

**Step 1.1: Install IBM ACE Developer Edition**
```bash
# Download from IBM website
# https://www.ibm.com/products/app-connect/developer-edition

# Windows installation
1. Download ACE Developer Edition installer
2. Run installer with default options
3. Install ACE Toolkit for visual flow design
4. Verify installation: mqsiversion
```

**Step 1.2: Create Integration Server**
```bash
# Create integration server
mqsicreateintegrationserver -i TESTNODE_user -e BlogAgentServer

# Start integration server
mqsistart TESTNODE_user

# Verify server status
mqsilist
```

**Step 1.3: Configure Environment Variables**
```bash
# Add to .env file
IBM_ACE_HOST=localhost
IBM_ACE_PORT=7800
IBM_ACE_API_KEY=<generated_api_key>

# SMTP Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=<your_email>
SMTP_PASSWORD=<app_password>

# Slack Configuration
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# Teams Configuration
TEAMS_WEBHOOK_URL=https://outlook.office.com/webhook/YOUR/WEBHOOK/URL
```

### Phase 2: Create ACE Flows (1 hour)

**Step 2.1: Email Notification Flow**
```bash
# Using ACE Toolkit
1. Open ACE Toolkit
2. Create new Message Flow: "BlogPublishedEmail"
3. Add HTTP Input node (path: /api/notify/email)
4. Add Compute node for email transformation
5. Add Email Output node with SMTP configuration
6. Add Compute node for logging
7. Add HTTP Reply node
8. Deploy to BlogAgentServer
```

**Step 2.2: Slack Notification Flow**
```bash
# Using ACE Toolkit
1. Create new Message Flow: "BlogPublishedSlack"
2. Add HTTP Input node (path: /api/notify/slack)
3. Add Compute node for Slack message formatting
4. Add HTTP Request node for Slack webhook
5. Add error handling subflow
6. Deploy to BlogAgentServer
```

**Step 2.3: Teams Notification Flow**
```bash
# Using ACE Toolkit
1. Create new Message Flow: "BlogPublishedTeams"
2. Add HTTP Input node (path: /api/notify/teams)
3. Add Compute node for Teams adaptive card
4. Add HTTP Request node for Teams webhook
5. Deploy to BlogAgentServer
```

**Step 2.4: Generic Webhook Flow**
```bash
# Using ACE Toolkit
1. Create new Message Flow: "BlogPublishedWebhook"
2. Add HTTP Input node (path: /api/notify/webhook)
3. Add Compute node for payload transformation
4. Add HTTP Request node with retry logic
5. Add error handling and logging
6. Deploy to BlogAgentServer
```

### Phase 3: Python Integration Layer (30 minutes)

**Step 3.1: Create ACE Client**
```bash
mkdir -p tools
touch tools/__init__.py
touch tools/ibm_ace_client.py
```

**Step 3.2: Implement ACE Client**
```python
# tools/ibm_ace_client.py
import httpx
import os
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class IBMACEClient:
    """Client for IBM App Connect Enterprise REST API"""
    
    def __init__(self):
        self.host = os.getenv("IBM_ACE_HOST", "localhost")
        self.port = os.getenv("IBM_ACE_PORT", "7800")
        self.api_key = os.getenv("IBM_ACE_API_KEY")
        self.base_url = f"http://{self.host}:{self.port}"
    
    async def send_email_notification(
        self,
        blog_id: str,
        blog_title: str,
        blog_url: str,
        trust_score: float,
        recipients: List[str],
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Send email notification via ACE"""
        payload = {
            "notification_type": "blog_published",
            "blog_id": blog_id,
            "blog_title": blog_title,
            "blog_url": blog_url,
            "trust_score": trust_score,
            "recipients": recipients,
            "metadata": metadata
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/notify/email",
                    json=payload,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    logger.info(f"Email notification sent for blog {blog_id}")
                    return {"success": True, "channel": "email"}
                else:
                    logger.error(f"Email notification failed: {response.text}")
                    return {"success": False, "error": response.text}
        
        except Exception as e:
            logger.error(f"ACE email notification error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def send_slack_notification(
        self,
        blog_id: str,
        blog_title: str,
        blog_url: str,
        trust_score: float,
        channel: str = "#content-updates"
    ) -> Dict[str, Any]:
        """Send Slack notification via ACE"""
        payload = {
            "notification_type": "blog_published",
            "blog_id": blog_id,
            "blog_title": blog_title,
            "blog_url": blog_url,
            "trust_score": trust_score,
            "channel": channel
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/notify/slack",
                    json=payload,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    logger.info(f"Slack notification sent for blog {blog_id}")
                    return {"success": True, "channel": "slack"}
                else:
                    logger.error(f"Slack notification failed: {response.text}")
                    return {"success": False, "error": response.text}
        
        except Exception as e:
            logger.error(f"ACE Slack notification error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def send_teams_notification(
        self,
        blog_id: str,
        blog_title: str,
        blog_url: str,
        trust_score: float
    ) -> Dict[str, Any]:
        """Send Microsoft Teams notification via ACE"""
        payload = {
            "notification_type": "blog_published",
            "blog_id": blog_id,
            "blog_title": blog_title,
            "blog_url": blog_url,
            "trust_score": trust_score
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/notify/teams",
                    json=payload,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    logger.info(f"Teams notification sent for blog {blog_id}")
                    return {"success": True, "channel": "teams"}
                else:
                    logger.error(f"Teams notification failed: {response.text}")
                    return {"success": False, "error": response.text}
        
        except Exception as e:
            logger.error(f"ACE Teams notification error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def send_webhook_notification(
        self,
        webhook_url: str,
        blog_id: str,
        blog_title: str,
        blog_url: str,
        trust_score: float,
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Send generic webhook notification via ACE"""
        payload = {
            "notification_type": "blog_published",
            "webhook_url": webhook_url,
            "blog_id": blog_id,
            "blog_title": blog_title,
            "blog_url": blog_url,
            "trust_score": trust_score,
            "metadata": metadata
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/notify/webhook",
                    json=payload,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    logger.info(f"Webhook notification sent for blog {blog_id}")
                    return {"success": True, "channel": "webhook"}
                else:
                    logger.error(f"Webhook notification failed: {response.text}")
                    return {"success": False, "error": response.text}
        
        except Exception as e:
            logger.error(f"ACE webhook notification error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def send_all_notifications(
        self,
        blog_id: str,
        blog_title: str,
        blog_url: str,
        trust_score: float,
        recipients: List[str],
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Send notifications to all configured channels"""
        results = {
            "blog_id": blog_id,
            "notifications": []
        }
        
        # Send email
        email_result = await self.send_email_notification(
            blog_id, blog_title, blog_url, trust_score, recipients, metadata
        )
        results["notifications"].append(email_result)
        
        # Send Slack
        slack_result = await self.send_slack_notification(
            blog_id, blog_title, blog_url, trust_score
        )
        results["notifications"].append(slack_result)
        
        # Send Teams
        teams_result = await self.send_teams_notification(
            blog_id, blog_title, blog_url, trust_score
        )
        results["notifications"].append(teams_result)
        
        # Check overall success
        results["success"] = all(n.get("success", False) for n in results["notifications"])
        
        return results
```

### Phase 4: Notifier Agent Integration (30 minutes)

**Step 4.1: Update Notifier Agent**
```python
# services/orchestration_service/notifier_agent.py
from tools.ibm_ace_client import IBMACEClient

class NotifierAgent:
    """Notifier Agent using IBM ACE for enterprise integrations"""
    
    def __init__(self):
        self.ace_client = IBMACEClient()
    
    async def notify_stakeholders(
        self,
        blog_id: str,
        blog_title: str,
        blog_url: str,
        trust_score: float,
        recipients: List[str],
        metadata: Dict[str, Any]
    ):
        """Send notifications via IBM ACE"""
        
        logger.info(f"Notifier Agent: Sending notifications for blog {blog_id}")
        
        # Send all notifications via ACE
        results = await self.ace_client.send_all_notifications(
            blog_id=blog_id,
            blog_title=blog_title,
            blog_url=blog_url,
            trust_score=trust_score,
            recipients=recipients,
            metadata=metadata
        )
        
        # Log notification events
        await self.log_notification_events(blog_id, results)
        
        return results
    
    async def log_notification_events(self, blog_id: str, results: Dict[str, Any]):
        """Log notification events for audit trail"""
        log_entry = {
            "blog_id": blog_id,
            "timestamp": datetime.utcnow().isoformat(),
            "notifications": results["notifications"],
            "success": results["success"]
        }
        
        # Save to notification logs
        logs = load_notification_logs()
        if blog_id not in logs:
            logs[blog_id] = []
        logs[blog_id].append(log_entry)
        save_notification_logs(logs)
```

**Step 4.2: Register ACE Skill in Orchestrate**
```yaml
# Orchestrate skill definition
skill_name: send_notification_via_ace
description: Send notifications via IBM App Connect Enterprise
parameters:
  - name: blog_id
    type: string
    required: true
  - name: blog_title
    type: string
    required: true
  - name: blog_url
    type: string
    required: true
  - name: trust_score
    type: number
    required: true
  - name: recipients
    type: array
    required: true
implementation:
  type: rest_api
  endpoint: http://localhost:8004/notifier/send
  method: POST
```

## Success Metrics

### Integration Coverage
- **Email**: SMTP integration for stakeholder notifications
- **Slack**: Real-time team updates
- **Teams**: Enterprise collaboration integration
- **Webhooks**: Custom system integrations

### Reliability
- **Delivery rate**: 99.9% notification delivery
- **Retry logic**: Automatic retry on failure (3 attempts)
- **Error handling**: Graceful degradation if channel unavailable

### Auditability
- **Event logging**: All notifications logged with timestamps
- **Delivery confirmation**: Track successful/failed deliveries
- **Compliance**: Full audit trail for governance

### Performance
- **Latency**: < 2 seconds per notification
- **Throughput**: 100+ notifications per minute
- **Scalability**: ACE handles enterprise-scale message volumes

## Technical Dependencies

### IBM ACE
```txt
# IBM App Connect Enterprise Developer Edition
Version: 12.0 or higher
License: Free for development and testing
```

### Python Packages
```txt
# HTTP client for ACE REST API
httpx>=0.27.0
```

### Configuration
```bash
# ACE server configuration
IBM_ACE_HOST=localhost
IBM_ACE_PORT=7800
IBM_ACE_API_KEY=<generated_key>

# SMTP configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=<email>
SMTP_PASSWORD=<app_password>

# Slack webhook
SLACK_WEBHOOK_URL=<webhook_url>

# Teams webhook
TEAMS_WEBHOOK_URL=<webhook_url>
```

