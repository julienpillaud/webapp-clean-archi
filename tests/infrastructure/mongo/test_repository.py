from app.domain.entities import DEFAULT_PAGINATION_LIMIT
from app.domain.generics.entities import GenericEntity
from app.infrastructure.mongo.generics import GenericEntityMongoRepository
from tests.fixtures.factories.generics import GenericEntityMongoFactory


def test_get_all(
    generic_entity_mongo_factory: GenericEntityMongoFactory,
    generic_entity_mongo_repository: GenericEntityMongoRepository,
) -> None:
    # Arrange
    number_of_entity = 5
    generic_entity_mongo_factory.create_many(number_of_entity)

    # Act
    result = generic_entity_mongo_repository.get_all()

    # Assert
    assert result.total == number_of_entity
    assert result.limit == DEFAULT_PAGINATION_LIMIT
    assert len(result.items) == number_of_entity


def test_get_by_id(
    generic_entity_mongo_factory: GenericEntityMongoFactory,
    generic_entity_mongo_repository: GenericEntityMongoRepository,
) -> None:
    # Arrange
    entity = generic_entity_mongo_factory.create_one()
    assert entity.id is not None

    # Act
    result = generic_entity_mongo_repository.get_by_id(entity.id)

    # Assert
    assert result is not None
    assert result.id == entity.id
    assert result.name == entity.name


def test_get_by_id_not_found(
    generic_entity_mongo_repository: GenericEntityMongoRepository,
) -> None:
    # Act
    entity_id = "123456789012345678901234"
    result = generic_entity_mongo_repository.get_by_id(entity_id)

    # Assert
    assert result is None


def test_create(
    generic_entity_mongo_repository: GenericEntityMongoRepository,
) -> None:
    # Arrange
    entity = GenericEntity(id=None, name="Test Entity")

    # Act
    result = generic_entity_mongo_repository.create(entity)

    # Assert
    assert result.id is not None
    assert result.name == entity.name


def test_update(
    generic_entity_mongo_factory: GenericEntityMongoFactory,
    generic_entity_mongo_repository: GenericEntityMongoRepository,
) -> None:
    # Arrange
    entity = generic_entity_mongo_factory.create_one()
    assert entity.id is not None

    entity.name = "Updated Entity"

    # Act
    result = generic_entity_mongo_repository.update(entity)

    # Assert
    assert result.id == entity.id
    assert result.name == entity.name


def test_delete(
    generic_entity_mongo_factory: GenericEntityMongoFactory,
    generic_entity_mongo_repository: GenericEntityMongoRepository,
) -> None:
    # Arrange
    entity = generic_entity_mongo_factory.create_one()
    assert entity.id is not None

    # Act
    generic_entity_mongo_repository.delete(entity)

    # Assert
    result = generic_entity_mongo_repository.get_by_id(entity.id)
    assert result is None
