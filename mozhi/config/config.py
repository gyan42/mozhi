from dynaconf import Dynaconf

# Ref: https://github.surf/rochacbruno/learndynaconf

settings = Dynaconf(
    settings_files=[  # Paths or globs to any toml|yaml|ini|json|py
        'configs/settings.toml',
        'configs/.secrets.toml',
        'configs/datasets.toml',
        'configs/preprocessor.toml',
        'configs/models.toml'
    ],
    environments=True,  # Enable layered environments
    # (sections on config file for development, production, testing)
    load_dotenv=True,   # Load envvars from a file named `.env`
    # TIP: probably you don't want to load dotenv on production environments
    #  pass `load_dotenv={"when": {"env": {"is_in": ["development"]}}}
    dotenv_path="configs/.env",  # custom path for .env file to be loaded
    envvar_prefix="VF_ENV",  # variables exported as `VF_ENV_FOO=bar` becomes `settings.FOO == "bar"`
    env_switcher="ENV_FOR_VF",  # to switch environments `export ENV_FOR_VF=production`
)

