import datetime
from pyplanet.views.generics.widget import WidgetView
import asyncio


class AFKWidget(WidgetView):
    widget_x = -999
    widget_y = -999
    template_name = 'afk/AFK.xml'

    def __init__(self, app):
        super().__init__(self)
        self.app = app
        self.manager = app.context.ui
        self.id = 'pyplanet__AFK__Handling'
        self.subscribe("Player_AFK", self.handle_player_afk)
    
    async def get_context_data(self):
        context = await super().get_context_data()
        self.afk_timeout = await self.app.setting_afk_timeout.get_value()
        self.afk_timeout_frequence_check = await self.app.setting_afk_timeout_frequence_check.get_value()
        self.afk_timeout_sleep_delay = await self.app.setting_afk_timeout_sleep_delay.get_value()
        self.afk_grace_period = await self.app.setting_afk_grace_period.get_value()
        context.update({'afktimeout': self.afk_timeout,
                        'afktimeoutfrequencecheck': self.afk_timeout_frequence_check,
                        'afktimeoutsleepdelay': self.afk_timeout_sleep_delay,
                        'afkgraceperiod': self.afk_grace_period
                        })
        return context
    
    async def handle_player_afk(self, player, action, values, *args, **kwargs):
        #x = datetime.datetime.now()
        #print(x)
        await self.app.instance.gbx.multicall(
			self.app.instance.gbx('ForceSpectator', player.login, 3),
			self.app.instance.chat('$fff {}$z$s$fff is now set away from keyboard due to $z$s$f50inactivity.'.format(player.nickname))
		)
