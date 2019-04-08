import time
from airflow.operators import BaseOperator
from airflow.utils.decorators import apply_defaults
from powerbi_plugin.hooks.powerbi_hook import PowerBIHook


class PowerBIDatasetRefreshOperator(BaseOperator):
    """
    Refreshes a Power BI dataset.

    If no `group id` is specified then the dataset from "My Workspace" will
    be refreshed.

    By default the operator will wait until the refresh has completed before
    exiting. The refresh status is checked every 60 seconds as a default. This
    can be changed by specifying a new value for `recheck_delay`.

    :param client_id: Power BI App ID used to identify the application
        registered to have access to the REST API.
    :param dataset_key: The dataset id.
    :param group_id: The workspace id.
    :param wait_for_completion: Wait until the refresh completes before exiting.
    :param recheck_delay: Number of seconds to wait before rechecking the
        refresh status.
    :param powerbi_conn_id: Airflow Connection ID that contains the connection
        information for the Power BI account used for authentication.
    """
    template_fields = []
    template_ext = []
    ui_color = '#e4f0e8'

    @apply_defaults
    def __init__(self,
                 client_id: str,
                 dataset_key: str,
                 group_id: str = None,
                 wait_for_completion: bool = True,
                 recheck_delay: int = 60,
                 powerbi_conn_id: str = 'powerbi_default',
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.dataset_key = dataset_key
        self.group_id = group_id
        self.wait_for_completion = wait_for_completion
        self.recheck_delay = recheck_delay
        self.powerbi_conn_id = powerbi_conn_id
        self.hook = None

    def get_refresh_status(self) -> str:
        """
        Get the refresh status of the most recent dataset refresh in the
        refresh history of the data source.

        :return: str value of 'Completed`, `NoHistory` or `Unknown`
        """
        history = self.hook.get_refresh_history(dataset_key=self.dataset_key,
                                                group_id=self.group_id,
                                                top=1)
        value = history.get('value')

        if not value:
            return 'NoHistory'
        else:
            return value[0].get('status')

    def wait_on_completion(self) -> None:
        """
        Wait until the dataset refresh has completed.
        """
        while True:
            time.sleep(self.recheck_delay)
            status = self.get_refresh_status()
            self.log.info(f'Checking refresh status. Status is `{status}`')
            if status == 'Completed':
                self.log.info('Refresh completed.')
                break

    def execute(self, context):
        """
        Refresh the Power BI Dataset
        """
        if not self.hook:
            self.hook = PowerBIHook(client_id=self.client_id,
                                    powerbi_conn_id=self.powerbi_conn_id)

        # Check to see if a refresh is already in progress
        # Power BI only allows one refresh to take place and will raise
        # an exception if the API is called when a refresh is already in
        # progress. We wait until any existing refreshes are completed
        # before starting a new one.
        self.log.info('Check if a refresh is already in progress.')
        status = self.get_refresh_status()

        if status == 'Unknown':
            self.log.info(
                'Waiting for pre-existing refresh to complete before starting.'
            )
            self.wait_on_completion()
            self.log.info('Pre-existing refresh completed.')

        # Start dataset refresh
        self.log.info('Starting refresh.')
        self.hook.refresh_dataset(dataset_key=self.dataset_key,
                                  group_id=self.group_id)

        if self.wait_for_completion:
            self.wait_on_completion()
