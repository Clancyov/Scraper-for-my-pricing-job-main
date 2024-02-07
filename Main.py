from Iron import Iron
import time

class main:

    def Make_Iron_Pricelists(self):
        Now=time.strftime('(%Y_%m_%d--%H_%M)')
        iron=Iron()
        iron.Run(Now)

    def Make_Phone_Pricelists(self):
        pass

    def Make_Car_Pricelists(self):
        pass

Runner=main()
Runner.Make_Iron_Pricelists()