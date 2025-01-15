from dependency_injector import containers, providers

from src.database.container import DataBaseContainer
from src.registry.challenge import ChallengeRegistryService
from src.registry.grader import ActivityGrader
from src.registry.activity import ActivityRegistryService
from src.registry.reward import ChallengeRewardService
from src.registry.transaction import TransactionManager
from src.settings import Settings

class RegistryContainer(containers.DeclarativeContainer):
    database = providers.Container(DataBaseContainer)    
    settings = providers.Singleton(Settings)
    
    transaction = providers.Singleton(TransactionManager, 
                                     settings=settings)
    
    grader = providers.Singleton(ActivityGrader, 
                                 settings=settings)
    
    registry = providers.Singleton(ChallengeRegistryService, 
                                   repository=database.repository,
                                   transaction=transaction)
    
    activity = providers.Singleton(ActivityRegistryService, 
                                   repository=database.repository,
                                    transaction=transaction,
                                    grader=grader)

    reward = providers.Singleton(ChallengeRewardService, 
                                 repository=database.repository,
                                 transaction=transaction)
