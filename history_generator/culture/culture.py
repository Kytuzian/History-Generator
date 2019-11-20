from Tkinter import *

import internal.gui as gui
import internal.utility as utility

from form import Form
from art import Art

ART_CATEGORIES = {'artist': ['drawing', 'statue'],
                  'writer': ['play', 'novel', 'essay', 'poem', 'myth'],
                  'composer': ['song', 'musical'],
                  'philosopher': ['essay'],
                  'historian': ['historical essay', 'epic'],
                  'scientist': ['scientific essay'],
                  'oracle': ['prophesy']}

# Painting intentionally included multiple times, because it makes art more likely to be a painting.
ART_STYLES = {'drawing': ['painting', 'painting', 'painting', 'fresco', 'woodblock print', 'sketch']}
ART_SUBCATEGORIES = {'drawing': ['portrait', 'landscape', 'allegorical', 'scene']}

ART_MATERIALS = {'painting': [['<paint> on <medium>']],
                 'woodblock print': [['<paint> on wood']],
                 'fresco': [['<paint> on <medium>']],
                 'sketch': [['<sketch> on <medium>']],
                 'statue': [['<material>']]}

ART_SUBJECTS = {'landscape': [[['<landscape_type:cap><nature>'],
                               ['This is a <well|masterfully|poorly|adequately|knowledgably> painted <picture|image> '
                                'of <article><all_lower><landscape_type>.']]],
                'portrait': [[['<cap><<god>|<notable_person>|<notable_person_role>>'], ['']]],
                'allegorical': [[['<Taste|Touch|Smell|Hearing|Sight>'], ['']]],
                'scene': [[['<titlecase><<god>|<animal>|<notable_person>|<notable_person_role>>'], ['']]],
                'statue': [[['<titlecase><<god>|<animal>|<notable_person>|<notable_person_role>>'], ['']]],
                'song': [[['<cap><<animal>|<nature>|<n>|<god>|<name>|<notable_person>|<notable_person_role>>'], ['']]],
                'musical': [[['<char_name:(<|Sir> <name>)>'], ['It is a <comedy|tragedy|romance> about <char_name>.']],
                            [['The <Tale|Story|Song> of <<notable_person>|<god>|<notable_person_role>|<place>>'], ['']],
                            [['The <Song|Story> of the <cap><animal>'], ['']],
                            [['<titlecase><<name>|<notable_person>|<notable_person_role>> in <place>'], ['']],
                            [['<titlecase><<name>|<notable_person>|<notable_person_role>>'], ['']],
                            [['The <cap><n> of <titlecase><<name>|<notable_person>|<notable_person_role>>'], ['']]],
                'play': [[['The Tale of <<notable_person>|<god>|<notable_person_role>>'], ['']],
                         [['The Story of the <cap><animal>'], ['']],
                         [['<titlecase><<name>|<notable_person>|<notable_person_role>>'], ['']],
                         [['The <cap><n> of <<name>|<notable_person>|<notable_person_role>|<place>>'], ['']]],
                'novel': [
                    [['<cap><article><Tale|Story> of <<notable_person>|<god>|<notable_person_role>|<place>>'], ['']],
                    [['The Story of the <cap><animal>'], ['']], [['<cap><article><adj,> <cap><n>'], ['']],
                    [['<cap><article><|<conj;gerund;<v>>> <cap><n>'], ['']],
                    [['<titlecase><<name>|<notable_person>|<notable_person_role>>'], ['']],
                    [['<cap><place>'], ['']],
                    [['The <cap><n> of <<name>|<notable_person>|<notable_person_role>>'], ['']],
                    [['<titlecase><<name>|<notable_person>|<notable_person_role>> with '
                      '<titlecase><<name>|<notable_person>|<notable_person_role>>'], ['']]],
                'myth': [[['<cap><article><Tale|Story> of <|article><animal|<name>><| and the <animal>>'], ['']]],
                'essay': [[['<On|Concerning> <article><cap><<animal>|<nature>>'], ['']],
                          [['<On|Concerning> <cap><philosophy>'], ['']],
                          [['A Critique of <cap><<philosophy>|<art>>'], ['']],
                          [['<cap><philosophy> in <cap><<art>|<art_creator>|<philosophy>|<art>>'], ['']],
                          [['<Defending|Against> <cap><<art>|<art_creator>|<philosophy>|<art>>'], ['']],
                          [['The <Rise|Fall> of <cap><philosophy>'], ['']],
                          [['Letter from <place>'], ['']]],
                'poem': [[['<cap><animal|nature>'], ['']],
                         [['<Ode|Song> <on|to> <work_subject:cap><<notable_person>|<god>|<place>>'],
                          ['It <celebrates|decries|acknowledges|praises|curses> <work_subject>.']],
                         [['<Ode|Song> <on|to> <subject:article><cap><<animal>|<nature>>'],
                          ['It is about <all_lower><subject>.']],
                         [['<work_subject:cap><conj;gerund;<v>>'], [
                             'It <talks about|discusses|contemplates> <all_lower><work_subject>. The <|attitude of the >poem is generally <positive|negative>.']],
                         [['<cap><conj;gerund;<v>> <indef><cap><n>'], ['']],
                         [['<titlecase><article><adj,> <poem_subject:cap><n>'],
                          ['This poem uses the symbol of <all_lower><article><poem_subject> to <discuss|talk '
                           'about|ponder> the <role|part|place> of <pl><n> in <society|culture|everyday life>.']],
                         [['<titlecase><<name>|<notable_person>|<notable_person_role>>'], ['']],
                         [['The <cap><n> of <titlecase><<name>|<notable_person>|<notable_person_role>>'], ['']]],
                'historical essay': [
                    [['<cap><article>History of <<place>|<notable_person>|<notable_person_role>>'], ['']],
                    [['A Study of <<place>|<notable_person>|<notable_person_role>>'], ['']],
                    [['<On the|The> Effectiveness of the <chosen_weapon:cap><weapon>'],
                     ['It states <self|the author>\'s opinion that the <all_lower><chosen_weapon> is '
                      '<|highly|marginally|sort of|very|extremely> '
                      '<overrated|underappreciated|overused|underused>.',
                      'It states <self|the author>\'s opinion that <all_lower><chosen_weapon> is '
                      '<savage|noble|effective|practical|ineffective|useless>.']],
                    [['<On the|The> Effectiveness of <armor_type:cap><armor>'],
                     ['<This|The> <essay|paper> <<discusses|talks about> the <strengths|weaknesses> '
                      'of <all_lower><armor_type>.|<states|says> that <all_lower><armor_type> is '
                      '<exceedingly|extremely|barely|adequately|sort of|very> '
                      '<useful|useless|effective|ineffective>.>']],
                    [['On <treaty_name:treaty>'],
                     ['This essay <discusses|talks about> <treaty_name>, and <praises|is critical '
                      'of> the treaty\'s <decisiveness|lasting '
                      'impact|strength|weakness|indecisivesness|<short|long> term thinking>.']],
                    [['The <treaty_impact:Failures|Successes|Achievements|Legacy> of '
                      '<treaty_name:treaty>'],
                     ['The author, <self> <believes|thinks|states|says> that the '
                      '<lower><treaty_impact><| of <treaty_name>> is of '
                      '<great|minor|massive|insignificant> '
                      '<historical|cultural|social|societal|intellectual> importance.']],
                    [['<Strengths and Weaknesses|Strengths|Weaknesses> of the '
                      '<chosen_weapon:cap><weapon>'],
                     ['It <states|says> that the <all_lower><chosen_weapon> <<excels|fails|succeeds> '
                      'at|performs <poorly|well> when> <attacking|defending>.']],
                    [['<Strengths and Weaknesses|Strengths|Weaknesses> of <cap><armor>'], ['']]],
                'epic': [[['The Epic of <<place>|<notable_person>|<notable_person_role>>'], ['']]],
                'scientific essay': [[['The <self> Experiment'],
                                      ['The experiment was <|marginally|sort of|very|extremely> <|un>successful.']],
                                     [['An Inquiry into <cap><scientific_subject>'], [
                                         'It goes into <little|moderate|great> depth discussing <|the finer points of> <0>.']],
                                     [['A Study of <cap><scientific_subject>'], ['']]],
                'prophesy': [[['A <Prophesy|Foretelling> of <prophesy_type:a Good Harvest|a Bad '
                               'Harvest|Victory|Peace|a War>'],
                              ['It predicts <that <all_lower><prophesy_type> will come|there will be '
                               '<all_lower><prophesy_type>> in <randint;1;10> years.']],
                             [['<The|A> Prophesy of <chosen_nation:nation>'],
                              ['This prophesy predicts that <chosen_nation> will <fall|gain <|great> glory|achieve '
                               'peace|go to war> in <randint;5;25> years.']],
                             [['A <Prophesy|Foretelling> of <prophesy_type:Destruction|Armageddon|Judgement|Final '
                               'Peace>'],
                              ['This prophesy predicts that there will be <all_lower><prophesy_type> in '
                               '<randint;10;1000> years in the <spring|summer|warm season|fall|autumn|harvest '
                               'season|winter|cold season>.',
                               'This prophesy predicts that <all_lower><prophesy_type> will come in <randint;10;1000> '
                               'years in the <spring|summer|warm season|fall|autumn|harvest season|winter|cold '
                               'season>.',
                               'This prophesy predicts that <all_lower><prophesy_type> will come in <randint;10;1000> '
                               'years.',
                               'This prophesy predicts that there will be <all_lower><prophesy_type> in '
                               '<randint;10;1000> years.']]]}


