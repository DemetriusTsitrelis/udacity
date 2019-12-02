from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 tests_results=[],
                 retries = 3,
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id,
        self.tests_results = tests_results
        self.retries = retries
        

    def execute(self, context):
        redshift_hook = PostgresHook(self.redshift_conn_id)
        for test, expected_result in self.tests_results:
            passed_test = False
            for i in range(self.retries):
                self.log.info(f"Running test: {test}")
                test_result = redshift_hook.get_records(test)
                if test_result == expected_result:
                    passed_test = True
                    break
                    
            if not passed_test:
                err_message = f"Data quality test failed: {test}"
                self.log.error(err_message)
                raise ValueError(err_message)
                    
        self.log.info("DataQualityOperator tests succeeded")
