# -*- coding: utf-8 -*-
import pytz
from datetime import datetime
from odoo.addons.sm_maintenance.models.models_load_data import load_data


class sm_utils(object):

  @staticmethod
  def get_today_date():
    timezone = pytz.timezone('Europe/Madrid')
    date_time = datetime.now(tz=timezone)
    return datetime.date(date_time)

  @staticmethod
  def send_email_from_template(parent, template):
    company = parent.env.user.company_id
    mail_template = getattr(company, template)
    email_values = {'send_from_code': True}
    mail_template.with_context(email_values).send_mail(parent.id,True)

  @staticmethod
  def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

  @staticmethod
  def record_exists(parent, child_model, relation_name, name_query):
    if relation_name:
      relation = getattr(parent, relation_name)
      if relation.id:
        return True
    else:
      existing_model = parent.env[child_model].sudo().search(
        [('name', '=', name_query)])
      if existing_model.id:
        return True
    return False

  @staticmethod
  def get_create_existing_model(model_env, query, creation_data=False):
    existing_model = model_env.search(query)
    create_model = True
    if existing_model:
      if existing_model.exists():
        model = existing_model
        create_model = False
    if create_model:
      if creation_data:
        model = model_env.create(creation_data)
    return model

  @staticmethod
  def delete_existing_model(model_env, query):
    existing_model = model_env.search(query)
    if existing_model:
      if existing_model.exists():
        existing_model.unlink()
        return True
    return False

  @staticmethod
  def create_system_task(parent,task_name=False,task_description=False):
    loader = load_data.get_instance()
    parent.env['project.task'].create({
      'name': task_name,
      'description': task_description,
      'project_id': loader.get_system_project_id()
    })

  @staticmethod
  def is_module_active(contextself, module_name):
    module = contextself.env['ir.module.module'].search(
      [('name', '=', module_name), ('state', '=', 'installed')])
    return module.exists()