"""Finance Database Command Router."""
from openbb_core.app.model.command_context import CommandContext
from openbb_core.app.model.obbject import OBBject
from openbb_core.app.provider_interface import (
    ExtraParams,
    ProviderChoices,
    StandardParams,
)
from openbb_core.app.query import Query
from openbb_core.app.router import Router
from pydantic import BaseModel

router = Router(prefix="")

# pylint: disable=unused-argument


@router.command(model="ETFSearch")
def etf(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject[BaseModel]:
    """Search for ETFs."""
    return OBBject(results=Query(**locals()).execute())


@router.command(model="StockSearch")
def equity(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject[BaseModel]:
    """Search for Equities."""
    return OBBject(results=Query(**locals()).execute())


@router.command(model="CryptoSearch")
def crypto(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject[BaseModel]:
    """Search for cryptocurrencies."""
    return OBBject(results=Query(**locals()).execute())
