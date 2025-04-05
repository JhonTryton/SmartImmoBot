import os
from telegram import (
    Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
)
from telegram.ext import (
    Updater, CommandHandler, CallbackQueryHandler, CallbackContext
)
from tinydb import TinyDB
import logging

TOKEN = os.getenv("7602685077:AAHoYinNG1uTmDa5Tp-dfKBMjQCAKH26kvE")
MONGO_URI = os.getenv("mongodb+srv://jhonskyload:9RQEDyKAKPeqYaF1@cluster0.tabu1ts.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
# Configuration
TOKEN = '7602685077:AAHoYinNG1uTmDa5Tp-dfKBMjQCAKH26kvE'  # Remplace par ton token Telegram
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
db = TinyDB("smartimmobot_db.json")

# Logs
logging.basicConfig(level=logging.INFO)

# === Fonctions utilitaires ===
def get_main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🆘 Aide", callback_data='help')],
        [InlineKeyboardButton("📢 Annonces", callback_data='annonces')],
        [InlineKeyboardButton("✍️ Faire une demande", callback_data='demande')],
        [InlineKeyboardButton("📅 Rendez-vous", callback_data='rdv')],
        [InlineKeyboardButton("💡 Conseils", callback_data='conseils')],
        [InlineKeyboardButton("❤️ Dons", callback_data='dons')]
    ])

def get_back_button(callback_data='start'):
    return InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Retour", callback_data=callback_data)]])

# === Commandes principales ===
def start(update: Update, context: CallbackContext):
    user = update.effective_user
    welcome = f"Bienvenue *{user.first_name}* sur *SmartImmoBot* !\n\nChoisissez une option ci-dessous :"
    update.message.reply_text(welcome, parse_mode=ParseMode.MARKDOWN, reply_markup=get_main_menu())

def help_command(update: Update, context: CallbackContext):
    msg = (
        "*Aide - SmartImmoBot*\n\n"
        "Voici les commandes disponibles :\n"
        "• /start - Démarrer le bot\n"
        "• /annonces - Voir les annonces\n"
        "• /demande - Soumettre une demande\n"
        "• /rdv - Prendre un rendez-vous\n"
        "• /conseils - Recevoir des conseils\n"
        "• /dons - Soutenir le projet\n\n"
        "Besoin d'assistance ? Contact : 0171070739"
    )
    update.callback_query.edit_message_text(text=msg, parse_mode=ParseMode.MARKDOWN, reply_markup=get_back_button())

# === Gestion des callbacks ===
def handle_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data

    if data == "help":
        help_command(update, context)
    elif data == "annonces":
        handle_annonces(update)
    elif data == "demande":
        handle_demande(update)
    elif data == "rdv":
        handle_rdv(update)
    elif data == "conseils":
        handle_conseils(update)
    elif data == "dons":
        handle_dons(update)
    elif data in ["annonces_filtrer", "demande_filtrer"]:
        query.edit_message_text("Merci. Veuillez décrire votre besoin (type de bien, budget, localisation, etc.)", reply_markup=get_back_button())
    elif data in ["conseil_achat", "conseil_location", "conseil_vente", "conseil_invest"]:
        conseils = {
            "conseil_achat": "Analysez le marché, négociez bien, vérifiez les documents avant tout achat.",
            "conseil_location": "Priorisez l’emplacement, l’état du logement, et vérifiez le contrat.",
            "conseil_vente": "Faites de belles photos, fixez un bon prix, soyez transparent.",
            "conseil_invest": "Investissez dans des zones prometteuses, comparez les rendements."
        }
        query.edit_message_text(conseils[data], reply_markup=get_back_button('conseils'))
    elif data in ["rdv_matin", "rdv_aprem", "rdv_soir"]:
        horaires = {
            "rdv_matin": "Vous serez contacté entre 8h et 12h.",
            "rdv_aprem": "Vous serez contacté entre 13h et 18h.",
            "rdv_soir": "Vous serez contacté après 18h."
        }
        db.insert({"rendezvous": data})
        query.edit_message_text(f"Merci ! {horaires[data]}", reply_markup=get_back_button("rdv"))
    elif data == "don_virement":
        query.edit_message_text("Effectuez un virement au RIB suivant : *CI198 0111 1234 5678 9012*", parse_mode=ParseMode.MARKDOWN, reply_markup=get_back_button("dons"))
    elif data == "start":
        query.edit_message_text("Menu principal :", reply_markup=get_main_menu())

# === Fonctions spécifiques ===
def handle_annonces(update: Update):
    keyboard = [
        [InlineKeyboardButton("Location", url="https://www.exemple.com/location")],
        [InlineKeyboardButton("Vente", url="https://www.exemple.com/vente")],
        [InlineKeyboardButton("Filtrer", callback_data='annonces_filtrer')],
        [InlineKeyboardButton("⬅️ Retour", callback_data='start')]
    ]
    update.callback_query.edit_message_text("Choisissez une catégorie :", reply_markup=InlineKeyboardMarkup(keyboard))

def handle_demande(update: Update):
    keyboard = [
        [InlineKeyboardButton("Location", callback_data='demande_filtrer')],
        [InlineKeyboardButton("Vente", callback_data='demande_filtrer')],
        [InlineKeyboardButton("⬅️ Retour", callback_data='start')]
    ]
    update.callback_query.edit_message_text("Quel type de demande souhaitez-vous faire ?", reply_markup=InlineKeyboardMarkup(keyboard))

def handle_rdv(update: Update):
    keyboard = [
        [InlineKeyboardButton("Matin (8h-12h)", callback_data='rdv_matin')],
        [InlineKeyboardButton("Après-midi (13h-18h)", callback_data='rdv_aprem')],
        [InlineKeyboardButton("Soir (après 18h)", callback_data='rdv_soir')],
        [InlineKeyboardButton("⬅️ Retour", callback_data='start')]
    ]
    update.callback_query.edit_message_text("Sélectionnez un créneau horaire :", reply_markup=InlineKeyboardMarkup(keyboard))

def handle_conseils(update: Update):
    keyboard = [
        [InlineKeyboardButton("Achat", callback_data='conseil_achat')],
        [InlineKeyboardButton("Location", callback_data='conseil_location')],
        [InlineKeyboardButton("Vente", callback_data='conseil_vente')],
        [InlineKeyboardButton("Investissement", callback_data='conseil_invest')],
        [InlineKeyboardButton("⬅️ Retour", callback_data='start')]
    ]
    update.callback_query.edit_message_text("Quel type de conseils cherchez-vous ?", reply_markup=InlineKeyboardMarkup(keyboard))

def handle_dons(update: Update):
    keyboard = [
        [InlineKeyboardButton("PayPal", url="https://paypal.com")],
        [InlineKeyboardButton("Crypto", url="https://binance.com")],
        [InlineKeyboardButton("Virement Bancaire", callback_data='don_virement')],
        [InlineKeyboardButton("⬅️ Retour", callback_data='start')]
    ]
    update.callback_query.edit_message_text("Choisissez un mode de don :", reply_markup=InlineKeyboardMarkup(keyboard))

# === Handlers ===
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CallbackQueryHandler(handle_callback))

# === Lancement du bot ===
updater.start_polling()
updater.idle()
