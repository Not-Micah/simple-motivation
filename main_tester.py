from kivymd.app import MDApp
from kivy.clock import Clock
from kivymd.uix.card import MDCard
from kivymd.uix.widget import MDAdaptiveWidget
#####
from data import read_quotes, write_quote, read_theme, write_theme
#####
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
#####
from retrieve import get_data_from_google_sheet
#####
from threading import Thread
from kivy.clock import mainthread, Clock
#####
import ssl
#####
from kivy.properties import BooleanProperty


ssl._create_default_https_context = ssl._create_unverified_context

class VerificationDialog(MDBoxLayout):
    pass

class QuoteContainer(MDCard, MDAdaptiveWidget):
    pass

class QuoteSaved(MDCard, MDAdaptiveWidget):
    pass

class Main(MDApp):
    isready = BooleanProperty(False)

    def load_qotd(self):
        # get daily quote
        self.qotd = get_data_from_google_sheet()

        # displaying the qotd
        self.root.ids.quote_text.text = self.qotd[0]
        self.root.ids.quote_author.text = self.qotd[1]

        # enabling/disablign the save button
        if self.qotd not in self.saved_quotes:
            self.root.ids.save_button.disabled = False

        self.verification_dialog.content_cls.ids.confirm_button.disabled = False

    def build(self):
        self.theme_cls.theme_style = "Dark"

    def on_start(self):
        self.isready = True

    def on_isready(self, *largs):
        def load_all(*l):
            ###
            self.root.ids.save_button.disabled = True

            ###
            self.saved_quotes = read_quotes()                                                                               # loading the saved quotes from txt

            self.theme = read_theme()                                                                                       # retreiving light/dark mode settings
            self.load_theme()                                                                                               # applying the light/dark mode setting

            self.load_saved_quotes()                                                                                        # loading the quotes at the bottom due to self.theme requirement    
            
            Thread(target=self.load_qotd).start()

            self.verification_dialog = MDDialog(title="Delete Quote?", type="custom", content_cls=VerificationDialog())     # preloading verification dialog

        Clock.schedule_once(load_all, .25)


    @mainthread
    def load_saved_quotes(self):
        self.root.ids.saved_container.clear_widgets()

        for i in range(len(self.saved_quotes)):
            card = QuoteSaved()
            card.ids.quote_card_text.text = self.saved_quotes[i][0]
            card.ids.quote_card_author.text = self.saved_quotes[i][1]

            if self.theme == "dark":
                card.ids.quote_card_text.color = "#FAF9F6"
                card.ids.quote_card_author.color = "#FAF9F6"
                card.md_bg_color = "#191919"

            elif self.theme == "light":
                card.ids.quote_card_text.color = "#040404"
                card.ids.quote_card_author.color = "#040404"
                card.md_bg_color = "#FCFCFC"

            self.root.ids.saved_container.add_widget(card)

    @mainthread
    def save_quote(self):
        self.saved_quotes.append(self.qotd)
        
        # creating a saved quote card
        card = QuoteSaved()
        card.ids.quote_card_text.text = self.qotd[0]
        card.ids.quote_card_author.text = self.qotd[1]

        if self.theme == "dark":
            card.ids.quote_card_text.color = "#FAF9F6"
            card.ids.quote_card_author.color = "#FAF9F6"
            card.md_bg_color = "#191919"

        elif self.theme == "light":
            card.ids.quote_card_text.color = "#040404"
            card.ids.quote_card_author.color = "#040404"
            card.md_bg_color = "#FCFCFC"

        self.root.ids.saved_container.add_widget(card)

        # clearing the file
        with open("saved.txt", "w") as f:
            f.truncate(0)

        # rewriting all the saved quotes
        for i in range(len(self.saved_quotes)):
            write_quote(self.saved_quotes[i][0], self.saved_quotes[i][1])

    def open_verification(self, card):
        self.verification_dialog.content_cls.ids.preview_quote.text = card.ids.quote_card_text.text
        self.verification_dialog.open()

    def delete_quote(self, quote):
        # allowing the user to save the qotd after it being deleted
        if quote == self.qotd[0]:
            self.root.ids.save_button.disabled = False

        for i in range(len(self.saved_quotes)):
            if quote == self.saved_quotes[i][0]:
                self.saved_quotes.pop(i)
                break

        Thread(target=self.load_saved_quotes).start()
        self.verification_dialog.dismiss()

        # clearing the file
        with open("saved.txt", "w") as f:
            f.truncate(0)

        # rewriting all the saved quotes
        for i in range(len(self.saved_quotes)):
            write_quote(self.saved_quotes[i][0], self.saved_quotes[i][1])

    def theme_logic(self):
        if self.theme == "light":
            self.theme = "dark"

        elif self.theme == "dark":
            self.theme = "light"

        Thread(target=self.load_theme).start()

    def load_theme(self):
        if self.theme == "dark":
            # quote box
            self.root.ids.main.md_bg_color = "#121212"                          # COLOR 2
            self.root.ids.quote_text.color = "#FAF9F6"
            self.root.ids.quote_author.color = "#FAF9F6"
            
            # panel colors
            self.root.ids.navigation.text_color_normal = "#919191"
            self.root.ids.navigation.text_color_active = "#F7F7F7"
            self.root.ids.navigation.panel_color = "#191919"                    # COLOR 1

            # icon colors
            self.root.ids.save_button.icon_color = "#FAF9F6"
            self.root.ids.theme_button.icon_color = "#FAF9F6"
            self.root.ids.refresh_button.icon_color = "#FAF9F6"

            # card container
            self.root.ids.main_two.md_bg_color = "#121212"
            self.root.ids.saved_title.color = "#FAF9F6"

        elif self.theme == "light":
            # quote box
            self.root.ids.main.md_bg_color = "#F6F6F6"                          # COLOR 2
            self.root.ids.quote_text.color = "#040404"
            self.root.ids.quote_author.color = "#040404"
            
            # panel colors
            self.root.ids.navigation.text_color_normal = "#636363"
            self.root.ids.navigation.text_color_active = "#040404"
            self.root.ids.navigation.panel_color = "#DDDDDD"                    # COLOR

            # icon colors
            self.root.ids.save_button.icon_color = "#000000"
            self.root.ids.theme_button.icon_color = "#000000"
            self.root.ids.refresh_button.icon_color = "#000000"

            # card container
            self.root.ids.main_two.md_bg_color = "#F6F6F6"
            self.root.ids.saved_title.color = "#040404"
    
        Thread(target=self.load_saved_quotes).start()

        # updating theme content
        with open('theme.txt', 'w') as f:
            f.write(self.theme)

if __name__ == "__main__":
    Main().run()