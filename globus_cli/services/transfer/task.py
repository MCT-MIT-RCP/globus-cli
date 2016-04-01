from __future__ import print_function
import json

from globus_sdk import TransferClient

from globus_cli.helpers import outformat_is_json, cliargs, CLIArg
from globus_cli.services.transfer.helpers import (
    print_json_from_iterator, text_header_and_format)


@cliargs('List Tasks for the current user', [])
def task_list(args):
    """
    Executor for `globus transfer task-list`
    """
    client = TransferClient()

    task_iterator = client.task_list(num_results=10,
                                     filter='type:TRANSFER,DELETE')

    if outformat_is_json(args):
        print_json_from_iterator(task_iterator)
    else:
        text_col_format = text_header_and_format(
            [(36, 'Task ID'), (10, 'Status'), (10, 'Type'),
             (32, 'Source Display Name'), (32, 'Dest Display Name'),
             (None, 'Label')])

        for result in task_iterator:
            print(text_col_format.format(
                result.data['task_id'], result.data['status'],
                result.data['type'],
                result.data['source_endpoint_display_name'],
                result.data['destination_endpoint_display_name'],
                result.data['label']))


@cliargs('List Events for a given Task', [
    CLIArg('task-id', required=True,
           help='ID of the task for which you want to list events')
    ])
def task_event_list(args):
    """
    Executor for `globus transfer task-event-list`
    """
    client = TransferClient()

    event_iterator = client.task_event_list(args.task_id)

    if outformat_is_json(args):
        print_json_from_iterator(event_iterator)
    else:
        text_col_format = text_header_and_format(
            [(25, 'Time'), (32, 'Code'), (8, 'Is Error'), (None, 'Details')])

        for result in event_iterator:
            print(text_col_format.format(
                result.data['time'], result.data['code'],
                result.data['is_error'], result.data['details']))


@cliargs('Cancel a specific task, owned by the current user', [
    CLIArg('task-id', required=True,
           help='ID of the task which you want to cancel')
    ])
def cancel_task(args):
    """
    Executor for `globus transfer task cancel`
    """
    client = TransferClient()

    res = client.cancel_task(args.task_id)

    if outformat_is_json(args):
        print(json.dumps(res.data, indent=2))
    else:
        print(res.data['message'])


@cliargs('Update label and/or deadline on an active task', [
    CLIArg('task-id', required=True,
           help='ID of the task which you want to cancel'),
    CLIArg('label', default=None, help='New Label for the Task'),
    CLIArg('deadline', default=None, help='New Deadline for the Task')
    ])
def update_task(args):
    """
    Executor for `globus transfer task update`
    """
    client = TransferClient()

    task_doc = {
        'DATA_TYPE': 'task'
    }

    if args.label:
        task_doc['label'] = args.label
    if args.deadline:
        task_doc['deadline'] = args.deadline

    res = client.update_task(args.task_id, task_doc)

    if outformat_is_json(args):
        print(json.dumps(res.data, indent=2))
    else:
        print('Success')


@cliargs('Show detailed information about a specific task', [
    CLIArg('task-id', required=True,
           help='ID of the task which you want to examine')
    ])
def show_task(args):
    """
    Executor for `globus transfer task show`
    """
    client = TransferClient()

    res = client.get_task(args.task_id)

    print(json.dumps(res.data, indent=2))


@cliargs('Show detailed info about pause rules that are applied to a task', [
    CLIArg('task-id', required=True, help='ID of the task')
    ])
def task_pause_info(args):
    """
    Executor for `globus transfer task pause-info`
    """
    client = TransferClient()

    res = client.task_pause_info(args.task_id)

    print(json.dumps(res.data, indent=2))