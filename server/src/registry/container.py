from dependency_injector import containers, providers

from src.database.container import DataBaseContainer
from src.registry.challenge import ChallengeRegistryService
from src.registry.proof import ProofRegistryService
from src.registry.transaction import TransactionManager
from src.settings import Settings

class RegistryContainer(containers.DeclarativeContainer):
    settings = providers.Singleton(Settings)
    
    database = providers.Dependency(DataBaseContainer)

    transaction = providers.Singleton(TransactionManager, 
                                     settings=settings)
        
    registry = providers.Singleton(ChallengeRegistryService, 
                                   repository=database.repository,
                                   settings=settings)
    
    proof = providers.Singleton(ProofRegistryService, 
                                repository=database.repository,
                                settings=settings)

