API Usage Documentation
=======================

This API is designed to perform various operations. Authentication is required for all requests.

For Turkish version of this documentation, please see [README_TR.md](README_TR.md)

Authentication
--------------
The 'X-Auth-Hash' header is required for all requests. The value of this header must match the special hash provided to you.

Example:
X-Auth-Hash: your_secret_hash_here

Endpoints
---------

1. Application Status Check
   URL: /
   Method: GET
   Description: Checks if the application is running.
   Return: "Hello, Flask application is running!"

2. Function Execution
   URL: /run
   Method: POST
   Description: Executes the 'boot' function in the specified file.
   Required Fields:
     - process_id: A unique identifier for the process
     - file_path: Path to the file to be executed
   Optional Fields:
     - args: List of arguments to be sent to the function
     - kwargs: Dictionary of keyword arguments to be sent to the function
     - callback_url: URL to send notification in case of an error
   Example Request Body:
   {
     "process_id": "12345",
     "file_path": "packages/example.py",
     "args": [1, 2, 3],
     "kwargs": {"param1": "value1"},
     "callback_url": "http://example.com/callback"
   }
   Return: A message indicating that the process has started and the process_id

3. Listing Fatal Errors
   URL: /fatals
   Method: GET
   Description: Lists all saved fatal error files.
   Return: List of fatal error files

4. Fatal Error Details
   URL: /fatals/<filename>
   Method: GET
   Description: Shows the content of the specified fatal error file.
   Return: JSON data containing error details

5. Deleting Fatal Error Record
   URL: /fatals/<filename>
   Method: DELETE
   Description: Deletes the specified fatal error file.
   Return: 
     If successful: A message indicating that the deletion was successful
     If unsuccessful: Error message

Error Codes
-----------
- 400 Bad Request: Required fields are missing or incorrect
- 401 Unauthorized: Authentication failed
- 404 Not Found: Requested resource not found
- 500 Internal Server Error: An error occurred on the server side

Notes
-----
- All requests and responses are in JSON format.
- In case of an error, the error message is returned in the 'error' field.
- The '/run' endpoint operates asynchronously. The process starts immediately and control is returned.
- Fatal errors are stored as .txt files in the 'fatals' directory.
- Fatal error records can be deleted with a DELETE request, but this action cannot be undone.
- Real-time notifications can be sent using Pusher in the executed files.

Using Pusher
------------
Pusher can be used within the executed files. This is useful for sending real-time notifications.

Example of Pusher Usage:
Pusher can be used in the executed Python file as follows:

```
def boot(*args, **kwargs):
    # Trigger Pusher event
    safe_trigger('my-channel', 'my-event', {'message': 'Process started'})
    
    # Main functionality goes here
    # ...

    # Trigger another event when the process is completed
    safe_trigger('my-channel', 'process-completed', {'message': 'Process completed'})
```

The `safe_trigger` function checks if the Pusher client is available and safely triggers the event. This function is automatically injected, so it can be used directly.

Parameters:
- First parameter: Channel name
- Second parameter: Event name
- Third parameter: Data to be sent (in dict format)

Note: Pusher usage is optional. If Pusher is not configured, `safe_trigger` calls will be silently ignored and will not cause an error.

Using Selenium
--------------
Selenium can be used in the executed files to perform operations in a remote browser. Necessary imports and driver creation function for Selenium are automatically provided.

Example of Selenium Usage:
Selenium can be used in the executed Python file as follows:

```
def boot(*args, **kwargs):
    driver = get_selenium_driver()
    
    driver.get("https://www.example.com")
    title = driver.title
    
    driver.quit()
    
    return {"status": "success", "title": title}
```

Available Selenium Elements:
- get_selenium_driver(): Returns a Selenium WebDriver object
- By: Selenium's By class
- WebDriverWait: Selenium's WebDriverWait class
- EC: Selenium's expected_conditions module

Note:
- Connection to Selenium Hub is automatically configured.
- Always call driver.quit() after completing operations to close the browser.
- It is recommended to use try-except blocks for error handling.
