import datetime
import cloudlanguagetools.constants


class UsageSlice():
    def __init__(self, 
                request_type: cloudlanguagetools.constants.RequestType, 
                usage_scope: cloudlanguagetools.constants.UsageScope, 
                usage_period: cloudlanguagetools.constants.UsagePeriod, 
                service: cloudlanguagetools.constants.Service, 
                api_key: str):
        self.request_type = request_type
        self.usage_scope = usage_scope
        self.usage_period = usage_period
        self.service = service
        self.api_key = api_key

    def build_key_suffix(self) -> str:
        date_str = datetime.datetime.today().strftime('%Y%m')
        if self.usage_period == cloudlanguagetools.constants.UsagePeriod.daily:
            date_str = datetime.datetime.today().strftime('%Y%m%d')

        api_key_suffix = ''
        if self.usage_scope == cloudlanguagetools.constants.UsageScope.User:
            api_key_suffix = f':{self.api_key}'

        return f':{self.usage_scope.key_str}:{self.usage_period.name}:{date_str}:{self.service.name}:{self.request_type.name}{api_key_suffix}'


    def over_quota(self, characters, requests) -> bool:
        if self.usage_scope == cloudlanguagetools.constants.UsageScope.User:
            if self.usage_period == cloudlanguagetools.constants.UsagePeriod.daily:
                if self.service == cloudlanguagetools.constants.Service.Naver:
                    if characters > 20000:
                        return True
                if characters > 100000:
                    return True
        return False