def create_art(nation, creator):
    category = creator.choice(ART_CATEGORIES[creator.periods[-1].role])

    style = ''
    sub_category = ''
    material = ''

    if category == 'drawing':
        style = creator.choice(ART_STYLES[category])
        sub_category = creator.choice(ART_SUBCATEGORIES[category])

        gen_forms = creator.choice(ART_SUBJECTS[sub_category])
    else:
        gen_forms = creator.choice(ART_SUBJECTS[category])

    gen = Form(gen_forms, custom_weights=creator.periods[-1].custom_weights)
    subject, content = gen.generate(nation=nation, creator=creator)

    if subject is not None:
        creator.periods[-1].custom_weights = gen.custom_weights

        material_gen = None
        if style in ART_MATERIALS:
            material_gen = Form(ART_MATERIALS[style], custom_weights=creator.periods[-1].custom_weights)
        elif category in ART_MATERIALS:
            material_gen = Form(ART_MATERIALS[category], custom_weights=creator.periods[-1].custom_weights)

        name = utility.titlecase(nation.language.translateTo(subject))

        if material_gen is not None:
            material = material_gen.generate(nation=nation, creator=creator)[0]
            creator.periods[-1].custom_weights = material_gen.custom_weights

        return Art(nation, creator, name, subject, category, style, sub_category, content, material, None, gen)
    else:
        return None


