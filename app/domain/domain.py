from cleanstack.domain import BaseDomain, CommandHandler

from app.domain.context import ContextProtocol
from app.domain.dev.commands import (
    benchmark_command,
    custom_error_command,
    unexpected_domain_error_command,
    unexpected_error_command,
)
from app.domain.dummies.commands import get_dummies_command
from app.domain.posts.commands import (
    create_post_command,
    delete_post_command,
    get_post_command,
    get_posts_command,
    update_post_command,
)
from app.domain.users.commands import (
    authenticate_user_command,
    create_user_command,
    delete_user_command,
    get_user_command,
    get_users_command,
    update_user_command,
)


class Domain(BaseDomain[ContextProtocol]):
    get_posts = CommandHandler(get_posts_command)
    get_post = CommandHandler(get_post_command)
    create_post = CommandHandler(create_post_command)
    update_post = CommandHandler(update_post_command)
    delete_post = CommandHandler(delete_post_command)

    authenticate_user = CommandHandler(authenticate_user_command)
    get_users = CommandHandler(get_users_command)
    get_user = CommandHandler(get_user_command)
    create_user = CommandHandler(create_user_command)
    update_user = CommandHandler(update_user_command)
    delete_user = CommandHandler(delete_user_command)

    get_dummies = CommandHandler(get_dummies_command)

    benchmark = CommandHandler(benchmark_command)
    custom_error = CommandHandler(custom_error_command)
    unexpected_error = CommandHandler(unexpected_error_command)
    unexpected_domain_error = CommandHandler(unexpected_domain_error_command)
