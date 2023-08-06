from pydantic import BaseSettings

import gear_score


class Settings(BaseSettings):
    use_local_db: bool = True
    public_db_url: str = "https://wotlk.ezhead.org"
    db_dsn = f'sqlite+aiosqlite:///{gear_score.__name__}.sqlite'

    class Config:
        env_prefix = 'gs'


settings = Settings()
