from setuptools import setup

setup(
    name='EvaluationWorkflow', version='1.0',
    packages=['evaluation'],
    entry_points={
        'trac.plugins': [
            'workflow = evaluation.workflow',
            'hider = evaluation.hider',
        ],
    },
)
