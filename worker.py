import asyncio

async def audit_model_task(model_id, bits):
    print(f"[Async] Starting parallel audit: {model_id}")
    # Simulating heavy GPU/CPU task
    await asyncio.sleep(1) 
    return f"Done: {model_id}"

async def main_async(models_list):
    tasks = [audit_model_task(m, 4) for m in models_list]
    results = await asyncio.gather(*tasks)
    print(results)