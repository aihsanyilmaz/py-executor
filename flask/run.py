from flask import request, jsonify, current_app
import importlib.util
import threading
import requests
import os
from fatals import save_fatal_error
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def safe_trigger(app, channel, event, data):
    if app.pusher_client:
        app.pusher_client.trigger(channel, event, data)

def get_selenium_driver():
    return webdriver.Remote(
        command_executor='http://selenium-hub:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.CHROME
    )

def import_module_from_file(file_path):
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def run_function_in_background(process_id, file_path, args, kwargs, callback_url, app):
    try:
        module = import_module_from_file(file_path)
        # Gerekli fonksiyonları ve sınıfları modüle enjekte et
        module.safe_trigger = lambda channel, event, data: safe_trigger(app, channel, event, data)
        module.get_selenium_driver = get_selenium_driver
        module.By = By
        module.WebDriverWait = WebDriverWait
        module.EC = EC
        if hasattr(module, 'boot') and callable(module.boot):
            module.boot(*args, **kwargs)
        else:
            raise AttributeError("Modülde 'boot' fonksiyonu bulunamadı veya çağrılabilir değil.")
    except Exception as e:
        error_message = str(e)
        error_details = {
            "process_id": process_id,
            "error": error_message,
            "file": file_path,
            "args": args,
            "kwargs": kwargs
        }
        save_fatal_error(process_id, error_details)
        if callback_url:
            try:
                requests.post(callback_url, json=error_details)
            except requests.RequestException:
                pass

def run_function():
    data = request.json
    process_id = data.get('process_id')
    file_path = data.get('file_path')
    args = data.get('args', [])
    kwargs = data.get('kwargs', {})
    callback_url = data.get('callback_url')

    if not all([process_id, file_path]):
        return jsonify({"error": "process_id and file_path are required"}), 400

    full_file_path = os.path.join(os.getcwd(), file_path)
    if not os.path.exists(full_file_path):
        return jsonify({"error": "Specified file not found"}), 404

    threading.Thread(target=run_function_in_background, args=(
        process_id, full_file_path, args, kwargs, callback_url, current_app._get_current_object()
    )).start()

    return jsonify({"message": "Function is running in the background", "process_id": process_id}), 202
