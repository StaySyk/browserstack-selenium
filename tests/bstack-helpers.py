import json

def mark_session_name(driver, test_name):
    executor_object = {
        'action': 'setSessionName',
        'arguments': {
            'name': test_name
        }
    }
    browserstack_executor = 'browserstack_executor: {}'.format(json.dumps(executor_object))
    driver.execute_script(browserstack_executor)

def mark_test_status(driver, status, reason):
    executor_object = {
        'action': 'setSessionStatus',
        'arguments': {
            'status': status,  # "passed" or "failed"
            'reason': reason
        }
    }
    browserstack_executor = 'browserstack_executor: {}'.format(json.dumps(executor_object))
    driver.execute_script(browserstack_executor)
