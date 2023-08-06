"""This file is part of Pyxgram.

   Pyxgram is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   Pyxgram is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with Pyxgram.  If not, see <http://www.gnu.org/licenses/>. """

#Pls send the issues to https://github.com/borisd93/pyxgram/issues/

import time
import os
from functools import partial
import telegram
import telegram.ext

class Logger:
    """Logger Class its a self logging method for Basebot of pyxgram"""
    def __init__(self,logfile,separator=True):
        """Init method of Logger Class"""
        self.logfile=logfile
        if separator:
            self.log_separator()
        if os.path.exists(self.logfile) is False:
            with open(self.logfile,'w') as self.main_file:
                self.main_file.write('Log created at '+time.strftime("%H:%M:%S")+'\n')
        with open(self.logfile,'a') as self.main_file:
            self.main_file.write('Log started at '+time.strftime("%H:%M:%S")+'\n')
        print('Log started at '+time.strftime("%H:%M:%S"))
    def log_separator(self):
        """Creates a separator"""
        with open(self.logfile,'a') as self.main_file:
            self.main_file.write('\n\nSeparator\n\n')
    def error(self,error):
        """Logs an error"""
        with open(self.logfile,'a') as self.main_file:
            self.main_file.write('Error at '+time.strftime("%H:%M:%S")+': '+error+'\n')
        print('Error at '+time.strftime("%H:%M:%S")+': '+error)
    def info(self,info):
        """Logs an information"""
        with open(self.logfile,'a') as self.main_file:
            self.main_file.write('Info at '+time.strftime("%H:%M:%S")+': '+info+'\n')
        print('Info at '+time.strftime("%H:%M:%S")+': '+info)
    def clear(self):
        """Clears the log"""
        with open(self.logfile,'a') as self.main_file:
            self.main_file.write('')
        with open(self.logfile,'a') as self.main_file:
            self.main_file.write('Log cleared at '+time.strftime("%H:%M:%S")+'\n')
        print('Log cleared at '+time.strftime("%H:%M:%S"))

