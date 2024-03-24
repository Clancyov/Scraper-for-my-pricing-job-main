from Iron import Iron
from Phone import Phone
import time

Now=time.strftime('(%Y_%m_%d--%H_%M)')

class main:

    def Make_Iron_Pricelists(self):
        
        iron = Iron()
        iron.Run(Now)

    def Make_Phone_Pricelists(self):

        phone = Phone()
        phone.Run(Now)

    def Make_Car_Pricelists(self):
        pass

Runner=main()
# Runner.Make_Iron_Pricelists()
Runner.Make_Phone_Pricelists()