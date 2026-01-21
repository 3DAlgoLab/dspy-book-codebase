import dspy
from dspy import streamify
from dspy.streaming import StreamListener  # <1>
from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse

app = FastAPI()

gemini = dspy.LM(model="gemini/gemini-2.5-pro")  # <2>
dspy.configure(lm=gemini)

class QA(dspy.Signature):
    """Answer questions with detailed explanations."""
    question = dspy.InputField()
    answer = dspy.OutputField()

@app.get('/chat/stream')
async def stream_chat(question: str = Query(..., description="The question to ask")):
    async def generate():
        stream_listeners = [  # <3>
            StreamListener(signature_field_name="reasoning"),
            StreamListener(signature_field_name="answer")
        ]
        
        predictor = dspy.ChainOfThought(QA)
        streaming_predictor = streamify(predictor, stream_listeners=stream_listeners)  # <4>
        
        has_streamed = False  # <5>
        
        async for chunk in streaming_predictor(question=question):  # <6>
            if isinstance(chunk, dspy.streaming.StreamResponse):  # <7>
                has_streamed = True
                yield f"{chunk.chunk}"
            elif isinstance(chunk, dspy.Prediction):  # <8>
                if not has_streamed:  # <9>
                    if hasattr(chunk, 'reasoning') and chunk.reasoning:
                        yield f"{chunk.reasoning}"
                    if hasattr(chunk, 'answer') and chunk.answer:
                        yield f"{chunk.answer}"
    
    return StreamingResponse(generate(), media_type='text/event-stream')