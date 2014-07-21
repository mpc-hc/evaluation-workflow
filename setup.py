from setuptools import setup

setup(
    name='EvaluationWorkflow',
    description='A Trac workflow plugin for MPC-HC',
    version='1.0.2',
    url='https://github.com/mpc-hc/evaluation-workflow',
    download_url='https://github.com/mpc-hc/evaluation-workflow',
    license='MIT',
    author='Armada651 <Jules Blok>',
    author_email='jules.blok@gmail.com',
    zip_safe=True,
    platforms='any',
    packages=['evaluation'],
    entry_points={
        'trac.plugins': [
            'workflow = evaluation.workflow',
            'hider = evaluation.hider'
        ]
    }
)
