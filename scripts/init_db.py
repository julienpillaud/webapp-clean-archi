from cleanstack.sql.entities import OrmEntity

from app.core.config import Settings
from app.infrastructure.sql.models import (  # noqa
    OrmItem,
    OrmPost,
    OrmTag,
    OrmUser,
    post_tag,
)
from app.infrastructure.sql.resource import SQLEngine


def main() -> None:
    settings = Settings(postgres_params={"echo": True})
    resource = SQLEngine.from_settings(settings)
    OrmEntity.metadata.drop_all(resource.engine)
    OrmEntity.metadata.create_all(resource.engine)


if __name__ == "__main__":
    main()
