from pywinauto import Application
import pywinauto
app = Application().start(r"C:\Program Files\Microvirt\MEmu\MEmu.exe")
app = Application().connect(process=29364)
dlg = app.top_window().print_control_identifiers()
print("MEMU0 OUTPUT PRINTING")
dlg2 = app.Memu0.print_control_identifiers()
print("MEMU1 OUTPUT PRINTING")
dlg2 = app.Memu1.print_control_identifiers()
