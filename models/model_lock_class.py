# -*- coding: utf-8 -*- 

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ModelLockClass(models.AbstractModel):
    """ Model lock class is the base class of the Lock/unlock management,this will add the lock field,lock/unlock methods
    to model so that this feature is centralized"""
    _name = 'model.lock.class'
    _description = 'Model lock class'

    locked = fields.Boolean(string='Locked',default=False)

    def action_lock(self):
        self._action_lock()

    def action_unlock(self):
        self._action_unlock()

    def _action_lock(self):
        self.write({'locked': True})

    def _action_unlock(self):
        self.with_context(force_update=True).write({'locked': False})


    def write(self, vals):
        for each in self:
            if each.locked and not each.env.context.get('force_update',False):
                raise ValidationError(_("%s is locked,Can not update/remove locked record")%each._description)
        return super(ModelLockClass,self).write(vals)

    def unlink(self):
        for each in self:
            if each.locked:
                raise ValidationError(_("%s is locked,Can not update/remove locked record")%each._description)
        return super(ModelLockClass,self).unlink()

    def _locked_by_access_rights(self):
        pass