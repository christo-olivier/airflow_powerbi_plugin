# Power BI Plugin

This plugin is designed to allow you to perform operations against Microsoft Power BI.

## Hooks

The current Power BI Hook allows the following operations to take place against the Power BI REST API:

1. Get the refresh history for a datasource
1. Refresh a dataset

## Operators

At present the following operators are available:

1. PowerBIDatasetRefreshOperator

# Installation

In order to make use of the plugin copy the `powerbi_plugin` package in the root of the repository into 
the `$AIRFLOW_HOME/plugins` folder. If the `$AIRFLOW_HOME/plugins` folder does not exist then simply create it. 

Once you have completed your Airflow plugins folder should look like this

`$AIRFLOW_HOME/plugins/powerbi_plugin`  
`$AIRFLOW_HOME/plugins/powerbi_plugin/__init__.py`   
`$AIRFLOW_HOME/plugins/powerbi_plugin/hooks/__init__.py`   
`$AIRFLOW_HOME/plugins/powerbi_plugin/hooks/powerbi_hook.py`   
`$AIRFLOW_HOME/plugins/powerbi_plugin/operators/__init__.py`  
`$AIRFLOW_HOME/plugins/powerbi_plugin/operators/powerbi_dataset_refresh_operator.py`   

In order to use the hook and operator use the following imports:
- `from airflow.hooks.powerbi_plugin import PowerBIHook`
- `from airflow.operators.powerbi_plugin import PowerBIDatasetRefreshOperator`


