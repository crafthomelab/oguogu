from dependency_injector import containers, providers

from src.settings import Settings
from src.storage.repository import ObjectRepository

class StorageContainer(containers.DeclarativeContainer):
    settings = providers.Singleton(Settings)
    
    repository = providers.Singleton(
        ObjectRepository, 
        settings=settings
    )