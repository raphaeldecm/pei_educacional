from datetime import datetime

from django.template.loader import get_template

from .models import Pei


def generatePeiExportHtml(pei_id):
    pei = Pei.objects.get(id=pei_id)

    current_datetime = datetime.now()
    formatted_date = current_datetime.strftime("%H:%Mh, em %d/%m/%Y")
    current_year = current_datetime.strftime("%Y")

    template = get_template("educational_plan/peis/pei_export.html")
    return template.render(
        {
            "object": pei,
            "formatted_date": formatted_date,
            "current_year": current_year,
        },
    )