class Basebot:
    """BaseBot its the main class of pyxgram module."""
    def __init__(self,token,include=None,logging=True):
        """Init method of BaseBot class """
        self.updater=telegram.ext.Updater(token=token)
        self.logging=logging
        self._jobqueue=None
        self._help=''
        self.dispatcher=self.updater.dispatcher
        if self.logging:
            self.log=Logger('bot.log')
            self.log.info('Bot created')
        if include:
            self.admin_id=include.admin_id
            self.separator=include.separator
        else:
            self.admin_id=[]
            self.separator='-'
    def error_handler(self,update: telegram.Update,context: telegram.ext.CallbackContext,function):
        """Its a error hancler for all the comands"""
        try:
            function(update,context)
        except ValueError as err:
            if self.logging:
                self.log.error('Value Error')
                self.log.error(str(err))
        except ZeroDivisionError as err:
            if self.logging:
                self.log.error('ZeroDivisionError')
                self.log.error(str(err))
        except Exception as err:
            if self.logging:
                self.log.error('A unknow error as ocurred')
                self.log.error(str(err))
    def normal_command(self,function):
        """Adds a command. Its a shorcut for dispatcher.add_handler(telegram.ext.CommandHandler)"""
        function1=partial(self.error_handler,function=function)
        self.dispatcher.add_handler(telegram.ext.CommandHandler(function.__name__,function1))
        self._help+='/'+function.__name__+self.separator+str(function.__doc__)+'\n\n'
        if self.logging:
            self.log.info('Added a new command')
    def admin_pass(self,update:telegram.Update,context:telegram.ext.CallbackContext,function):
        """This is a minimal subfunction of admin_command decorator"""
        for aid in self.admin_id:
            if update.message.chat_id==aid:
                function(update,context)
                break
            else:
                pass
    def admin_command(self,function):
        """The admin_command function uses the admin_id from the include.py file
        you can set this with <class>.admin_id=id replacing id with our id."""
        if self.logging:
            self.log.info('Added a Admin Command')
        function1=partial(self.admin_pass,function=function)
        handler=telegram.ext.CommandHandler(function.__name__,function1)
        self.dispatcher.add_handler(handler)
    def package_add(self,packagename):
        """Adds a package into the commands"""
        exec('from '+packagename+' import initial',globals())
        exec('initial(self)')
        if self.logging:
            self.log.info('Added the package '+packagename)
    def typing(self,update):
        """Send's the typing chat action"""
        context=telegram.ext.CallbackContext(self.dispatcher)
        return context.bot.send_chat_action(
            chat_id=update.message.chat_id,
            action=telegram.ChatAction.TYPING
        )
    def start(self):
        """Start's the bot and all the systems"""
        try:
            self.updater.start_polling()
            self.updater.idle()
            if self.logging:
                self.log.info('Bot started')
        except telegram.error.NetworkError as error:
            if self.logging:
                self.log.error('Network Error')
                self.log.error(str(error))
    def reply_text(self,text,update):
        """Reply a message with a text.
        This is a shorcut for the
        update.message.reply_text
        function"""
        update.message.reply_text(text)
    def send_text(self,text,update,chat_id=None,reply_markup=None):
        """Send a message with a text
        This i a shorcut for the
        bot.send_message or
        context.bot.send_message"""
        context=telegram.ext.CallbackContext(self.dispatcher)
        if chat_id is None:
            chat_id=update.message.chat_id
        if reply_markup:
            context.bot.send_message(chat_id,text,reply_markup=reply_markup)
        else:
            context.bot.send_message(chat_id,text)
    def setup_jqe(self):
        """Setup's the Jobqueue"""
        if self._jobqueue is None:
            self._jobqueue=self.updater.job_queue
        else:
            self.log.error('Jobqueue was already initiated')
    def jqe_run_repeating(self,function,date):
        """Its a shorcut for the Jobqueue of telegram module
        function - This argument need to be a function
        date - The time in seconds or datetime.datetime"""
        if self._jobqueue is None:
            self.log.error('Jobqueue not initiated')
        else:
            self._jobqueue.run_repeating(function,date)
    # BETA Maybe dont work ↓
    def jqe_run_once(self,function,date):
        """Its a shorcut for the Jobqueue of telegram module
        function - This argument need to be a function
        date - The time in seconds or datetime.datetime"""
        if self._jobqueue is None:
            self.log.error('Jobqueue not initiated')
        else:
            self._jobqueue.run_once(function,date)
    # BETA Maybe dont work ↑
    def jqe_kill(self):
        """Kills the JQE"""
        if self._jobqueue is None:
            self.log.error('Jobqueue not initiated')
        else:
            self._jobqueue.stop()
    def jqe_start(self):
        """Starts a killed JQE"""
        if self._jobqueue is None:
            self.log.error('Jobqueue not initiated')
        else:
            self._jobqueue.start()
    def commandFilter(self,function):
        """A filter for commands"""
        self.dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.command,function))
        self.log.info('Added a Text Filter Handler')
    def textFilter(self,function):
        """A filter for text"""
        self.dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text,function))
        self.log.info('Added a Text Filter Handler')
    def documentFilter(self,function):
        """A filter for documents"""
        self.dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.document,function))
        self.log.info('Added a Document Filter Handler')
    # BETA Maybe dont work ↓
    def send_with_buttons(self,text,callback,buttons,update,chat_id=None):
        """A function for send the buttons markup, not the buttons menu.
        An example,
        self.send_with_buttons(
            'hello',mycallbackfunction,
            [
                [telegram.InlineKeyboardButton("Here",callback_data=1),telegram.InlineKeyboardButton("Here",callback_data=1)]
            ],"",
            chat_id=update.message.chat_id
        )"""
        try:
            context=CallbackContext(self.dispatcher)
            if chat_id is None:
                chat_id=update.message.chat_id
            markup=telegram.InlineKeyboardMarkup(buttons)
            self.send_text(text,update,context,reply_markup=markup)
            self.dispatcher.add_handler(telegram.ext.CallbackQueryHandler(callback))
        except Exception as e:
            print('Thanks for testing, an Error as ocurred please send to my email the full log edkz@nogafam.me')
            self.log.error('Unknow error at lines 196:212, please see the full the log. '+str(e))
    # BETA Maybe dont work ↑
