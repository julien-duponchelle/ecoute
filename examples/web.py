#
# Export the text to a web page with a player supporting the subtiles.
#
# Run a python server in the examples folder:
# python3 -m http.server 9000
# Open http://localhost:9000/web.html in a browser to see the result.


import openai

import oreille

client = openai.OpenAI()
print("Processing wav")
print(
    oreille.transcribe(
        client,
        model="whisper-1",
        file=open("examples/test.wav", "rb"),
        language="fr",
        prompt="Test son",
        response_format="verbose_json",
        audio_format="wav",
    )
)


transcribe = oreille.transcribe(
    client,
    file=open("examples/test.wav", "rb"),
    model="whisper-1",
    language="fr",
    prompt="Test son",
    response_format="vtt",
    audio_format="wav",
)

with open("examples/web.vtt", "w+") as f:
    f.write(transcribe)

print("Exported to web.vtt")
