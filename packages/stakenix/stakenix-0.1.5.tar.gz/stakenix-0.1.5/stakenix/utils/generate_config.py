from pathlib import Path
from yaml import safe_dump


def generate_config() -> None:
    config = {
        "sql": {
            "mysql": {
                "driver": {
                    "name": "mysql+mysqlconnector",
                    "connection_args": {}
                },
                "databases": {
                    "default": {
                        "host": "place_for_host",
                        "port": "place_for_port",
                        "username": "place_for_username",
                        "password": "place_for_password",
                    },
                    "lucky_partners": {
                        "host": "place_for_host",
                        "port": "place_for_port",
                        "username": "place_for_username",
                        "password": "place_for_password",
                    }
                },
            },
            "postgresql": {
                "driver": {
                    "name": "postgresql",
                    "connection_args": {
                        "options": "-csearch_path={}"
                    }
                },
                "databases": {
                    "default": {
                        "host": "place_for_host",
                        "port": "place_for_port",
                        "username": "place_for_username",
                        "password": "place_for_password",
                        "database_name": "analyst_db"
                    }
                },
            },
            "clickhouse": {
                "driver": {
                    "name": "clickhouse",
                    "connection_args": {}
                },
                "databases": {
                    "default": {
                        "host": "place_for_host",
                        "port": "place_for_port",
                        "username": "place_for_username",
                        "password": "place_for_username",
                    }
                },
            },
            "mssql": {
                "driver": {
                    "name": "mssql",
                    "connection_args": {
                        "driver": "ODBC+Driver+17+for+SQL+Server"
                    }
                },
                "databases": {
                    "default": {
                        "host": "place_for_host",
                        "port": "place_for_port",
                        "username": "place_for_username",
                        "password": "place_for_password",
                        "database_name": "BPMonline7102CustomerCenterSoftkeyRUS_1453921_0613"
                    }
                },
            },
        },
        "nosql": {
            "mongodb": {
                "databases": {
                    "pobeda": {
                        "database_name": "pobeda",
                        "host": "place_for_host",
                        "username": "place_for_username",
                        "password": "place_for_password",
                        "ssh_host": "place_for_ssh_host",
                        "ssh_username": "place_for_username",
                    },
                    "lara": {
                        "database_name": "lotoru",
                        "host": "place_for_host",
                        "username": "place_for_username",
                        "password": "place_for_password",
                        "ssh_host": "place_for_ssh_host",
                        "ssh_username": "place_for_username",
                    },
                    "vipt": {
                        "database_name": "vipt",
                        "host": "place_for_host",
                        "username": "place_for_username",
                        "password": "place_for_password",
                        "ssh_host": "place_for_ssh_host",
                        "ssh_username": "place_for_username",
                    },
                    "mk5": {
                        "database_name": "mk5",
                        "host": "place_for_host",
                        "username": "place_for_username",
                        "password": "place_for_password",
                        "ssh_host": "place_for_ssh_host",
                        "ssh_username": "place_for_username",
                    },
                    "vipclub": {
                        "database_name": "vipclub",
                        "host": "place_for_host",
                        "username": "place_for_username",
                        "password": "place_for_password",
                        "ssh_host": "place_for_ssh_host",
                        "ssh_username": "place_for_username",
                    },
                }
            }
        },
        "grafana": {
            "url": "place_for_url",
            "headers": {
                "Authorization": "place_for_header",
                "Content-Type": "place_for_header",
                "Accept": "place_for_header",
            },
        }
    }

    path = Path.home().joinpath(".stakenix")
    config_path = path.joinpath("config.yaml")

    if not path.exists():
        path.mkdir()

    with open(config_path, "w") as file:
        safe_dump(config, file, sort_keys=False)
    
    print("Config successfully generated")
    print(f"Path to config: {config_path}")


if __name__ == "__main__":
    generate_config()