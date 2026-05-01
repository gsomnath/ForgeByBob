# ForgeByBob - Base Application Architecture

## Overview
AI-powered blog content generation platform built on microservices architecture. Currently powered by Google Gemini AI, designed for enterprise transformation with IBM watsonx technology stack.

## Current Architecture

### Microservices Design
The application consists of four independent services communicating via REST APIs:

1. **API Gateway** (Port 8000)
   - Central request routing and API orchestration
   - Unified interface for all client interactions
   - Service discovery and load balancing ready

2. **Blog Service** (Port 8001)
   - Blog content lifecycle management
   - AI content generation via Gemini API
   - Version control system for drafts
   - File-based storage with JSON persistence

3. **Settings Service** (Port 8002)
   - Centralized configuration management
   - Secure API key storage and retrieval
   - User preferences and publication settings

4. **UI Service** (Port 8003)
   - Web-based user interface
   - Real-time content preview
   - Settings management dashboard
   - API logs visualization

### Technology Stack

**Backend Framework**
- Python 3.11+ with FastAPI
- Async/await for concurrent operations
- Pydantic for data validation

**AI Integration**
- Google Gemini AI for text generation
- Google Imagen for image generation
- Request/response logging system

**Data Storage**
- File-based JSON storage
- Structured blog metadata
- Version history tracking

**Frontend**
- Jinja2 templating engine
- Server-side rendering
- Responsive HTML/CSS design

### Core Features

**Blog Management**
- Create blog projects with metadata (title, tags, description)
- Organize content in structured folders
- Track multiple draft versions
- Comment system for collaboration

**AI Content Generation**
- Prompt-based content creation
- Customizable generation parameters
- Image generation integration
- API call logging and monitoring

**Configuration System**
- Dynamic API key management
- Source folder configuration
- Publication site settings
- Google Cloud integration for Imagen

**Monitoring & Logging**
- Gemini API request/response logs
- Imagen API interaction tracking
- Paginated log viewing interface
- Error tracking and debugging

### Data Flow Architecture

```
User Request
    ↓
UI Service (Port 8003)
    ↓
API Gateway (Port 8000)
    ↓
┌─────────────┴─────────────┐
│                           │
Blog Service          Settings Service
(Port 8001)          (Port 8002)
    ↓                       ↓
Gemini API            Configuration
    ↓                    Storage
Content Storage
```

### Current Limitations & Transformation Opportunities

**Workflow Limitations**
- Manual, sequential operations requiring user intervention at each step
- No autonomous decision-making or agent coordination
- Single-threaded content generation process

**AI Provider Lock-in**
- Dependency on Google Gemini ecosystem
- No multi-model strategy or fallback options
- Limited to Google's API capabilities and pricing

**Quality Control Gaps**
- No automated content review or validation
- Manual quality assessment required
- No trust scoring or governance layer

**Integration Constraints**
- No enterprise notification system
- Manual publishing workflow
- Limited third-party integrations

**Scalability Concerns**
- File-based storage limits concurrent operations
- No distributed agent coordination
- Single-instance deployment model

## Transformation Vision

This solid microservices foundation provides an ideal platform for enhancement with:

**Agentic AI Architecture**
- Multi-agent coordination and autonomous workflows
- Self-correcting quality loops
- Parallel task execution

**Enterprise IBM Stack**
- IBM watsonx Orchestrate for agent management
- IBM watsonx.ai (Granite models) for LLM operations
- IBM App Connect Enterprise for integrations

**Governance & Trust**
- Automated content quality scoring
- Responsible AI compliance
- Audit trails and transparency

**Scalability & Reliability**
- Distributed agent coordination
- Enterprise-grade integrations
- Production-ready deployment patterns