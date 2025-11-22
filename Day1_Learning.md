 # Day 1 - Starter Voice Agent



 ## Overview

For Day 1 of the AI Voice Agents Challenge, I successfully set up my starter voice agent using the provided monorepo from Murf.ai. This involved running both the frontend (React/Next.js) and backend (LiveKit + Murf Falcon TTS) and verifying that the agent responds in real-time.



 ## What I Did

 - Cloned the official repository.

 - Set up the backend:

&nbsp; - Configured `.env.local` with LiveKit and Murf Falcon credentials.

&nbsp; - Ran `uv run pytest` → all tests passed ✅

&nbsp; - Started the backend agent using `uv run python src/agent.py dev`

\- Set up the frontend:

&nbsp; - Configured `.env.local` with LiveKit credentials.

&nbsp; - Ran `pnpm install` and `pnpm dev`

&nbsp; - Verified real-time voice interaction

 - Fixed environment variables for frontend connection (`route.ts`)



 ## Screenshots

\*\*Frontend Running:\*\*  

!\[Frontend Running](screenshots/shot1.png)



\*\*Agent Responding:\*\*  

!\[Agent Responding](screenshots/shot2.png)



\*(Replace these placeholders with your actual screenshots)\*



 ## Learnings

 - How to integrate LiveKit Agents with a React frontend.

 - Setting up Murf Falcon TTS for ultra-fast, real-time voice responses.

 - Understanding environment variables in Next.js projects.

 - Basics of running Python backend agents with LiveKit.

 - Running tests using `pytest` to ensure everything works.



 ## How to Run This Project

1. Clone the repo:

&nbsp;  ```bash

&nbsp;  git clone https://github.com/kumkum-thakur/ten-days-of-voice-agents-2025.git

2. Setup the backend 

-cd backend
-uv sync                       

-cp .env.example .env.local    

# Edit .env.local with your credentials:
# LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET, MURF_API_KEY, GOOGLE_API_KEY, DEEPGRAM_API_KEY
uv run python src/agent.py dev # Start backend agent

3. Run backend tests(optional)
 
-uv run pytest

4. Set up the frontend

-cd ../frontend

-pnpm install
-cp .env.example .env.local    # Copy environment file
# Edit .env.local with LiveKit credentials

pnpm dev                     

5. Open the app

-Go to: http://localhost:3000 in your browser

-Start talking to your voice agent and see real-time responses.






