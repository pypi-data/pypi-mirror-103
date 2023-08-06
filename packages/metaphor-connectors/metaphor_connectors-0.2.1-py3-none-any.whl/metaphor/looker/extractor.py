import logging
import os
from dataclasses import dataclass
from typing import List

import looker_sdk
from looker_sdk.sdk.api31.methods import Looker31SDK

from metaphor.common.event_util import EventUtil
from metaphor.common.extractor import BaseExtractor, RunConfig
from metaphor.common.metadata_change_event import (
    AspectType,
    Dashboard,
    DashboardInfo,
    DashboardLogicalID,
    DashboardPlatform,
    EntityType,
    MetadataChangeEvent,
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@dataclass
class LookerRunConfig(RunConfig):
    base_url: str
    client_id: str
    client_secret: str

    verify_ssl: bool = True
    timeout: int = 120


class LookerExtractor(BaseExtractor):
    """Looker metadata extractor"""

    def initSdk(self, config: LookerRunConfig) -> Looker31SDK:
        # Load config using environment variables instead from looker.ini file
        # See https://github.com/looker-open-source/sdk-codegen#environment-variable-configuration
        os.environ["LOOKERSDK_BASE_URL"] = config.base_url
        os.environ["LOOKERSDK_CLIENT_ID"] = config.client_id
        os.environ["LOOKERSDK_CLIENT_SECRET"] = config.client_secret
        os.environ["LOOKERSDK_VERIFY_SSL"] = str(config.verify_ssl)
        os.environ["LOOKERSDK_TIMEOUT"] = str(config.timeout)
        return looker_sdk.init31()

    async def extract(self, config: RunConfig) -> List[MetadataChangeEvent]:
        assert isinstance(config, LookerRunConfig)

        logger.info("Fetching metadata from Looker")

        sdk = self.initSdk(config)

        dashboards = self._fetch_dashboards(sdk)

        return [EventUtil.build_dashboard_event(d) for d in dashboards]

    def _fetch_dashboards(self, sdk: Looker31SDK) -> List[Dashboard]:
        dashboards: List[Dashboard] = []
        for dashboard in sdk.all_dashboards():
            dashboard_info = DashboardInfo()
            dashboard_info.aspect_type = AspectType.DASHBOARD_INFO
            dashboard_info.title = dashboard.title
            dashboard_info.description = dashboard.description

            dashboards.append(
                Dashboard(
                    entity_type=EntityType.DASHBOARD,
                    logical_id=DashboardLogicalID(
                        dashboard.id, DashboardPlatform.LOOKER
                    ),
                    dashboard_info=dashboard_info,
                )
            )

        return dashboards
