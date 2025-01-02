from dependency_injector import containers, providers

from src.database.container import DataBaseContainer
from src.registry.challenge import ChallengeRegistryService
from src.settings import Settings

class RegistryContainer(containers.DeclarativeContainer):
    settings = providers.Singleton(Settings)
    
    database = providers.Dependency(DataBaseContainer)
    
    registry = providers.Singleton(ChallengeRegistryService, 
                                   repository=database.repository,
                                   settings=settings)
