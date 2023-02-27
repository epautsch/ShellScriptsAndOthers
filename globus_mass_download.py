import os
import logging

import globus_sdk
from argparse import Namespace

from args import globus_mass, JIT_batch
import JIT_batch_json_commits


def make_transfer_client() -> globus_sdk.TransferClient:
    CLIENT_ID = 'c3a2f53f-046b-4f6d-92d8-81dc345a74f2'
    client = globus_sdk.NativeAppAuthClient(CLIENT_ID)

    client.oauth2_start_flow(refresh_tokens=True)
    authorize_url = client.oauth2_get_authorize_url()
    print(f'Please go to this URL and login:\n\n{authorize_url}\n')

    auth_code = input('Please enter the code you get after login here: ').strip()
    token_response = client.oauth2_exchange_code_for_tokens(auth_code)

    globus_transfer_data = token_response.by_resource_server['transfer.api.globus.org']

    transfer_rt = globus_transfer_data['refresh_token']
    transfer_at = globus_transfer_data['access_token']
    expires_at_s = globus_transfer_data['expires_at_seconds']

    authorizer = globus_sdk.RefreshTokenAuthorizer(
        transfer_rt, client, access_token=transfer_at, expires_at=expires_at_s
    )

    tc = globus_sdk.TransferClient(authorizer=authorizer)
    return tc


def transfer_data(tc: globus_sdk.TransferClient,
                  source_path: str,
                  dest_path: str,
                  source_endpoint_id: str,
                  dest_endpoint_id: str,
                  args: Namespace) -> None:
    endpoint_ls = tc.operation_ls(source_endpoint_id, path=source_path)
    files = [item for item in endpoint_ls if item['type'] == 'file' and item['size'] < (10 * 1024 * 1024 * 1024) - 37000000]

    for file in files:
        logging.info(f"Processing {file['name']}")
        print(file)

        task_data = globus_sdk.TransferData(source_endpoint=source_endpoint_id,
                                            destination_endpoint=dest_endpoint_id)
        task_data.add_item(
            os.path.join(source_path, file['name']),
            os.path.join(dest_path, file['name'])
        )
        result = tc.submit_transfer(task_data)

        task_id = result['task_id']
        minutes = 0
        while not tc.task_wait(task_id, timeout=60):
            minutes += 1
            print(f"{minutes} minute(s) have gone by since {task_id} has started")
        task = tc.get_task(task_id)
        if task['status'] == 'SUCCEEDED':
            logging.info(f"Transfer of {file['name']} succeeded")
            print(f"Transfer of {file['name']} completed successfully")
            JIT_batch_json_commits.main(args)
        else:
            logging.info(f"Transfer of {file['name']} failed")
            print(f"Transfer of {file['name']} failed")


def main():
    args_globus: Namespace = globus_mass()
    args_jit: Namespace = JIT_batch()
    JIT_batch_json_commits.make_dirs(args_jit.incoming)

    # log_file = os.path.join(args_globus.dest_path, 'transfer.log')
    log_file = '/home/epautsch/PTM-Torrent/globus_api_test/transfer.log'
    logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

    tc = make_transfer_client()

    print('My Endpoints: ')
    for ep in tc.endpoint_search(filter_scope='my-endpoints'):
        print('[{}] {}'.format(ep['id'], ep['display_name']))

    transfer_data(tc,
                  args_globus.source_path,
                  args_globus.dest_path,
                  args_globus.source_endpoint,
                  args_globus.dest_endpoint,
                  args_jit)


if __name__ == '__main__':
    main()
