from pydantic import Field

from structs.schemas.base import BasePydanticModel


class Action(BasePydanticModel):
    action: str
    message: dict

    @property
    def asset_id(self):
        return self.message['assetId']


class SubscribeToAsset(BasePydanticModel):
    asset_id: int = Field(alias='assetId')


class SubscribeAction(Action):
    message: SubscribeToAsset

    @property
    def asset_id(self):
        return self.message.asset_id
