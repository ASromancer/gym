from . import models

def get_logo(request):
	logo=models.AppSetting.objects.first()
	data={
		'logo':logo.image_tag   # type: ignore
	}
	return data