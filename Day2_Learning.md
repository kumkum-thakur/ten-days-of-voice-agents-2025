Day 2 – Coffee Shop Barista Agent



\## Introduction



\# This is my Day 2 submission for the AI Voice Agents Challenge by Murf.ai. The goal for this day was to turn the starter voice agent into a coffee shop barista capable of taking real-time voice orders, maintaining a small order state, and providing a text summary.



\## Overview



\# For Day 2, I successfully modified my Day 1 starter agent to function as a coffee shop barista. This involved:



-Adding order state management



-Integrating friendly barista responses



-Handling multiple drink orders



-Displaying a neat order summary



The backend now handles order logic, while the frontend still captures real-time voice input.



\## What I Did



-Backend Changes



-Modified agent.py to include coffee shop persona



-Added orders state object:



{

  "drinkType": "",

  "size": "",

  "extras": \[],

  "quantity": 0

}





-Implemented conversational logic for:



-Taking orders



-Updating order summary



-Handling multiple items



-Frontend Changes



-Verified that voice input correctly maps to order state



-Displayed text summary for order confirmation





\## Screenshots



!\[Frontend Running](screenshots/day2/frontend1.png)



\*\*Backend Running:\*\*  

!\[Backend Running](screenshots/day2/backend1.png)



\*\* Order Summary Script:\*\*  

!\[script](screenshots/day2/Script.png)



\## Learnings



Managing a small state object for multi-step conversations



Implementing a persona in the voice agent



Integrating real-time voice orders with backend logic



Displaying dynamic text summaries of user orders



Enhancing error handling for unexpected user input



\## How to Run This Project



1. Clone the repo:



git clone https://github.com/kumkum-thakur/ten-days-of-voice-agents-2025.git





2\. Set up the backend:



cd backend

cp .env.example .env.local

\# Edit .env.local with credentials:

\# LIVEKIT\_URL, LIVEKIT\_API\_KEY, LIVEKIT\_API\_SECRET, MURF\_API\_KEY, GOOGLE\_API\_KEY, DEEPGRAM\_API\_KEY

python -m src.agent start





3\. (Optional) Run backend tests:



uv run pytest





4\. Set up the frontend:



cd ../frontend

cp .env.example .env.local

\# Edit .env.local with LiveKit credentials

pnpm install

pnpm dev





5\. Open the app:



Go to: http://localhost:3000



Start talking to your coffee shop barista agent and see real-time responses.

