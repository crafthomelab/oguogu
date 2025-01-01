from dependency_injector import containers, providers

from src.database.repository import ChallengeRepository
from src.settings import Settings
from src.database.database import SessionManager

class DataBaseContainer(containers.DeclarativeContainer):
    settings = providers.Singleton(Settings)

    session_manager = providers.Singleton(SessionManager, settings=settings)
    
    repository = providers.Singleton(
        ChallengeRepository, 
        session_factory=session_manager.provided.session
    )