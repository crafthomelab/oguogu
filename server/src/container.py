from dependency_injector import containers, providers
from src.registry.container import RegistryContainer



class AppContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["src.routers"]
    )
    
    registry = providers.Container(RegistryContainer)
