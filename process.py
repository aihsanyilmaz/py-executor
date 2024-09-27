import os, importlib.util, inspect, traceback, time
from datetime import datetime
from modules.pusher import pusher

PACKAGE_FOLDER = os.path.join(os.getcwd(), "packages")

async def packageRun(processId: str, p: str, args: dict):
    status = True
    try:
        startTime = time.time()
        path = getPackagePath(p)
        
        if not os.path.exists(path):
            status = False

        spec = importlib.util.spec_from_file_location(p, path)
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
                await module.main(processId, **args)
            else:
                module.main(processId, **args)

    except Exception:
        with open("process.failed.log", "w") as fi:
            error_message = f"Error in packageRun: {str(e)}\n{traceback.format_exc()}"
            fi.write(f"Error details:\n{error_message}\n")
        return False

    executionTime = time.time() - startTime            
    logExecution(status, executionTime, processId, p, args)

    return status

def getPackagePath(file: str) -> str:
    return os.path.join(PACKAGE_FOLDER, f"{file}.py")

def logExecution(status: bool, executionTime: float, processId: str, package: str, args: dict):
    LOG_FILE = os.path.join(os.getcwd(), "execution.log")
    with open(LOG_FILE, "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if(status == True):
            prefix = f"Execution: {executionTime:.2f} sec"
        else:
            prefix = "STATUS: FALSE"

        log_entry = f"{timestamp} - {prefix} - Package: {package} - ProcessId: {processId} - Args: {args}\n"
        f.write(log_entry)