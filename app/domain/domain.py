from cleanstack.domain import BaseDomain, CommandHandler, QueryHandler

from app.domain.context import ContextProtocol
from app.domain.dev.commands import (
    benchmark_command,
    custom_error_command,
    unexpected_domain_error_command,
    unexpected_error_command,
)
from app.domain.dummies.commands import get_dummies_cached_command, get_dummies_command
from app.domain.posts.commands import (
    create_post_command,
    delete_post_command,
    get_post_command,
    get_posts_command,
    update_post_command,
)
from app.domain.users.commands import (
    get_user_by_provider_id_command,
    get_users_command,
)


class Domain(BaseDomain[ContextProtocol]):
    get_posts = QueryHandler(get_posts_command)
    get_post = QueryHandler(get_post_command)
    create_post = CommandHandler(create_post_command)
    update_post = CommandHandler(update_post_command)
    delete_post = CommandHandler(delete_post_command)

    get_user_by_provider_id = QueryHandler(get_user_by_provider_id_command)
    get_users = QueryHandler(get_users_command)

    get_dummies = QueryHandler(get_dummies_command)
    get_dummies_cached = QueryHandler(get_dummies_cached_command)

    benchmark = QueryHandler(benchmark_command)
    custom_error = QueryHandler(custom_error_command)
    unexpected_error = QueryHandler(unexpected_error_command)
    unexpected_domain_error = QueryHandler(unexpected_domain_error_command)
