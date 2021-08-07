from .base.basemodel import BaseModel, fields


class Settings(BaseModel):
    company_name = fields.CharField(max_length=70, null=True, default="Claims PLC")
    company_logo = fields.CharField(max_length=255, null=True)
    app_name = fields.CharField(max_length=30, default="Claims App")
    slogan = fields.CharField(max_length=70, null=True, default="Making your claims easier")

    class Meta:
        table = "settings"
