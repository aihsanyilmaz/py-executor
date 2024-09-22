import os, importlib.util, inspect, time
from datetime import datetime
from modules.pusher import pusher

FILES_FOLDER = os.path.join(os.getcwd(), "files")

def getFilePath(file: str) -> str:
    return os.path.join(FILES_FOLDER, f"{file}.py")

def logExecution(status: bool, executionTime: float, processId: str, file: str, args: list, kwargs: dict):
    LOG_FILE = os.path.join(os.getcwd(), "execution.log")
    with open(LOG_FILE, "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if(status == True):
            prefix = f"Execution: {executionTime:.2f} sec"
        else:
            prefix = "STATUS: FALSE"

        log_entry = f"{timestamp} - {prefix} - File: {file} - ProcessId: {processId} - Args: {args} - Kwargs: {kwargs}\n"
        f.write(log_entry)

async def runFile(processId: str, file: str, args: list, kwargs: dict):
    try:
        status = True
        startTime = time.time()
        
        filePath = getFilePath(file)
        
        if not os.path.exists(filePath):
            status = False

        spec = importlib.util.spec_from_file_location(file, filePath)
        if spec is None:
            status = False

        module = importlib.util.module_from_spec(spec)
        if module is None:
            status = False

        try:
            spec.loader.exec_module(module)
        except Exception:
            status = False

        if not hasattr(module, 'main') or not inspect.isfunction(module.main):
            status = False

        if status:
            module.pusher = lambda channel, event, data: pusher(channel, event, data)
            if inspect.iscoroutinefunction(module.main):
                await module.main(processId, *args, **kwargs)
            else:
                module.main(processId, *args, **kwargs)

        executionTime = time.time() - startTime            
        logExecution(status, executionTime, processId, file, args, kwargs)

    except Exception:
        return False

    return True