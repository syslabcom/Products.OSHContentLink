from DateTime import DateTime

def handle_object_created(obj, event):
    """ We can safely set the publication_date to the current date without
    condition on creation. If the users manually sets a fate, it will take precendence."""
    if(not obj.Schema()['publication_date'].get(obj)):
        now = DateTime()
        obj.setPublication_date(now)


def handle_workflow_action(obj, event):
    """ If an OSH_Links gets published, its effective date will be set to the current date """
    if event.action=='publish':
        now = DateTime()
        obj.setEffectiveDate(now)
        obj.reindexObject()

