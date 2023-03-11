from collections.abc import Callable

from bookkeeper.repository.abstract_repository import Model, AbstractRepository

def repository_factory(repo_type: type, db_file=None) -> Callable[[Model], AbstractRepository]:
    if db_file is None:
        def repo_gen(model: Model) -> AbstractRepository:
            return repo_type[model]()
        return repo_gen
    else:
        def repo_gen(model: Model) -> AbstractRepository:
            return repo_type[model](db_file=db_file, cls=model)
        return repo_gen