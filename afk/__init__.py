"""
AFK
"""
import asyncio

from pyplanet.apps.config import AppConfig
from pyplanet.apps.core.maniaplanet import callbacks as mp_signals
from .views import AFKWidget
from pyplanet.core.signals import pyplanet_start_after
from pyplanet.contrib.setting import Setting

class afk(AppConfig):
    game_dependencies = ['trackmania', 'trackmania_next', 'shootmania']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = AFKWidget(self)
        self.setting_afk_timeout = Setting(
            'afk_timeout', 'AFK Timeout', Setting.CAT_BEHAVIOUR, type=int,
            description='How long players can stay inactive until they are declared AFK. (in ms)',
            default=120000
        )
        self.setting_afk_timeout_frequence_check = Setting(
            'afk_timeout_frequence_check', 'AFK Timeout Frequence Check', Setting.CAT_BEHAVIOUR, type=int,
            description='How frequently to check that a player might be AFK. (in ms)',
            default=10000)
        
        self.setting_afk_timeout_sleep_delay = Setting(
            'afk_timeout_sleep_delay', 'AFK Timeout Delay', Setting.CAT_BEHAVIOUR, type=int,
            description='When assessing whether a player is AFK, check every X ms. Lower values may severely impact performance.',
            default=1000)
        
        self.setting_afk_grace_period = Setting(
            'afk_grace_period', 'AFK Grace Period', Setting.CAT_BEHAVIOUR, type=int,
            description='How long to wait before checking again that a player that has been confirmed to be active is AFK. (in ms)',
            default=30000)
        
    async def on_start(self):
        self.context.signals.listen(mp_signals.player.player_connect, self.player_connect)
        self.context.signals.listen(mp_signals.map.map_begin, self.map_start)
        self.context.signals.listen(pyplanet_start_after, self.on_after_start)
        
        # Register settings
        await self.context.setting.register(self.setting_afk_timeout)
        await self.context.setting.register(self.setting_afk_timeout_frequence_check)
        await self.context.setting.register(self.setting_afk_timeout_sleep_delay)
        await self.context.setting.register(self.setting_afk_grace_period)

    async def player_connect(self, player, **kwargs):
        await self.widget.display(player)

    async def map_start(self, *args, **kwargs):
        await self.widget.display()

    async def on_after_start(self, *args, **kwargs):
        await asyncio.sleep(1)
        asyncio.ensure_future(asyncio.gather(*[
            self.player_connect(p) for p in self.instance.player_manager.online
        ]))