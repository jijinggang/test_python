import asyncio
import os
from playsound import playsound  # pip install playsound=1.2.2
import edge_tts

async def main():
    while True:
        txt = input("Enter text: ")
        communicate = edge_tts.Communicate(txt,voice='zh-CN-XiaoxiaoNeural',rate="+0%")
        fname = "hello.mp3"
        await communicate.save(fname)
        playsound(fname)
        os.remove(fname)


if __name__ == "__main__":
    asyncio.run(main())