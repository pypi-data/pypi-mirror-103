## threedi-settings


Convert legacy model settings (V2) files to API V3 resources.


### Installation

To get all functionalities this package as to offer, install with all extras

    $ pip install threedi-settings[cmd, api]

### Usage

Before you hit it off make sure you have the following environment variables set correctly

```shell script
API_HOST=https://api.3di.live/v3.0  # no trailing slash
API_USERNAME=<your name goes here>
API_PASSWORD=<your password goes here>
```



Ths will give you access to the command line interface that let's you convert 3Di model settings to
3Di API resources. There are two flavors. Either use a model `*.ini` file as input or the `*.sqlite` file.

Both commands requires a `SIMULATION_ID` argument as settings can only be defined
on a per simulation basis in the API. That gives you much more flexibility to experiment
with different configurations.



#### Export from SQLITE database file

To use the settings that are stored in a 3Di model sqlite database file use the following command. Please note, that
all aggregation settings stored in the database also will be exported to the API V3. You can suppress this behaviour
through the `--no-aggregations` flag.


```shell script
export-settings export-from-sqlite --help
Usage: export-settings export-from-sqlite [OPTIONS] SIMULATION_ID SQLITE_FILE
                                          [SETTINGS_ROW]

  "Create API V3 settings resources from legacy model sqlite file"

Arguments:
  SIMULATION_ID   [required]
  SQLITE_FILE     SQLITE model file.  [required]
  [SETTINGS_ROW]  Specify the row id of the v2_global_settings entry you want
                  to export.  [default: 1]


Options:
  --aggregations / --no-aggregations
                                  If the '--no-aggregations' option is not
                                  explicitly set, the aggregation settings
                                  found in the sqlite file will be exported,
                                  too.  [default: True]

  --help                          Show this message and exit.
```

If you are unsure about the `SETTINGS_ROW` argument you can quickly list the existing rows in the database by running


```shell script
global-settings ls --help
Usage: global-settings ls [OPTIONS] SQLITE_FILE

  Shows id and name of existing global settings entries

Arguments:
  SQLITE_FILE  SQLITE model file.  [required]

Options:
  --help  Show this message and exit.
```

#### Export from ini (and aggregation) file

If you have access to the model ini file, and optionally to the corresponding aggregation file, you can use


```shell script
export-settings export-from-ini --help
Usage: export-settings export-from-ini [OPTIONS] SIMULATION_ID INI_FILE
                                       [AGGREGATION_FILE]

  "Create API V3 settings resources from legacy model ini file"

Arguments:
  SIMULATION_ID       [required]
  INI_FILE            Legacy model settings ini file.  [required]
  [AGGREGATION_FILE]  Legacy model aggregation settings file.

Options:
  --help  Show this message and exit.
```

#### Overview of the API V3 simulation settings fields

Most of the setting fields have been renamed in the API V3. To get an overview
of all available fields, their descriptions, suitable defaults etc use the
`describe-simulation-settings` command.

```shell script
describe-simulation-settings --help
Usage: describe-simulation-settings [OPTIONS]

  Shows all API V3 simulation settings fields, help texts on how to use
  them, suitable defaults, types etc.

Options:
  --help                          Show this message and exit.

```


### Internal Usage

This package is also used to retrieve simulation settings resources from the API to further
convert them to an internal format that the 3Di calculation core is able to read and process.

The package therefore can be installed without the extras mentioned above or a
single extra like `api` which will give you the `threedi-api-client` requirement
and therefore access to the http module.


* Free software: MIT license
* Documentation: https://threedi-settings.readthedocs.io.



#### Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.

