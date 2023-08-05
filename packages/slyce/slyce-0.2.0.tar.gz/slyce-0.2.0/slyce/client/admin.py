from typing import Dict

from slyce.client.abstract import AbstractSlyceClient


class SlyceAdminClient(AbstractSlyceClient):
    async def execute_weld(self,
                           account_id: str,
                           space_id: str,
                           weld_statement: str,
                           *_,
                           **kwargs) -> Dict:
        kwargs['weld_statement'] = weld_statement
        return await self._execute_workflow(account_id, space_id, **kwargs)

    async def execute_weld_from_file(self,
                                     account_id: str,
                                     space_id: str,
                                     weld_filepath: str,
                                     *_,
                                     **kwargs) -> Dict:
        with open(weld_filepath, 'r') as f:
            return await self.execute_weld(account_id, space_id, f.read(), **kwargs)
