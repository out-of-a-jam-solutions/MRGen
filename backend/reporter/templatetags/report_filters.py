from django import template

from reporter import models

register = template.Library()

@register.filter
def count_unresolved_warnings(report):
    """
    Counts the number of warnings that are unresolved at the end of the report period.
    """
    return report.subreport_set.filter(end_date=report.end_date).get().num_warnings_unresolved_end


@register.filter
def count_resolved_warnings(report):
    """
    Counts the number of warnings that were resolved during the report period.
    """
    total = 0
    for sub_report in report.subreport_set.all():
        total += sub_report.num_warnings_resolved
    return total

