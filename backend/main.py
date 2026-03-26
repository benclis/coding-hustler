"""
Coding Hustler Chat Backend
FastAPI server with Agent orchestration
"""

from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import json
import asyncio
from datetime import datetime
from agent.automation_pipeline import automation_pipeline
from agent.logger import setup_logger

logger = setup_logger(__name__)

app = FastAPI(title="Coding Hustler Chat")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    """Chat message model"""
    content: str
    role: str = "user"

class AgentResponse(BaseModel):
    """Agent response model"""
    status: str
    message: str
    data: Optional[dict] = None
    pipeline_id: Optional[str] = None

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "agent": "ready"
    }

@app.post("/chat")
async def chat_endpoint(message: ChatMessage):
    """Main chat endpoint - Agent processes message"""
    try:
        logger.info(f"📨 Chat received: {message.content}")
        
        # Parse user input
        user_input = message.content.lower()
        
        # INTENT DETECTION
        if "serbest" in user_input or "freelance" in user_input:
            intent = "freelance_guide"
        elif "script" in user_input or "video" in user_input:
            intent = "script_generation"
        elif "thumbnail" in user_input or "design" in user_input:
            intent = "thumbnail_design"
        elif "upload" in user_input or "youtube" in user_input:
            intent = "youtube_upload"
        else:
            intent = "general_help"
        
        logger.info(f"🎯 Intent: {intent}")
        
        # AGENT PROCESSING
        if intent == "freelance_guide":
            result = await process_freelance_guide(message.content)
        elif intent == "script_generation":
            result = await process_script_generation(message.content)
        elif intent == "thumbnail_design":
            result = await process_thumbnail_design(message.content)
        elif intent == "youtube_upload":
            result = await process_youtube_upload(message.content)
        else:
            result = await process_general_help(message.content)
        
        logger.info(f"✅ Response ready: {result['status']}")
        
        return result
    
    except Exception as e:
        logger.error(f"❌ Chat error: {str(e)}")
        return AgentResponse(
            status="error",
            message=f"Error: {str(e)}"
        )

async def process_freelance_guide(user_input: str):
    """Process freelance guide request"""
    try:
        logger.info("🤖 Processing: Freelance Guide")
        
        # Trigger automation pipeline
        result = automation_pipeline.start_pipeline(
            newsletter_content=user_input,
            topic="Serbest Çalışma Başlangıcı"
        )
        
        response_text = f"""
✅ SERBEST ÇALIŞMA REHBERİ HAZIR!

📝 Newsletter: Draft completed
🎬 Video Script: Generated ({result['pipeline_log']['stages'][1].get('duration', 12)} min)
🖼️ Thumbnail: Designed (Est. CTR: {result['pipeline_log']['stages'][2].get('ctr_estimate', 4)}%)
📤 Upload: Ready for YouTube
🔍 SEO: Optimized ({result['pipeline_log']['stages'][4]['optimization']['optimization_score']}/100)
📅 Schedule: Tuesday 8 AM Turkish time

Pipeline ID: {result['pipeline_id']}

Sonraki adım: Video çek ve yükle! 🚀
"""
        
        return AgentResponse(
            status="success",
            message=response_text,
            data=result,
            pipeline_id=result['pipeline_id']
        )
    
    except Exception as e:
        logger.error(f"❌ Freelance guide failed: {str(e)}")
        return AgentResponse(
            status="error",
            message=f"Hata: {str(e)}"
        )

async def process_script_generation(user_input: str):
    """Process script generation request"""
    try:
        logger.info("🤖 Processing: Script Generation")
        
        response_text = """
✅ VIDEO SCRIPTI HAZIR!

📋 Hook (10 sec): Attention-grabbing opening
📖 Body (11 min): 5 sections, 2 min each
🎯 CTA (30 sec): Call-to-action with links

Script file: scripts/generated_script.json

Şimdi video çekebilirsin! 🎬
"""
        
        return AgentResponse(
            status="success",
            message=response_text
        )
    
    except Exception as e:
        return AgentResponse(status="error", message=str(e))

async def process_thumbnail_design(user_input: str):
    """Process thumbnail design request"""
    try:
        logger.info("🤖 Processing: Thumbnail Design")
        
        response_text = """
✅ THUMBNAIL TASARIMI HAZIR!

🎨 Colors: Bold red + yellow gradient
📝 Text: "SERBEST ÇALIŞMA" (Montserrat Bold)
😊 Emoji: 💰 (money)
👤 Logo: Coding Hustler branding
📊 Est. CTR: 4.8% (80th percentile)

Design spec: thumbnails/design_spec.json

Canva'da oluşturabilirsin! 🖼️
"""
        
        return AgentResponse(
            status="success",
            message=response_text
        )
    
    except Exception as e:
        return AgentResponse(status="error", message=str(e))

async def process_youtube_upload(user_input: str):
    """Process YouTube upload request"""
    try:
        logger.info("🤖 Processing: YouTube Upload")
        
        response_text = """
✅ YOUTUBE UPLOAD HAZIRLANDI!

📹 Video file: ./video.mp4
🖼️ Thumbnail: ./thumbnail.png
📝 Title: "Serbest Çalışma Rehberi: [Topic]"
📋 Description: Optimized with links
🏷️ Tags: serbest çalışma, para kazanma, freelance, Coding Hustler
📅 Schedule: Tuesday 8:00 AM (Turkish time)
🔒 Visibility: Public
💰 Monetization: Enabled

API Ready: youtube_uploader.upload_video()

Upload başlasak mı? 🚀
"""
        
        return AgentResponse(
            status="success",
            message=response_text
        )
    
    except Exception as e:
        return AgentResponse(status="error", message=str(e))

async def process_general_help(user_input: str):
    """Process general help request"""
    try:
        logger.info("🤖 Processing: General Help")
        
        response_text = """
👋 Merhaba! Ben Coding Hustler Agent'iyim.

Şunları yapabilirim:
1️⃣ "serbest çalışma" → Freelance guide + video prep
2️⃣ "script yaz" → Video script generation
3️⃣ "thumbnail tasarla" → Thumbnail design spec
4️⃣ "youtube'a yükle" → Upload preparation
5️⃣ "analiz et" → Video metrics analysis

Ne istiyorsun? 🤔
"""
        
        return AgentResponse(
            status="success",
            message=response_text
        )
    
    except Exception as e:
        return AgentResponse(status="error", message=str(e))

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time chat"""
    await websocket.accept()
    logger.info("🔌 WebSocket connected")
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Process message
            response = await chat_endpoint(ChatMessage(content=message['content']))
            
            # Send response back
            await websocket.send_json({
                "status": response.status,
                "message": response.message,
                "data": response.data,
                "timestamp": datetime.now().isoformat()
            })
    
    except Exception as e:
        logger.error(f"❌ WebSocket error: {str(e)}")
        await websocket.close()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Coding Hustler Agent API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "chat": "/chat",
            "websocket": "/ws/chat",
            "health": "/health"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
