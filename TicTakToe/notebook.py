# Notebook widget example using tix
import tkinter.tix as tix
import tkinter.messagebox as mb

top = tix.Tk()
nb = tix.NoteBook(top, width=300, height=300)
nb.pack(expand=True, fill="both")

nb.add("Page1", label="Text")
frame1 = tix.Frame(nb.subwidget("page1"))
st = tix.ScrolledText(frame1)
st.subwidget("text").insert("1.0", "Type text here...")
st.pack(expand=True)
frame1.pack()

nb.add("Page2", label="Message boxes")
frame2 = tix.Frame(nb.subwidget("page2"))

tix.Button(frame2, text="Error", bg="red",
           command=lambda t="error", m="This is bad":
           mb.showerror(t, m)).pack(fill="x", expand=True)

tix.Button(frame2, text="Info", bg="lightblue",
           command=lambda t="info", m="Some Information":
           mb.showinfo(t, m)).pack(fill="x", expand=True)

tix.Button(frame2, text="Warning", bg="yellow",
           command=lambda t="warning", m="Shtsksm":
           mb.showwarning(t, m)).pack(fill="x", expand=True)

tix.Button(frame2, text="Question", bg="green",
           command=lambda t="question", m="Shtsksm?":
           mb.askyesno(t, m)).pack(fill="x", expand=True)

tix.Button(frame2, text="Yes-No", bg="lightgrey",
           command=lambda t="yes-no", m="Are you sure?":
           mb.askyesno(t, m)).pack(fill="x", expand=True)

tix.Button(frame2, text="Yes-No-Cancel", bg="white",
           command=lambda t="yes-no-cancel", m="Last chance, are you sure?":
           mb.askyesnocancel(t, m)).pack(fill="x", expand=True)

frame2.pack()
top.mainloop()
