
from kombu import Queue


from adsdata import app as app_module

app = app_module.ADSDataPipelineCelery('data-pipeline')


app.conf.CELERY_QUEUES = (
    Queue('process-bibcodes', app.exchange, routing_key='process-bibcodes'),
    Queue('output-nonbib', app.exchange, routing_key='output-nonbib'),
    Queue('output-metrics', app.exchange, routing_key='output-metrics')
)


@app.task(queue='process-bibcodes')
def task_process_bibcodes(bibcodes):
    """accepts an order list of bibcodes"""
    from adsdata import process
    process.process_bibcodes(bibcodes, compute_metrics=True)


@app.task(queue='output-nonbib')
def task_output_nonbib(msg):
    """
    This worker will forward results to the outside
    exchange (typically an ADSMasterPipeline) to be
    incorporated into the storage
    :param msg: a protobuf containing the non-bibliographic metadata
            {'bibcode': '....',
             'reads': [....],
             'simbad': '.....',
             .....
            }
    :return: no return
    """
    app.logger.debug('Will forward this nonbib record: %s', msg)
    app.forward_message(msg)


@app.task(queue='output-metrics')
def task_output_metrics(msg):
    """
    This worker will forward metrics to the outside
    exchange (typically an ADSMasterPipeline) to be
    incorporated into the storage
    :param msg: a protobuf containing the metrics record
            {'bibcode': '....',
             'downloads': [....],
             'citations': [.....],
             .....
            }
    :return: no return
    """
    app.logger.debug('Will forward this metrics record: %s', msg)
    app.forward_message(msg)



if __name__ == '__main__':
    app.start()
