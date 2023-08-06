from bergen.schema import DataPoint
from bergen.wards.graphql.aiohttp import AIOHttpGraphQLWard
from bergen.auths.base import BaseAuthBackend
from typing import Callable, Dict
from bergen.enums import DataPointType
from bergen.clients.base import BaseWard
import logging
import asyncio
from bergen.console import console
logger = logging.getLogger(__name__)

datapointregistry = None

class DataPointRegistry(object):


    def __init__(self) -> None:
        self.pointIDPointMap: Dict[str, DataPoint] = {}
        self.pointIDWardMap: Dict[str, BaseWard] = {}
        self.pointIDNegotiationMap: Dict[str, BaseWard] = {}


        self.builders =  {
                # Default Builders for standard
                DataPointType.GRAPHQL: lambda datapoint, bergen: AIOHttpGraphQLWard(host=datapoint.outward, port=datapoint.port, token=bergen.auth.getToken(), protocol="http", loop=bergen.loop, needs_negotiation=datapoint.needsNegotiation)
        }

    def registerClientBuilder(self, type:str , builder: Callable):
        self.builders[type] = builder

    def createWardForDatapoint(self, point, bergen) -> BaseWard:


        if point.id in self.pointIDWardMap:
            return self.pointIDWardMap[point.id]

        logger.info(f"Creating new Ward for Datapoint {point}")


        if point.type in self.builders:
            builder = self.builders[point.type]
            self.pointIDWardMap[point.id]  = builder(point, bergen)
            self.pointIDPointMap[point.id]  = point

            return self.pointIDWardMap[point.id]
        else:
            raise NotImplementedError(f"We have no idea how to build the ward for this Datapoint {point.type}")

    async def configureWards(self):
        wards = [ward for id, ward in self.pointIDWardMap.items()]
        names = [point.app.name for id, point in self.pointIDPointMap.items()]
        await asyncio.gather(*[ward.configure() for ward in wards])

        negotiation_results = await asyncio.gather(*[ward.negotiate() for ward in wards])
        extensions =  {name: result for name, result in zip(names, negotiation_results)}
        return extensions





def get_datapoint_registry() -> DataPointRegistry:
    global datapointregistry
    if datapointregistry is None:
        datapointregistry = DataPointRegistry()
    return datapointregistry