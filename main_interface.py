from tkinter import *
from tkinter import ttk
from tkinter.ttk import Combobox
from main import testActorandPlanner
from shared import GLOBALS
from shared.gui import globalQueue
from multiprocessing import Queue
from PIL import ImageTk, Image

class MainInterface():
    def __init__(self):
        self.window = Tk()
        style = ttk.Style(self.window)
        style.theme_use('clam')

        domain = Label(text="Domain")
        domain.place(x=5,y=10)
        self.domain_cb = Combobox(self.window, values=("fetch", "nav", "rescue", "explore", "deliver"))
        self.domain_cb.place(x=130, y=10)

        actor = Label(text="Acting Engine")
        actor.place(x=5,y=40)
        self.actor_cb = Combobox(self.window, values=("RAE", "APE"))
        self.actor_cb.place(x=130, y=40)

        problemLabel = Label(text="Problem")
        problemLabel.place(x=5,y=70)
        self.problem_text = Text(self.window, height=1, width=27, background='#EEEEEE')
        self.problem_text.place(x=130, y=70)

        planner = Label(text="Planner")
        planner.place(x=5,y=100)
        self.planner_cb = Combobox(self.window, values=("UPOM", "RAEPlan", "APEPlan", "None"))
        self.planner_cb.place(x=130, y=100)

        timelimLabel = Label(text="Time Limit for Planner")
        timelimLabel.place(x=5,y=130)
        self.timelim_text = Text(self.window, height=1, width=25, background='#EEEEEE')
        self.timelim_text.place(x=150, y=130)

        utility = Label(text="Utility")
        utility.place(x=5,y=160)
        self.utility_cb = Combobox(self.window, values=("efficiency", "successRatio", "costEffectiveness"))
        self.utility_cb.place(x=130, y=160)

        learningStrategy = Label(text="Learning Strategy")
        learningStrategy.place(x=5,y=190)
        self.learning_cb = Combobox(self.window, values=("None", "learnM", "learnH", "learnMI"))
        self.learning_cb.place(x=130, y=190)

        self.run_button = Button(self.window,
                        text="Run",
                        command=self.Run)
        self.run_button.place(x=200,y=220)

        self.clear_button = Button(self.window,
                                 text="Clear",
                                 command=self.Clear)
        self.clear_button.place(x=240,y=220)

        self.output = Text(self.window, height=45, width=77, background='#EEEEEE')
        self.output.place(x=350, y=5)

        self.result = Text(self.window, height=26, width=47, background='#EEEEEE')
        self.result.place(x=5, y=250)
        self.resultQueue = Queue()



        # lb=Listbox(window, height=5, selectmode='multiple')
        # for num in data:
        #     lb.insert(END,num)
        # lb.place(x=250, y=150)

        # v0=IntVar()
        # v0.set(1)
        # r1=Radiobutton(window, text="male", variable=v0,value=1)
        # r2=Radiobutton(window, text="female", variable=v0,value=2)
        # r1.place(x=100,y=50)
        # r2.place(x=180, y=50)

        # v1 = IntVar()
        # v2 = IntVar()
        # C1 = Checkbutton(window, text = "Cricket", variable = v1)
        # C2 = Checkbutton(window, text = "Tennis", variable = v2)
        # C1.place(x=100, y=100)
        # C2.place(x=180, y=100)

        self.window.title('Refinement Acting, Planning and Learning Engine')
        self.window.geometry("900x600")
        self.window.mainloop()



    def Run(self):
        self.window.after(1, self.simulate)
        GLOBALS.SetDataGenerationMode(None)
        GLOBALS.SetUtility(self.utility_cb.get())
        GLOBALS.SetHeuristicName(None)
        GLOBALS.SetDoIterativeDeepening(False)
        GLOBALS.SetTimeLimit(500)
        GLOBALS.SetModelPath("./learning/models/AIJ2020/")
        planner = None if self.planner_cb.get() == "None" else self.planner_cb.get()
        learningStrategy = None if self.learning_cb.get() == "None" else self.learning_cb.get()
        testActorandPlanner(
                    domain=self.domain_cb.get(),
                    problem=self.problem_text.get("1.0","end-1c"),
                    actor=self.actor_cb.get(),
                    useLearningStrategy=learningStrategy,
                    planner=planner,
                    plannerParams=[50],
                    showGui='off',
                    v=0,
                    outputQueue=self.resultQueue
        )
        # testActorandPlanner(
        #     domain='fetch',
        #     problem='problem1',
        #     actor='RAE',
        #     useLearningStrategy='learnM',
        #     planner=None,
        #     plannerParams=[50],
        #     showGui='off',
        #     v=0,
        #     outputQueue=self.resultQueue,
        # )


    def Clear(self):
        self.output.delete("1.0","end")
        self.result.delete("1.0","end")

    def simulate(self):
        if not globalQueue.empty():
            t = globalQueue.get()
            t1 = ' '.join(map(str, t))
            self.output.insert(END, t1)
        if not self.resultQueue.empty():
            t = self.resultQueue.get()
            self.result.insert(END, t)

            # x = Tk()
            # self.rTree = Canvas(x, width = 1000, height = 1000)
            # self.rTree.place(x=0, y=0)
            # img = ImageTk.PhotoImage(Image.open("actingTree.png"))
            # self.rTree.create_image(500, 500, anchor=SE, image=img)
            # x.mainloop()

            #img = Image.open("actingTree.png")
            #img = img.resize((500, 500))
            #self.rTree.create_image(500, 500, anchor=SE, image=ImageTk.PhotoImage(img))


        self.window.after(1, self.simulate)

if __name__=="__main__":
    MainInterface()

