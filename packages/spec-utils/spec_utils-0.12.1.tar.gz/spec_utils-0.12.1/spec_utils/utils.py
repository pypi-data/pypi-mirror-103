from concurrent.futures import ThreadPoolExecutor, as_completed


def fetch(client, method: str, params: dict = {}):
    """ Execute method of a client with recived parameters """
    method = getattr(client, method)
    return method(**params)


def bulk_get_pages(client, method, params: dict = {}, \
        page_range: tuple = (1, 2), max_workers: int = 100, **kwargs) -> list:
    """ Get a range of pages of a client simultaneously. """

    # structures prepare
    responses = []
    processes = []
    params_ = params
    
    # create executor context
    with ThreadPoolExecutor(max_workers=max_workers) as executor:

        # processes prepare
        for i in range(*page_range):
            params_["params"]["page"] = i
            processes.append(
                executor.submit(
                    fetch,
                    client=client,
                    method=method,
                    params=params_
                )
            )
        
        # execute and put result in out structure
        [responses.append(r_.result()) for r_ in as_completed(processes)]

        # close executor
        executor.shutdown(wait=True)

    # return responses
    # list of pages result
    return responses
