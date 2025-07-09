from balethon.conditions import command, group, at_state, private, equals
from config import *  
from group_manager import *
from state_handler import *
from callback_handler import call_handler



@bot.on_callback_query(private)
async def reply_buttons(callback_query):
    await call_handler(callback_query)


@bot.on_message(command("start") & private)
async def handle_start(message):
    await bot.send_message(message.chat.id, "سلام! یکی از گزینه‌ها رو انتخاب کنید:", main_menu(True))


@bot.on_message(at_state('INPUT_NUMBER_NOTE') ) 
async def first_state_save_note(message):
    await first_step_save(message)


@bot.on_message(at_state('INPUT_TEXT_NOTE'))
async def next_state_save_note(message):
    await next_step_save(message)    


@bot.on_message(at_state("INPUT_NUMBER_HADITH"))
async def handle_hadith_id(message):
    await handel_number_hadith(message)


@bot.on_message(at_state('INPUT_EDIT_NUMBER_NOTE'))
async def first_state_edit_not(message):
    await first_state_edit(message)
    
@bot.on_message(at_state('INPUT_EDIT_TEXT_NOTE'))
async def next_state_edit_not(message):
    await next_state_edit(message)

bot.on_message(at_state('SEND_MESSAGE_TO_CHANEL'))
async def send_to_chanle(message):
    print ('...................')
    await send_message_to_chanel(message)


@bot.on_message(group)
async def collect_group_input(message):
    if message.chat.id == group_pajohesh_hadith_id:
        await manage_hadith_message(message.chat.id , message.id , message.text)


@bot.on_edited_message(group)
async def update_handler(message):
    if message.chat.id == group_pajohesh_hadith_id:
        await handle_hadith_updats(message.chat.id , message.id , message.text)
        




bot.run()
