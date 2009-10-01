from DateTime import DateTime

def handle_object_created(obj, event):
    """
    If the user did not define a publication date, we set it to now
    """
    if(not obj.Schema()['publication_date'].get(obj)):
        now = DateTime()
        obj.setPublication_date(now)


def handle_workflow_action(obj, event):
    """ If an OSH_Links gets published, its effective date will be set to the current date.
        If no Publication date was set, we set this too
    """
    if event.action=='publish':
        now = DateTime()
        obj.setEffectiveDate(now)
        obj.reindexObject()
        if(not obj.Schema()['publication_date'].get(obj)):
            now = DateTime()
            obj.setPublication_date(now)

