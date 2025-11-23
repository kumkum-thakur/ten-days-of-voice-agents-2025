import json
import logging
import os
from datetime import datetime
from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    JobProcess,
    MetricsCollectedEvent,
    RoomInputOptions,
    WorkerOptions,
    cli,
    metrics,
    tokenize,
)
from livekit.plugins import murf, silero, google, deepgram, noise_cancellation
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("agent")
load_dotenv(".env.local")

# ---------------------------
# Helper: Natural-language parser
# ---------------------------
def parse_order_from_text(text):
    text = text.lower()
    drinks = ["latte", "cappuccino", "americano", "espresso", "cold coffee", "iced coffee", "mocha", "flat white", "tea", "chai", "hot chocolate", "filter coffee"]
    found_drink = next((d for d in drinks if d in text), None)

    size = None
    if "small" in text or "s " in text: size = "small"
    if "medium" in text or "m " in text or "med " in text: size = "medium"
    if "large" in text or "l " in text: size = "large"

    milk = None
    for m in ["whole", "skim", "almond", "oat", "soy", "milk", "non-dairy", "no milk"]:
        if m in text:
            milk = m
            break

    extras = []
    for e in ["whipped", "whipped cream", "caramel", "vanilla", "extra shot", "sugar", "sweetener", "honey", "ice", "no ice", "none"]:
        if e in text:
            extras.append(e)
    extras = list(dict.fromkeys(extras))

    name = None
    import re
    for pattern in [r"for (\w+)", r"my name is (\w+)", r"this is (\w+)"]:
        m = re.search(pattern, text)
        if m:
            name = m.group(1).capitalize()
            break

    return {
        "drinkType": found_drink,
        "size": size,
        "milk": milk,
        "extras": extras if extras != ["none"] else [],
        "name": name,
    }

# ---------------------------
# Barista Agent
# ---------------------------
class BaristaAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions="""
You are a friendly desi-cafe barista named 'BrewBuddy'. Speak in warm, mildly Hinglish.
Ask clarifying questions until the order has: drinkType, size, milk, extras, name.
Once complete, output JSON exactly in this format, wrapped between MARKER_ORDER_START and MARKER_ORDER_END:

MARKER_ORDER_START
{"drinkType":"<drink>","size":"<size>","milk":"<milk>","extras":["<extra1>", "<extra2>"],"name":"<name>"}
MARKER_ORDER_END

Do NOT output anything else between the markers. Always use valid JSON.
"""
        )

# ---------------------------
# Prewarm VAD
# ---------------------------
def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()

# ---------------------------
# Entrypoint
# ---------------------------
async def entrypoint(ctx: JobContext):
    session = AgentSession(
        stt=deepgram.STT(model="nova-3"),
        llm=google.LLM(model="gemini-2.5-flash"),
        tts=murf.TTS(
            voice="en-US-matthew",
            style="Conversation",
            tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
            text_pacing=True,
        ),
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        preemptive_generation=True,
    )

    usage_collector = metrics.UsageCollector()

    @session.on("metrics_collected")
    def _on_metrics_collected(ev: MetricsCollectedEvent):
        metrics.log_metrics(ev.metrics)
        usage_collector.collect(ev.metrics)

    async def log_usage():
        summary = usage_collector.get_summary()
        logger.info(f"Usage: {summary}")

    ctx.add_shutdown_callback(log_usage)

    await session.start(
        agent=BaristaAgent(),
        room=ctx.room,
        room_input_options=RoomInputOptions(noise_cancellation=noise_cancellation.BVC()),
    )

    await ctx.connect()

    # ---------------------------
    # Save order function
    # ---------------------------
    async def _save_order_from_text(resp_text: str):
        if not resp_text:
            return
        start = resp_text.find("MARKER_ORDER_START")
        end = resp_text.find("MARKER_ORDER_END")
        if start != -1 and end != -1 and end > start:
            json_text = resp_text[start + len("MARKER_ORDER_START"):end].strip()
            try:
                order = json.loads(json_text)
            except Exception as e:
                logger.error("Failed to parse order JSON: %s", e)
                return

            if isinstance(order.get("extras"), str) and order["extras"].lower() == "none":
                order["extras"] = []

            orders_dir = os.path.join(os.path.dirname(__file__), "..", "orders")
            os.makedirs(orders_dir, exist_ok=True)
            ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
            name_safe = order.get("name") or "guest"
            filename = f"order_{name_safe}_{ts}.json"
            path = os.path.join(orders_dir, filename)
            try:
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(order, f, indent=4, ensure_ascii=False)
                logger.info("✅ Order saved: %s", filename)
            except Exception as e:
                logger.exception("Failed to save order JSON: %s", e)

    # ---------------------------
    # Capture all assistant responses
    # ---------------------------
    @session.on("assistant_response")
    async def _on_assistant_response(event):
        text = getattr(event, "text", None) or str(event)
        await _save_order_from_text(text)

# ---------------------------
# Run CLI
# ---------------------------
if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
