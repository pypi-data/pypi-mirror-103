import asyncio
import json

import requests
from selenium import webdriver
from selenium.common.exceptions import JavascriptException
from selenium.webdriver import ActionChains
import chromedriver_binary
import websockets


ENVIRONMENTS = {
    'local': 'LOCAL',
    'cloud': 'DC',
    'unblockable': 'RESID',
}
FORMATS = {
    'json': 'json_format',
    'csv': 'csv_format',
}
OUTPUTS = set(['data', 'file'])
STARTING_LIMIT = 64
MAX_RESPONSE_THRESHOLD = 2 ** 20


class Client:
    def __init__(self, username, password, host='parsagon.io'):
        data = {'username': username, 'password': password}
        r = requests.post(f'https://{host}/api/accounts/token-auth/', data=data)
        if r.status_code != requests.codes.ok:
            self._display_errors(r)
        self.token = r.json()['token']
        self.host = host

    def _display_errors(response):
        errors = response.json()
        if 'non_field_errors' in errors:
            raise Exception(errors['non_field_errors'])
        else:
            raise Exception(errors)

    async def handle_driver(self, driver, result_id):
        async with websockets.connect(f'wss://{self.host}/ws/scrapers/results/{result_id}/client/') as websocket:
            async for message in websocket:
                message = json.loads(websocket.recv())
                convo_id = message['convo_id']
                response = 'OK'
                command = message['command']
                if command == 'get':
                    driver.get(message['url'])
                    await asyncio.sleep(2)
                elif command == 'mark':
                    elem_idx = driver.execute_script(f"let elemIdx = {message['elem_idx']}; for (const node of document.querySelectorAll(':not([data-parsagon-io-marked])')) {{ node.setAttribute('data-parsagon-io-marked', elemIdx); elemIdx++; }} return elemIdx;")
                    await websocket.send(json.dumps({'response': elem_idx, 'convo_id': convo_id}))
                    return
                elif command == 'scroll':
                    driver.execute_script("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});")
                    await asyncio.sleep(1)
                elif command == 'click':
                    actions = ActionChains(driver)
                    target = driver.find_element_by_xpath(f"//*[@data-parsagon-io-marked={message['target_id']}]")
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});", target)
                    await asyncio.sleep(0.5)
                    try:
                        actions.move_to_element(target).click().perform()
                        await asyncio.sleep(2)
                        driver.execute_script("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});")
                        await asyncio.sleep(1)
                    except JavascriptException:
                        pass
                elif command == 'inspect':
                    query = message['query']
                    if query == 'url':
                        response = driver.current_url
                    elif query == 'page_source':
                        response = driver.page_source
                    elif query == 'target_data':
                        target = driver.find_element_by_xpath(f"//*[@data-parsagon-io-marked={message['target_id']}]")
                        tag = target.tag_name
                        text = target.text
                        href = target.get_attribute('href')
                        url = driver.execute_script(f"return document.querySelector('[data-parsagon-io-marked=\"{message['target_id']}\"]').href;")
                        response = {'tag': tag, 'text': text, 'href': href, 'url': url}
                await websocket.send(json.dumps({'response': response, 'convo_id': convo_id}))

    async def get_result(self, result_id, format, output, file_path):
        headers = {'Content-Type': 'application/json', 'Authorization': f'Token {self.token}'}
        r = requests.post(f'https://{self.host}/api/scrapers/results/{result_id}/execute/', headers=headers)
        if r.status_code != requests.codes.ok:
            self._display_errors(r)
        while True:
            r = requests.get(f'https://{self.host}/api/scrapers/results/{result_id}/', headers=headers)
            if r.status_code != requests.codes.ok:
                self._display_errors(r)
            result_data = r.json()
            if result_data['status'] == 'FINISHED':
                break
            elif result_data['status'] == 'ERROR':
                raise Exception('A server error occurred. Please notify Parsagon.')
            await asyncio.sleep(5)

        if output == 'file':
            if format == 'csv':
                raise Exception("Output type 'file' not yet supported for format 'csv'")
            else:
                offset = 0
                limit = STARTING_LIMIT
                offset_incr = 0;
                max_response_size = 0
                r = requests.get(f'https://{self.host}/api/scrapers/results/{result_id}/download/?data_format={format}&offset={offset}&limit={limit}', headers=headers)
                if r.status_code != requests.codes.ok:
                    self._display_errors(r)
                result_data = r.json()
                offset_incr = len(result_data['result'])
                offset += offset_incr
                new_data = json.dumps(result_data)
                with open(file_path, 'w') as f:
                    f.write(new_data)
        else:
            r = requests.get(f'https://{self.host}/api/scraaprs/results/{result_id}/download/?data_format={format}',
                             headers=headers)
            if r.status_code != requests.codes.ok:
                self._display_errors(r)
            data = r.json()
            if format == 'csv':
                return data['result']
            else:
                return data

    def execute(scraper_name, urls, env, max_page_loads=1, format='json', output='data', file_path=''):
        if env not in ENVIRONMENTS:
            raise ValueError("Environment must be 'local', 'cloud', or 'unblockable'")
        if format not in FORMATS:
            raise ValueError("Format must be 'json' or 'csv'")
        if output not in OUTPUTS:
            raise ValueError("Output must be 'data' or 'file'")
        if output == 'file' and not file_path:
            raise ValueError("Output type is 'file' but no file path was given")

        headers = {'Content-Type': 'application/json', 'Authorization': f'Token {self.token}'}

        data = {'scraper_name': scraper_name, 'urls': urls, 'max_page_loads': max_page_loads}
        r = requests.post(f'https://{self.host}/api/scrapers/runs/', headers=headers, data=data)
        if r.status_code != requests.codes.ok:
            self._display_errors(r)
        run = r.json()

        if not run['scraper'][FORMATS[format]]:
            raise Exception(f'{format} format is unavailable for this scraper')

        data = {'environment': ENVIRONMENTS[env]}
        r = requests.post(f'https://{self.host}/api/scrapers/runs/{run["id2"]}/results/', headers=headers, data=data)
        if r.status_code != requests.codes.ok:
            self._display_errors(r)
        result = r.json()

        loop = asyncio.get_event_loop()
        if env == 'local':
            driver = webdriver.Chrome()
            asyncio.ensure_future(self.handle_driver(driver, result['id2']))
        return_value = loop.run_until_complete(self.get_result(result['id2'], format, output, file_path))
        if env == 'local':
            driver.quit()
        return return_value