class Culture:
    def __init__(self, nation, art=None):
        if art is None:
            art = []
        self.nation = nation

        self.art = art

        self.art_display = None

    def show_information_gui(self):
        self.gui_window = Tk()
        self.gui_window.title('Culture of {}'.format(self.nation.name))
        self.gui_window.geometry("700x750+0+0")
        self.gui_window.config(background='white')

        self.gui_window.columnconfigure(2, weight=1)
        self.gui_window.rowconfigure(2, weight=1)

        self.nation_label = gui.Label(self.gui_window, text='Nation:')
        self.nation_label.grid(row=0, column=0, sticky=W)

        self.nation_button = gui.Button(self.gui_window, text=self.nation.name.short_name(),
                                        command=self.nation.show_information_gui)
        self.nation_button.grid(row=0, column=1, sticky=W)

        self.art_label = gui.Label(self.gui_window, text='Art:')
        self.art_label.grid(row=1, column=0, sticky=W)

        self.art_display = Listbox(self.gui_window)
        self.art_display.grid(row=2, column=0, columnspan=3, sticky=N + S + E + W)
        self.art_display.bind('<Double-Button-1>', self.select_art)

        self.update_art_display()

    def save(self, path):
        res = {}
        res['art'] = []
        for art in self.art:
            res['art'].append(art.get_info())

        with open(path + 'culture.txt', 'w') as f:
            f.write(str(res))

    def select_art(self, event):
        selected_item = self.art_display.get(self.art_display.curselection())
        for art in self.art:
            if '{} ({})'.format(art.name, art.subject) == selected_item:
                art.show_information_gui()
                break

    def update_art_display(self):
        self.art_display.delete(0, END)
        for art in self.art:
            self.art_display.insert(END, '{} ({})'.format(art.name, art.subject))

    def combine(self, other):
        for art in other.art:
            self.add_art(art)

    def add_art(self, work):
        work.nation = self.nation
        self.art.append(work)
