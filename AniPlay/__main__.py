import importlib
from AniPlay import app
from pyrogram import idle
from AniPlay.plugins import ALL_MODULES

async def init():
    try:
        for module in ALL_MODULES:
            try:
                importlib.import_module("AniPlay.plugins." + module)
            except Exception as e:
                print(f"[ERROR]: Module {module} failed to import. Exception: {str(e)}")

        print("[INFO]: Imported Modules Successfully")

        await app.start()
        print("[INFO]: Bot Started")
        await idle()
    finally:
        if app.is_initialized:
            print("[INFO]: BOT STOPPED")
            await app.stop()

if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init())
