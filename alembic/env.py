from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

#from app.models.user import User, BlacklistedUser
# from app.models.user import User, BlacklistedUser
# from app.models.category import PostCategory, PostCategories
# from app.models.comment import Comment
# from app.models.post import Post, PostView, PostVote
# from app.models.sections import Section
# from app.db.session import Base, engine
# from app.core.config import settings

from BlogFastAPI.app.models.user import User, BlacklistedUser
from BlogFastAPI.app.models.category import PostCategory, PostCategories
from BlogFastAPI.app.models.comment import Comment
from BlogFastAPI.app.models.post import Post, PostView, PostVote
from BlogFastAPI.app.models.sections import Section
from BlogFastAPI.app.db.session import Base, engine
from BlogFastAPI.app.core.config import settings


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata


config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
