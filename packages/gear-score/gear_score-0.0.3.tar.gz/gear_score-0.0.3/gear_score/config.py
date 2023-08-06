from pydantic import BaseSettings

import gear_score


class Settings(BaseSettings):
    use_local_db: bool = True
    public_db_hosts: list = ("https://wotlk.ezhead.org", "https://wotlkdb.com")
    db_dsn = f'sqlite+aiosqlite:///{gear_score.__name__}.sqlite'
    http_request_timeout = 5

    class Config:
        env_prefix = 'gs'


settings = Settings()
