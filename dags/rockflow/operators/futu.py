import os

from stringcase import snakecase

from rockflow.common.futu_company_profile import FutuCompanyProfileCn, FutuCompanyProfileEn
from rockflow.operators.oss import OSSSaveOperator


class FutuOperator(OSSSaveOperator):
    def __init__(self,
                 ticker: str,
                 **kwargs) -> None:
        if 'task_id' not in kwargs:
            kwargs['task_id'] = f"{snakecase(self.__class__.__name__)}_{ticker}"
        super().__init__(**kwargs)
        self.ticker = ticker

    @property
    def key(self):
        return os.path.join(self._key, f"{self.ticker}.html")

    @property
    def page(self):
        raise NotImplementedError()

    @property
    def instance(self):
        return self.page(
            symbol=self.ticker,
            futu_ticker=self.ticker,
            proxy=self.proxy,
        )

    @property
    def content(self):
        return self.instance.get().content


class FutuCnOperator(FutuOperator):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    @property
    def page(self):
        return FutuCompanyProfileCn


class FutuEnOperator(FutuOperator):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    @property
    def page(self):
        return FutuCompanyProfileEn
