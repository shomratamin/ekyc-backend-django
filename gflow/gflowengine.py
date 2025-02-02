from jinja2 import Template, Environment, BaseLoader, BytecodeCache, TemplateNotFound, FileSystemLoader
from .models import GFlowPage, GFlowCollection, GFlowApp
from . import exposed_functions
from django.db.models.signals import post_save
from django.dispatch import receiver

global gflow_environment, gflow_loader

class GFlowLoader(BaseLoader):
    def __init__(self):
        self.template_dict = dict()
        self.uptodate_map = dict()
        self.load_all()

    def load_all(self):
        all_apps = GFlowApp.objects.filter(published=True)
        if all_apps is None:
            return

        for app in all_apps:
            collections = app.collections.all()
            for collection in collections:
                pages = collection.pages.all()
                for page in pages:
                    _key = '__'.join([app.routing, page.name])
                    self.template_dict[_key] = [page.content, page.modified, page.id]
                    self.uptodate_map[_key] = False

        # return
        # all_templates = GFlowPage.objects.all().order_by('collection__name')
        # for t in all_templates:
        #     # if t.name.startswith('partial'):
        #     # if t.app.name == 'onboarding' or t.app.name == 'shared' or t.app.name == 'simplified':
        #     #     self.template_dict[t.name] = [t.content, t.page_index, t.is_active, t.modified, t.access_permission]
        #     #     self.uptodate_map[t.name] = False
        #     # # else:
        #     self.template_dict[t.name] = [t.content, t.modified]
        #     self.uptodate_map[t.name] = False

    def get_template_names(self):
        templates = []
        for key in list(self.template_dict.keys()):
            template = self.template_dict[key]
            templates.append('__'.join([key,str(template[-1])]))
        templates.sort()
        return templates

    def get_collections(self):
        templates = []
        collections = GFlowCollection.objects.all()
        for collection in collections:
            pages = collection.pages.all()
            for page in pages:
                _key = '__'.join([collection.name, page.name, str(page.id)])
                templates.append(_key)
        templates.sort()
        return templates

    def get_template(self, name):
        if name in self.template_dict:
            return self.template_dict[name][0]
        else:
            return False

    def get_template_ide(self, name):
        t_name = name.split('__')
        template = GFlowPage.objects.filter(pk=t_name[-1])
        if not template.exists():
            return 'error'

        template = template.first()
        
        return template.content


    def get_access_permission(self, name):
        if name in self.template_dict:
            return self.template_dict[name][-1]
        else:
            return False

    def create_or_update_template(self, name, content):
        app_name = name.split('__')
        template = GFlowPage.objects.filter(pk=app_name[-1])
        if not template.exists():
            return

        template = template.first()
        template.content = content
        template.save()

        template_key = '__'.join(app_name[:-1])
        self.template_dict[template_key] = [template.content, template.modified, template.id]
        self.uptodate_map[template_key] = False

    def delete_template(self, name):
        template = GFlowPage.objects.filter(name = name)
        if template.exists():
            template.delete()
            del self.template_dict[name]
            del self.uptodate_map[name]

    def get_source(self, environment, name):
        if name not in self.template_dict:
            raise TemplateNotFound(name)

        def uptodate():
            uptodate_status = self.uptodate_map[name]
            if uptodate_status == False: 
                self.uptodate_map[name] = True
            return uptodate_status

        template = self.template_dict[name]
        return template[0], None, uptodate




def load_environment():
    global gflow_environment, gflow_loader, gflow_admin_environment
    gflow_loader = GFlowLoader()
    gflow_environment = Environment(block_start_string='<!--?', block_end_string='?-->', \
        line_statement_prefix='#', extensions=['jinja2.ext.loopcontrols','jinja2.ext.do'], loader=gflow_loader)
    gflow_environment.filters['bool'] = bool
    gflow_admin_environment = Environment(block_start_string='<!--?', block_end_string='?-->', \
        extensions=['jinja2.ext.loopcontrols'], loader=FileSystemLoader('gflow/templates'))

def bind_exposed_functions():
    global gflow_environment
    for name, func in exposed_functions.__dict__.items():
        if callable(func):
            if name.startswith('expose__'):
                name = name.replace('expose__','')
                gflow_environment.globals[name] = func

load_environment()
bind_exposed_functions()


@receiver(post_save, sender=GFlowPage)
def gflow_page_update_hook(sender, instance, using, **kwargs):
    global gflow_loader
    gflow_loader.load_all()

@receiver(post_save, sender=GFlowCollection)
def gflow_collection_update_hook(sender, instance, using, **kwargs):
    global gflow_loader
    gflow_loader.load_all()


@receiver(post_save, sender=GFlowApp)
def gflow_app_update_hook(sender, instance, using, **kwargs):
    global gflow_loader
    gflow_loader.load_all()
