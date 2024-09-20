def boot(*args, **kwargs):
    # Trigger Pusher event (optional)
    safe_trigger('selenium-channel', 'process-started', {'message': 'Selenium process started'})

    try:
        # Get Selenium driver
        driver = get_selenium_driver()

        # Go to Google
        driver.get("https://www.google.com")

        # Find search box and type "Selenium"
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.send_keys("Selenium")
        search_box.submit()

        # Wait for results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search"))
        )

        # Get page title
        title = driver.title

        # Send result with Pusher
        safe_trigger('selenium-channel', 'search-completed', {
            'message': 'Search completed',
            'title': title
        })

        # Close the browser
        driver.quit()

        return {"status": "success", "title": title}

    except Exception as e:
        error_message = str(e)
        safe_trigger('selenium-channel', 'error-occurred', {
            'message': 'An error occurred',
            'error': error_message
        })
        raise  # Re-raise the error so it's recorded as a fatal error

if __name__ == "__main__":
    result = boot()
    print(result)