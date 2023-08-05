from typing import Dict
from typing import List
from typing import Tuple

from slyce.client.abstract import AbstractSlyceClient
from slyce.credentials import SlyceCredentials


class SlyceAccountClient(AbstractSlyceClient):
    """ Client for calling Slyce API
    """

    def __init__(self, credentials: SlyceCredentials, **kwargs):
        """
        Args:
            credentials (SlyceCredentials): Slyce credentials.
            fingerprint (str, optional): Unique identifier for the instance of this library.

        Raises:
            InvalidCredentials: If missing or invalid credentials.
        """
        super().__init__(credentials, **kwargs)

    @property
    def _account_id(self):
        return self._credentials.account_id

    @property
    def _space_id(self):
        return self._credentials.space_id

    async def execute_workflow(self,
                               workflow_id: str,
                               *,
                               image_id: str = None,
                               language_code: str = None,
                               country_code: str = None,
                               anchor: Tuple[int, int] = None,
                               roi: List[Tuple[int, int]] = None,
                               options: Dict = None,
                               **kwargs) -> Dict:

        """Execute a workflow.

        Args:
            workflow_id(str): ID of the workflow.
            image_id(str, optional): ID of the image to use in the workflow.
            language_code(str, optional): Language code to use in the workflow.
            country_code(str, optional): Country code to use in the workflow.
            anchor(Tuple[int, int], optional): Anchor point in reference to image.
            roi(List[Tuple[int, int]], optional): Region of interest, as points, in reference to image.
            options(Dict, optional): Any options to be passed into the workflow at runtime.

        Raises:
            ExecuteWorkflowError

        Returns:
            Dict: Workflow Execution Response object.
        """

        return await super().execute_workflow(
            self._account_id,
            self._space_id,
            workflow_id,
            image_id=image_id,
            language_code=language_code,
            country_code=country_code,
            anchor=anchor,
            roi=roi,
            options=options,
            **kwargs
        )

    async def upload_image(self, filepath: str = None, *, url: str = None, **kwargs) -> str:
        """Upload an image.

        Args:
            filepath (str): Path to the image file.
            url (str): URL of ther image file.
        Raises:
            ValueError
            FileNotFoundError
            UploadImageError
        Returns:
            str: The ID of the uploaded image.
        """

        return await super().upload_image(self._account_id, filepath=filepath, url=url, **kwargs)
