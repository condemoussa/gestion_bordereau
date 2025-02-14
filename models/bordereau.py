# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models

class FicheBordereau(models.Model):
    _name = "fiche.bordereau"
    _description = "Gestion des bordereaux"
    _rec_name = "name"

    @api.model
    def create(self, vals):
        record = super(FicheBordereau, self).create(vals)
        if record:
            record['name'] = "N°bord" + "00" + str(record.id)
        return record



    def action_submit(self):
        self.update({"state": "verify"})
        # envoie de mail
        users = self.env["res.users"].search([('type_groups', '=', 'type2')])

        # Création de l'e-mail pour chaque utilisateur
        for user in users:
            mail_values = {
                'subject': "Création de Bordereau d’envoi",
                'body_html': f"""
                    <p>Bonjour M. {user.name},</p>
                    <p>Un nouveau bordereau a été créé : <strong>{self.name}</strong> par <strong>{self.create_uid.name}</strong>. 
                    Veuillez vérifier, s'il vous plaît.</p>
                """,
                'email_to': user.user_mail,
                'author_id': self.env.user.partner_id.id,  # Auteur de l'email (l'utilisateur actuel)
            }
            self.env['mail.mail'].create(mail_values).send()  # Création et envoi de l'email

    def action_verify_controleur(self):

        self.update({"state": "transfer"})

        users = self.env["res.users"].search([('type_groups', '=', 'type11')])

        for user in users:
            mail_values = {
                'subject': "Bordereau d’envoi",
                'body_html': f"""
                           <p>Bonjour M. {user.name},</p>
                           <p>Un nouveau bordereau a été créé : <strong>{self.name}</strong> par <strong>{self.create_uid.name}</strong>. 
                           Veuillez vérifier, s'il vous plaît.</p>
                       """,
                'email_to': user.user_mail,
                'author_id': self.env.user.partner_id.id,  # Auteur de l'email (l'utilisateur actuel)
            }
            self.env['mail.mail'].create(mail_values).send()  # Création et envoi de l'email

    def action_transfer(self):
        self.update({"state": "transfere3"})

    def action_rejeter(self):
        self.update({"state": "draft"})

    def action_verify_d_financier(self):
        self.update({"state": "transfere2"})
        users = self.env["res.users"].search([('type_groups', '=', 'type8')])

        for user in users:
            mail_values = {
                'subject': "Bordereau d’envoi",
                'body_html': f"""
                                  <p>Bonjour M. {user.name},</p>
                                  <p>Un nouveau bordereau a été créé : <strong>{self.name}</strong> par <strong>{self.create_uid.name}</strong>. 
                                  Veuillez vérifier, s'il vous plaît.</p>
                              """,
                'email_to': user.user_mail,
                'author_id': self.env.user.partner_id.id,  # Auteur de l'email (l'utilisateur actuel)
            }
            self.env['mail.mail'].create(mail_values).send()  # Création et envoi de l'email

    def action_verify_tresorerie(self):
        self.update({"state": "transfere3"})

        users = self.env["res.users"].search([('type_groups', '=', 'type3')])

        for user in users:
            mail_values = {
                'subject': "Bordereau d’envoi",
                'body_html': f"""
                                         <p>Bonjour M. {user.name},</p>
                                         <p>Un nouveau bordereau a été créé : <strong>{self.name}</strong> par <strong>{self.create_uid.name}</strong>. 
                                         Veuillez autoriser, s'il vous plaît.</p>
                                     """,
                'email_to': user.user_mail,
                'author_id': self.env.user.partner_id.id,  # Auteur de l'email (l'utilisateur actuel)
            }
            self.env['mail.mail'].create(mail_values).send()  # Création et envoi de l'email

    def action_autorisation_visa(self):
        self.update({"state": "transfere4"})

        users = self.env["res.users"].search([('type_groups', '=', 'type8')])

        for user in users:
            mail_values = {
                'subject': "Bordereau d’envoi",
                'body_html': f"""
                                                <p>Bonjour M. {user.name},</p>
                                                <p>l'autorisation à ete accord  </p>
                                               
                                            """,
                'email_to': user.user_mail,
                'author_id': self.env.user.partner_id.id,  # Auteur de l'email (l'utilisateur actuel)
            }
            self.env['mail.mail'].create(mail_values).send()  # Création et envoi de l'email



    name = fields.Char("N°" , readonly=True)
    description = fields.Text(string="Description")
    dat_bord = fields.Date("Date bordereau")
    user_id= fields.Many2one("res.users", string="Demandeur",  default=lambda self: self.env.user.id , readonly=True)
    state = fields.Selection(
        [
            ("draft", "Brouillon"),
            ("verify", "Contrôleur de Gestion"),
            ("transfer", "Directeur Financier"),
            ("transfere2", "Tresorerie"),
            ("transfere3", "Directeur Général"),
            ("transfere4", "Visa d'autorisation paiement"),
            ("rejected", "Rejetée"),
        ],
        string="État",
        default="draft",
    )

    piece_jointe= fields.Binary("Bordereau physique")


